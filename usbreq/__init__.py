""" Main module for usbreq. You mostly want the methods of :py:class:`USBDevice`. """

import sys
import enum
import warnings

import usb.core
import inflection


def find(*args, **kwargs):
    """ Creates a :py:class:`USBDevice` using the same logic and arguments as :py:meth:`usb.core.find`. """
    return USBDevice(usb.core.find(*args, **kwargs))


class DummyEnum(int):
    """ Dummy class that wraps an int but has a .value attribute like an enum.

    For cases where an enum is expected but you need a value outside of that enum.
    """

    @property
    def value(self):
        return self


class USBDirection(enum.IntEnum):
    """ The direction field of bmRequestType.

    .. attribute:: OUT
        :annotation: = 0x00
    .. attribute:: HOST_TO_DEVICE
        :annotation: = 0x00
    .. attribute:: IN
        :annotation: = 0x80
    .. attribute:: DEVICE_TO_HOST
        :annotation: = 0x80
    """

    OUT = 0x00
    IN  = 0x80

    HOST_TO_DEVICE = 0x00
    DEVICE_TO_HOST = 0x80


    @classmethod
    def parse(cls, direction):
        """
        Parses a USB direction from a string or number. Strings are accepted in any case,
        with underscores, dashes, or even spaces.

        :param direction:
            A string or integer describing the descriptor type.
            Valid strings are: ``"OUT"``, ``"IN"``, ``"HOST_TO_DEVICE"``, and ``"DEVICE_TO_HOST"``, in any case,
            and with underscores, dashes, or spaces.
        :type direction: str, int, or USBDirection

        :rtype: USBDirection
        """

        if isinstance(direction, cls):
            return direction

        elif isinstance(direction, str):

            direction = direction.upper().replace('-', '_').replace(' ', '_')
            return cls[direction]


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
    """ The type field of bmRequestType.

    .. attribute:: STANDARD
        :annotation: = 0x00
    .. attribute:: CLASS
        :annotation: = 0x20
    .. attribute:: VENDOR
        :annotation: = 0x40
    .. attribute:: RESERVED
        :annotation: = 0x60
    """

    STANDARD = 0x00
    CLASS    = 0x20
    VENDOR   = 0x40
    RESERVED = 0x60

    @classmethod
    def parse(cls, req_type):
        """
        Parses a USB request type from a string or number. Strings are accepted in any case.

        :param req_type:
            A string or integer describing the request type.
            Valid strings are ``"STANDARD"``, ``"CLASS"``, ``"VENDOR"``, and ``"RESERVED"``,
            in any case.
        :type req_type: str, int, or USBRequestType

        :rtype: USBRequestType
        """

        if isinstance(req_type, cls):
            return req_type

        elif isinstance(req_type, str):

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
    """ The recipient field of bmRequestType. """

    DEVICE    = 0x00
    INTERFACE = 0x01
    ENDPOINT  = 0x02
    OTHER     = 0x03
    RESERVED  = 0x04

    @classmethod
    def parse(cls, recipient):
        """
        Parses a USB recipient from a string or number. Strings are accepted in any case.

        :param recipient:
            A string or integer describing the recipient.
            Valid strings are: ``"DEVICE"``, ``"INTERFACE"``, ``"ENDPOINT"``, ``"OTHER"``, and
            ``"RESERVED"``, in any case.
        :type recipient: str, int, or USBRecipient

        :rtype: USBRecipient
        """

        if isinstance(recipient, cls):
            return recipient

        elif isinstance(recipient, str):

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
    """ The bRequest field of setup data. """

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
        """
        Parses a USB request number from a string or number. Strings are accepted in any case,
        with underscores, dashes, or even spaces.

        :param request:
            A string or integer describing the request.
            Valid strings are the enum constants of this class, in any case.
        :type request: str, int, or USBRequestNumber

        :rtype: USBRequestNumber
        """

        if isinstance(request, cls):
            return request

        elif isinstance(request, str):

            request = inflection.underscore(request).upper()
            return cls[request]

        elif isinstance(request, int):

            try:
                return cls(request)
            except ValueError:
                return DummyEnum(request)

        else:
            raise TypeError(
                "Request number must either be specified as a string or an int"
            )


class USBDescriptorType(enum.IntEnum):
    """ Descriptor types valid for :py:meth:`USBDevice.get_descriptor`.

    .. attribute:: DEVICE
        :annotation: = 0x01
    .. attribute:: CONFIGURATION
        :annotation: = 0x02
    .. attribute:: STRING
        :annotation: = 0x03
    .. attribute:: INTERFACE
        :annotation: = 0x04
    .. attribute:: ENDPOINT
        :annotation: = 0x05
    """

    DEVICE        = 0x01
    CONFIGURATION = 0x02
    STRING        = 0x03
    INTERFACE     = 0x04
    ENDPOINT      = 0x05


    @classmethod
    def parse(cls, descriptor_type):
        """
        Parses a descriptor type from a string or number. Strings are accepted in any case.

        :param descriptor_type: A string or integer describing the descriptor type.
        :type descriptor_type: str, int, or USBDescriptorType

        :rtype: USBDescriptorType
        """

        if isinstance(descriptor_type, cls):
            return descriptor_type

        elif isinstance(descriptor_type, str):
            descriptor_type = descriptor_type.upper()
            return cls[descriptor_type]

        elif isinstance(descriptor_type, int):
            try:
                return cls(descriptor_type)
            except ValueError:
                return DummyEnum(descriptor_type)

        else:
            raise TypeError(
                "Descriptor type must either be specified as a string or an int"
            )


class USBDevice:
    """ Wrapper for :py:class:`usb.core.Device` that adds shortcut and convenience methods. """

    def __init__(self, dev: usb.core.Device):

        self.dev = dev


    def __getattr__(self, attr):
        return getattr(self.dev, attr)


    def _get_descriptor(self, *, descriptor_type: USBDescriptorType, index: int, langid=None,
            length=None, req_type='STANDARD', recipient='DEVICE'):

        wValue = (descriptor_type.value << 8) | index
        wIndex = langid if langid is not None else 0

        return self.control_request(
            direction='IN',
            req_type=req_type,
            recipient=recipient,
            request='GET_DESCRIPTOR',
            value=wValue,
            index=wIndex,
            length=length,
        )


    def _find_descriptor_in_chain(self, *, data, descriptor_type: USBDescriptorType, index: int):

        current_bytes = data[0:]
        count_of_type = 0

        while True:

            # First, get the first two fields that every descriptor is guaranteed to have.
            current_length = current_bytes[0]
            current_type = current_bytes[1]

            # If this descriptor type matches the one the user asked for, increment
            # the number of descriptors we have seen of that type.
            if current_type == descriptor_type.value:
                count_of_type += 1

                # With that, if the number of descriptors we've seen of this type
                # is 1 more than the index we're looking for, then this must be the
                # right descriptor. Return the current data bounded by the length
                # of this descriptor we parsed out earlier.
                if (count_of_type - 1) == index:
                    return current_bytes[:current_length]

            # If we didn't return this descriptor, then we need to move onto the next one,
            # by advancing the start of our data by the length of this descriptor.
            try:
                current_bytes = current_bytes[current_length:]
            except IndexError:
                # If we've run out of data, however, then we must not have found the
                # descriptor the user is looking for. Sorry!
                raise ValueError(
                    f"Descriptor of type {descriptor_type} was not found in data: {data}"
                )


    def control_request(self, *, direction, req_type, recipient, request, value=0, index=0, length=None, data=None, **kwargs):
        """ Wrapper for usb.core.Device.ctrl_transfer which has shortcut kwargs for convenience.

        :param direction:
            The direction field of bmRequestType. Accepts everything :py:meth:`USBDirection.parse` does.
        :type direction: str, int, or USBDirection

        :param req_type:
            The type field of bmRequestType. Accepts everything :py:meth:`USBRequestType.parse` does.
        :type req_type: str, int, or USBRequestType
        :param recipient:
            The recipient field of bmRequestType. Accepts everything :py:meth:`USBRecipient.parse` does.
        :type recipient: str, int, or USBRecipient

        :param request:
            The bRequest field of setup data. Accepts everything :py:meth:`USBRequestNumber.parse` does.
        :type request: str, int, or USBRequestNumber

        :param value:
            The wValue field of setup data. Specific to the request you're performing.
        :type value: int

        :param index:
            The wIndex field of setup data. Specific to the request you're performing.
        :type index: int

        :param length:
            How many bytes you want to request from the device or send to the device.
            If specified for OUT requests, your specified data is automatically truncated to this
            length.
            If specified for IN requests, this length is sent as part of the USB request.
            Optional in both cases. If not specified for IN requests, inferred as 0xFF (max length).
        :type length: Optional[int]

        :param data:
            The data to send for OUT requests.
        :type data: bytes
        """

        direction = USBDirection.parse(direction)
        req_type = USBRequestType.parse(req_type)
        recipient = USBRecipient.parse(recipient)

        bmRequestType = (
            direction.value |
            req_type.value |
            recipient.value
        )

        bRequest = USBRequestNumber.parse(kwargs.get("bRequest", request))
        wValue = kwargs.get("wValue", value)
        wIndex = kwargs.get("wIndex", index)
        length = kwargs.get("wLength", length)

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


    def get_descriptor(self, *, type, index=0, langid=None, length=None,
            req_type='STANDARD', recipient='DEVICE', find_intended=False):
        """ Shortcut for the GET_DESCRIPTOR standard request.

        :param type: The type of descriptor to get. Accepts as a string in any case, or a number.
        :type kind: str, int, or USBDescriptorType

        :param index: Which descriptor of that type to get, if applicable.
        :type index: int

        :param langid: Optional language ID for a string descriptor, if applicable.
        :type langid: Optional[int]

        :param find_intended:
            USB does not allow you to individually and directly request
            interface or endpoint descriptors. Specifying `find_intended=True` asks this method,
            instead of making the actual control request that would correspond to the passed
            arguments, to make the request that includes the descriptor you specified with `type`
            and `index`, and then parse the device-returned data to find that descriptor and
            return only that instead.
            This is experimental and may have unexpected results!
        :type find_intended: bool

        :return: The bytes of the descriptor.
        :rtype: bytes
        :raises ValueError: if ``type`` as a string or number does not describe a known descriptor type
        """

        descriptor_type = USBDescriptorType.parse(type)

        # If the user hasn't asked us to cheat, then we're just doing what it says on the tin.
        if not find_intended:

            return self._get_descriptor(
                descriptor_type=descriptor_type,
                index=index,
                langid=langid,
                length=length,
                req_type=req_type,
                recipient=recipient
            )

        # If the user _has_ asked us to cheat, then we have some work to do.
        else:

            available_directly = [
                USBDescriptorType.DEVICE,
                USBDescriptorType.CONFIGURATION,
                USBDescriptorType.STRING,
            ]

            if descriptor_type in available_directly:
                warnings.warn(
                    f"Specified descriptor type {descriptor_type} does not require 'cheating', "
                    "but find_intended was given as True. This may not have been your intention!"
                )
                return self._get_descriptor(
                    descriptor_type=descriptor_type,
                    index=index,
                    langid=langid,
                    length=length,
                    req_type=req_type,
                    recipient=recipient
                )


            # Alright, with that out of the way, let's get to the meat of things.
            # First, request just the configuration descriptor itself, so we can
            # read its wTotalLength field.
            configuration_descriptor = self._get_descriptor(
                req_type='STANDARD',
                recipient='DEVICE',
                descriptor_type=USBDescriptorType.CONFIGURATION,
                index=1,
                length=9,
            )

            # config_total_len = struct.unpack("<h", configuration_descriptor[2:4])[0]
            config_total_len = int.from_bytes(configuration_descriptor[2:4], byteorder='little')

            # Now that we have that, get eeeeeverything that's attached to the configuration
            # descriptor. Hopefully, one if its subordinate descriptors has what we're
            # looking for.
            descriptor_chain = self._get_descriptor(
                req_type='STANDARD',
                recipient='DEVICE',
                descriptor_type=USBDescriptorType.CONFIGURATION,
                index=1,
                length=config_total_len,
            )

            # Sanity check.
            if len(descriptor_chain) != config_total_len:
                print(
                    "Warning: device returned less ({}) than wTotalLength ({})! This is kind of weird!"
                        .format(len(descriptor_chain), config_total_len),
                    file=sys.stderr,
                )

            return self._find_descriptor_in_chain(
                data=descriptor_chain,
                descriptor_type=descriptor_type,
                index=index
            )
