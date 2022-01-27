import enum

import usb.core
import inflection


def find(*args, **kwargs):
    return USBDevice(usb.core.find(*args, **kwargs))


class USBDirection(enum.IntEnum):
    """ This class is used internally, and should not be considered a public part of the API. """

    OUT = 0x00
    IN  = 0x80

    HOST_TO_DEVICE = 0x00
    DEVICE_TO_HOST = 0x80


    @classmethod
    def parse(cls, direction):

        if isinstance(direction, str):

            direction = direction.upper().replace('-', '_').replace(' ', '_')
            return cls[direction]

            # if direction in ('IN', 'DEVICE_TO_HOST', 'DEVICE-TO-HOST', 'DEVICE TO HOST'):
                # return USBDirection.IN

            # elif direction in ('OUT', 'HOST_TO_DEVICE', 'HOST-TO-DEVICE', 'HOST TO DEVICE'):
                # return USBDirection.OUT

            # else:
                # raise ValueError(
                    # "Direction specified as a string must be one of the following, in any case, with whitespace, underscores, or dashes:\n"
                    # "'IN', 'DEVICE_TO_HOST', 'OUT', 'HOST_TO_DEVICE'"
                # )


        elif isinstance(direction, int):

            masked = direction & 0x80

            if direction == 0 or masked == 0x00:
                return USBDirection.OUT

            elif direction == 1 or masked == 0x80:
                return USBDirection.IN

            else:
                raise ValueError(
                    "Direction specified as an int must be a valid bmRequestType value, or a valid value for the direction field of bmRequestType"
                )

        else:
            raise TypeError("Direction must either be specified as a string or an int")


class USBRequestType(enum.IntEnum):
    """ This class is used internally, and should not be considered a public part of the API. """

    STANDARD = 0x00
    CLASS    = 0x20
    VENDOR   = 0x40
    RESERVED = 0x60

    @classmethod
    def parse(cls, req_type):

        if isinstance(req_type, str):

            req_type = req_type.upper()
            return cls[req_type]

        elif isinstance(req_type, int):

            masked = req_type & 0x60

            if req_type == 0 or masked == cls.STANDARD:
                return cls.STANDARD

            elif req_type == 1 or masked == cls.CLASS:
                return cls.CLASS

            elif req_type == 2 or masked == cls.VENDOR:
                return cls.VENDOR

            elif req_type == 3 or masked == cls.RESERVED:
                return cls.RESERVED

            else:
                raise ValueError(
                    "Request type specified as an int must be a valid bmRequestType value, or a valid value for the type field of bmRequestType"
                )

        else:
            raise TypeError("Request type must either be specified as a string or an int")


class USBRecipient(enum.IntEnum):
    """ This class is used internally, and should not be considered a public part of the API. """

    DEVICE    = 0x00
    INTERFACE = 0x01
    ENDPOINT  = 0x02
    OTHER     = 0x03
    RESERVED  = 0x04

    @classmethod
    def parse(cls, recipient):

        if isinstance(recipient, str):

            recipient = recipient.upper()
            return cls[recipient]

        elif isinstance(recipient, int):

            masked = recipient & 0x1F

            if recipient == 0 or masked == cls.DEVICE:
                return cls.DEVICE

            elif recipient == 1 or masked == cls.INTERFACE:
                return cls.INTERFACE

            elif recipient == 2 or masked == cls.ENDPOINT:
                return cls.ENDPOINT

            elif recipient == 3 or masked == cls.OTHER:
                return cls.OTHER

            else:
                return cls.RESERVED

        else:
            raise TypeError(
                "Request recipient must either be specified as a string or an int"
            )


class USBRequestNumber(enum.IntEnum):

    GET_STATUS        = 0x00
    CLEAR_FEATURE     = 0x01
    SET_FEATURE       = 0x03
    SET_ADDRESS       = 0x05
    GET_DESCRIPTOR    = 0x06
    SET_DESCRIPTOR    = 0x07
    GET_CONFIGURATION = 0x08
    SET_CONFIGURATION = 0x09
    GET_INTERFACE     = 0x0A
    SET_INTERFACE     = 0x11
    SYNCH_FRAME       = 0x12


    @classmethod
    def parse(cls, request):

        if isinstance(request, str):

            request = inflection.underscore(request).upper()
            return cls[request]

        elif isinstance(request, int):

            return cls(request)

        else:
            raise TypeError(
                "Request number must either be specified as a string or an int"
            )


class USBDescriptorType(enum.IntEnum):
    """ Descriptor types valid for :py:meth:`USBDevice.get_descriptor`."""

    DEVICE        = 0x01
    CONFIGURATION = 0x02
    STRING        = 0x03
    INTERFACE     = 0x04
    ENDPOINT      = 0x05


    @classmethod
    def parse(cls, descriptor_type):
        """
        Parses a descriptor type from a string or a number. Strings are accepted in any case.

        :param descriptor_type: A string or integer describing the descriptor type.
        :type descriptor_type: str or int
        """

        if isinstance(descriptor_type, str):
            descriptor_type = descriptor_type.upper()
            return cls[descriptor_type]

        elif isinstance(descriptor_type, int):
            return cls(descriptor_type)

        else:
            raise TypeError(
                "Descriptor type must either be specified as a string or an int"
            )


class USBDevice:

    def __init__(self, dev: usb.core.Device):

        self.dev = dev


    def __getattr__(self, attr):
        return getattr(self.dev, attr)


    def control_request(self, *, direction, req_type, recipient, request, value, index, length=None, data=None):

        direction = USBDirection.parse(direction)
        req_type = USBRequestType.parse(req_type)
        recipient = USBRecipient.parse(recipient)

        bmRequestType = (
            direction.value |
            req_type.value |
            recipient.value
        )

        bRequest = USBRequestNumber.parse(request).value
        wValue = value
        wIndex = index

        if direction == USBDirection.IN and data is not None:
            raise ValueError("Incompatible arguments: direction == IN, data != None")

        if direction == USBDirection.OUT and data is None:
            raise ValueError("OUT request specified but data to send not given")

        if direction == USBDirection.OUT:

            if length is not None:
                data = data[0..length]

            return self.ctrl_transfer(bmRequestType=bmRequestType, bRequest=bRequest,
                wValue=wValue, wIndex=wIndex, data_or_wLength=data,
            )

        else:

            if length is None:
                length = 0xFF # Maxmimum length.

            return bytes(self.ctrl_transfer(bmRequestType=bmRequestType, bRequest=bRequest,
                wValue=wValue, wIndex=wIndex, data_or_wLength=length,
            ))


    def get_descriptor(self, *, type, index=0, langid=None, length=None):
        """
        Shortcut for the GET_DESCRIPTOR standard request.

        Note: A list of known descriptor types can be found at :py:class:`USBDevice`.

        :param type: The type of descriptor to get. Accepts as a string in any case, or a number.
        :type kind: str or int
        :param index: Which descriptor of that type to get, if applicable.
        :type index: int
        :param langid: Optional language ID for a string descriptor, if applicable.
        :type langid: Optional[int]
        :return: The bytes of the descriptor.
        :rtype: bytes
        :raises ValueError: if ``type`` as a string or number does not describe a known descriptor type
        :raises TypeError: if ``type`` is a type other than ``str`` or ``int``
        """

        descriptor_type = USBDescriptorType.parse(type)

        wValue = (descriptor_type.value << 8) | index
        wIndex = langid if langid is not None else 0

        return self.control_request(
            direction='IN',
            req_type='STANDARD',
            recipient='DEVICE',
            request='GET_DESCRIPTOR',
            value=wValue,
            index=wIndex,
            length=length,
        )
