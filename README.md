# usbreq — a PyUSB wrapper for rapid testing and prototyping

usbreq is a WIP simple helper Python module for quick scripts and tests with USB devices.
It is not intended for stable programs.


## Usage

The core of this library is the [`USBDevice`](./usbreq/__init__.py#L232) class, which wraps
[PyUSB's](https://github.com/pyusb/pyusb) `usb.core.Device` class, and adds additional shortcut methods
(currently only two):

- `USBDevice.control_request(self, *, direction, req_type, recipient, request, value, index, length, data)`
	- `direction`, `req_type`, `recipient`, and `request` are accepted as strings (in any case), integers,
		or instances of usbreq's relevant enums (e.g. `req_type=usbreq.USBRequestType.STANDARD`).
	- The fields of `bmRequestType` (`direction`, `req_type`, and `recipient`) when given as integers are accepted
		either bitshifted or not.
	- For accepting `request` as a string, currently all standard requests of all recipients are implemented,
		but class requests are not yet.
	- `data` cannot be specified for IN requests
	- `length` is optional and inferred from data for OUT requests, or set to maximum (0xFF) for IN requests.
		- If specified for OUT requests, only the specified amount of `data` will be sent to the device.
- `USBDevice.get_descriptor(self, *, type, index, langid=None, length, find_intended=False)`
	- `type` is accepted as a string (in any case), an int, or an instance of `usbreq.USBDescriptorType`.
	- `index` is optional and defaults to 0.
	- `langid` only makes sense if `type="string"`, and is optional there as well (defaults to 0)
	- `length` is passed through directly to `USBDevice.control_request()`
	- `find_intended=True` asks this method to "cheat" for you and find a descriptor that is not directly requestable
		in USB, by parsing data for you. For example: `get_descriptor(type="endpoint", index=1, find_intended=True)`
		will first request the device's configuration descriptor, and then parse its subordinate descriptors to find
		the the second (zero-indexed) descriptor where bDescriptorType is 0x05.


## Documentation

Hopefully at some point I will solve Sphinx's riddle, but for now, this library is only really documented in this
readme, and in the code via docstrings. Sorry!
