# Quectel BG77 Controller App
The developed application allows for the management of Quectel BG77 via a simple command line interface (CLI). The basic network parameters can be set using a YAML configuration file. In addition, the application allows checking the network status, sending AT commands, or conducting network attachments.

## Kernel Modules
Although Quectel BG77 utilizes a conventional Linux USB driver, its ID is not a part of the conventional Linux kernel. Thus, it requires modification of **option** and **usb_wwan** kernel module followed by new kernel compilation. The kernel modification required for proper functionality of the Quectel BG77 module is described [here](kernel.md).

## Python Environment

The developed application is written in Python 3 (at least version 3.6), and all required packages are listed in **requirerements.txt**. All dependencies can be automatically installed by command `pip install -r requirements.txt` or `pip3 install -r requirements.txt` on some operating systems.

## How to Communicate with Module

When the USB serial option driver has been installed in the module, the device files (usually) named as `ttyUSB0`, `ttyUSB1`, `ttyUSB2`, etc. will be created in directory `/dev`.  The developed application utilizes the last virtual serial port `ttyUSB2` to communicate directly with the Quectel BG77 module via AT commands. The remaining virtual ports can be used for modem debugging and communication with integrated GPS module.

Finally, after successful registration in the network, a new network interface usually `eth1` interface is created via the Ethernet Control Mode (ECM) of a modem USB interface. When this interface is assigned an IP address, it indicates successful network registration. However, such an indication is somehow clumsy, and the developed application provides a more convenient way of checking the network status.

## Command Line Interface

The developed application uses up to three input arguments based on the selected parameter mode **-m**. A detailed description of the input parameters is provided with a traditional **-h** argument such as `python3 app.py -h`.

The mode parameter **-m** (`python3 app.py -m {att|cmd|link|stat}`) provides four choices of input values, as shown in the table below.

| Mode |         Description         |
|------|:---------------------------:|
| att  |     Network attach mode     |
| cmd  |       Send AT command       |
| link |         Link status         |
| stat | Signal strength and quality |

### Network Attach Mode (att)
Conduct a network-attach procedure with parameters given in the configuration file. It is not necessary to launch this mode with every restart, as the module remembers the last setting and launches the network attachment procedure automatically after power up with the last settings. Therefore, it is recommended that this mode be launched only when the configuration file changes.

### Send AT Command (cmd)
Allows sending commands to the communication module passed via parameter **-c**, which is mandatory in this mode. It is also possible to utilize the second parameter **-t**, which allows setting the AT command timeout in seconds, as some commands take a longer time to process. When no timeout parameter is given, the default value from configuration file is used.

### Link Status (link)
This is the simplest way to check the network connectivity. In this mode, the command returns either `ATTACHED` or `DEATTACHED`, based on the real module network registration status.

### Signal strength and quality (stat)
The signal strength and quality are returned in a human-readable form. In addition, it provides information about the currently utilized technology for communication. All the returned parameters are listed in the table below.

```
Tech: eMTC, RSSI: -46 dBm, RSRP: -69 dBm, SINR: 7.00 dB, RSRQ: -9 dB
```

| Parameter |                             Description                              |
|-----------|:--------------------------------------------------------------------:|
| Tech      |     NOSERVICE - No service, **eMTC** - LTE-M, **NBIoT** - NB-IoT     |
| RSSI      |        Integer indicating the received signal strength in dBm        |
| RSRP      |   An integer indicating the reference signal received power in dBm   |
| SINR      | A float indicating the signal to interference plus noise ratio in dB |
| RSRQ      |  An integer indicating the reference signal received quality in dB   |

## Configuration File
The developed application utilizes the YAML configuration file located in the config.yml file in the same folder as that of the application. The structure of the file is as follows.

```
Port: /dev/ttyUSB2
BaudRate: 115200
APN: lpwa.vodafone.iot
Band:
  - B20
  - B8
  - B3
Tech: LTEM
PLMN: AUTO
RegTimeout: 300
CmdTimeout: 30

Logging:
  file: ./Logs/logs.log
  level: info
```
| Parameter  |                                                                                          Description                                                                                           |
|------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Port       |                                                                              Serial port for sending AT commands                                                                               |
| BaudRate   |                                                                       Serial port baud rate, default value is 115200 Bd                                                                        |
| APN        |                                                                                     Address of APN gateway                                                                                     |
| Band       | List of bands which module scans for. Option `ALL` allows module scan all supported bands (B1, B2, B3, B4, B5, B8, B12, B13, B14, B18, B19, B20, B25, B26, B27, B28, B31, B66, B72, B73, B85). |
| Tech       |                                                               An integer indicating the reference signal received quality in dB                                                                |
| PLMN       |                                Public land mobile network number of selected operator (5 or 6 digits). When `AUTO` is used, operator is automatically selected.                                |
| RegTimeout |                           Maximum timeout for network registration. When no service is found within this limit, the application turns off the radio to save energy.                            |
| CmdTimeout |                                    Default value of AT command timeous in seconds. This value is used when **-t** parameter is not provided in `cmd` mode.                                     |
| Logging    |                  Section for Logging settings. According to set `level`, log of the application is stored into the file which is rotated every 24 hours and kept for 30 days.                  |
| file       |                              Path to the logging file. When the path contains a folder, the folder must exist; otherwise, the app launch will end with an error.                               |
| level      |                        The minimum level of logs which are logged to console and logging file. The allowed values are `debug`, `info`, `warning`, `error`, `critical`.                         |





