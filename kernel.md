# Modules Modification
The following chapters show how to integrate USB serial option driver into the Linux operating system.

## Add VID and PID
In order to recognize the module, the module’s VID and PID information as below need to be added to the
file `[KERNEL]/drivers/usb/serial/option.c`.

```
static const struct usb_device_id option_ids[] = {
#if 1 //Added by Quectel
	{ USB_DEVICE(0x05C6, 0x9090) }, /* Quectel UC15 */
	{ USB_DEVICE(0x05C6, 0x9003) }, /* Quectel UC20 */
	{ USB_DEVICE(0x05C6, 0x9215) }, /* Quectel EC20(MDM9215) */
	{ USB_DEVICE(0x2C7C, 0x0125) }, /* Quectel EC20(MDM9x07)/EC25/EG25 */
	{ USB_DEVICE(0x2C7C, 0x0121) }, /* Quectel EC21 */
	{ USB_DEVICE(0x2C7C, 0x0191) }, /* Quectel EG91 */
	{ USB_DEVICE(0x2C7C, 0x0195) }, /* Quectel EG95 */
	{ USB_DEVICE(0x2C7C, 0x0306) }, /* Quectel EG06/EP06/EM06 */
	{ USB_DEVICE(0x2C7C, 0x030B) }, /* Quectel EG065K/EG060K */
	{ USB_DEVICE(0x2C7C, 0x0512) }, /* Quectel EG12/EP12/EM12/EG16/EG18 */
	{ USB_DEVICE(0x2C7C, 0x0296) }, /* Quectel BG96 */
	{ USB_DEVICE(0x2C7C, 0x0700) }, /* Quectel BG95/BG77/BG600L-M3/BC69 */
	{ USB_DEVICE(0x2C7C, 0x0435) }, /* Quectel AG35 */
	{ USB_DEVICE(0x2C7C, 0x0415) }, /* Quectel AG15 */
	{ USB_DEVICE(0x2C7C, 0x0452) }, /* Quectel AG520 */
	{ USB_DEVICE(0x2C7C, 0x0455) }, /* Quectel AG550 */
	{ USB_DEVICE(0x2C7C, 0x0620) }, /* Quectel EG20 */
	{ USB_DEVICE(0x2C7C, 0x0800) }, /* Quectel RG500/RM500/RG510/RM510 */
	{ USB_DEVICE(0x2C7C, 0x0801) }, /* Quectel RG520/RM520/SG520 */
	{ USB_DEVICE(0x2C7C, 0x6026) }, /* Quectel EC200 */
	{ USB_DEVICE(0x2C7C, 0x6120) }, /* Quectel UC200 */
	{ USB_DEVICE(0x2C7C, 0x6000) }, /* Quectel EC200/UC200 */
	{ .match_flags = USB_DEVICE_ID_MATCH_VENDOR, .idVendor = 0x2C7C }, /* Match All Quectel Modules */
#endif
```

## Add the Zero Packet Mechanism
As required by the USB protocol, the mechanism for processing zero packets needs to be added during bulk-out transmission by adding the following statements. For Linux kernel version higher than 2.6.34, add the following statements to the file `[KERNEL]/drivers/usb/serial/usb_wwan.c`.

```
static struct urb *usb_wwan_setup_urb(struct usb_serial_port *port,
				      int endpoint,
				      int dir, void *ctx, char *buf, int len,
				      void (*callback) (struct urb *))
{
	...

	usb_fill_bulk_urb(urb, serial->dev,
			  usb_sndbulkpipe(serial->dev, endpoint) | dir,
			  buf, len, callback, ctx);

#if 1 //Added by Quectel for Zero Packet
	if (dir == USB_DIR_OUT) {
		...
		if (serial->dev->descriptor.idVendor == cpu_to_le16(0x2C7C))
			urb->transfer_flags |= URB_ZERO_PACKET;
	}
#endif
```

## Add Reset-resume Mechanism
Some USB host controllers/USB hubs will lose power or be reset when MCU enters the Suspend/Sleep mode, and cannot be used for USB resume after MCU exits from the Suspend/Sleep mode. The reset-resume mechanism needs to be enabled by adding the following statements. For Linux kernel version higher than 3.4, add the following statements to the file
`[KERNEL]/drivers/usb/serial/option.c`.

```
static struct usb_serial_driver option_1port_device = {
...
#ifdef CONFIG_PM
	.suspend           = usb_wwan_suspend,
	.resume            = usb_wwan_resume,
#if 1 //Added by Quectel
	.reset_resume = usb_wwan_resume,
#endif
#endif
};
```

