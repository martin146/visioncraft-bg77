# Quectel BG77 Controller App
The developed application allows for the management of Quectel BG77 via a simple command line interface (CLI). The basic network parameters can be set using a YAML configuration file. In addition, the application allows checking the network status, sending AT commands, or conducting network attachments.

## Prerequisites

### Kernel Modules
Although Quectel BG77 utilizes a conventional Linux USB driver, its ID is not a part of the conventional Linux kernel. Thus, it requires modification of **option** and **usb_wwan** kernel module followed by new kernel compilation. The kernel modification required for proper functionality of the Quectel BG77 module is described [here](readme.md).

### Python Environment

The developed application is written in Python 3 (at least version 3.6), and all required packages are listed in **requirerements.txt**. All dependencies can be automatically installed by command `pip install -r requirements.txt` or `pip3 install -r requirements.txt` on some operating systems.

### How to Communicate with Module

When the USB serial option driver has been installed in the module, the device files (usually) named as `ttyUSB0`, `ttyUSB1`, `ttyUSB2`, etc. will be created in directory `/dev`.  The developed application utilizes the last virtual serial port (ttyUSB2) to communicate directly with the Quectel BG77 module via AT commands. The remaining virtual ports can be used for modem debugging and communication with integrated GPS module.

Finally, after successful registration in the network, a new eth (usually eth1) interface is created via the Ethernet Control Mode (ECM) of a modem USB interface. When this interface is assigned an IP address, it indicates successful network registration. However, such an indication is somehow clumsy, and the developed application provides a more convenient way of checking the network status.




