# pycom
A Simple serial tool for MAC OSX 
The serial tool such as minicom cannot support baurdrate more then 1M (e.g. rk3399 using 1500000 for debug),
but pyserial can do it.<br/>

Usage:<br/>
./pycom /dev/tty.usbserial-xxxxxxx<br/>
Entry 'quit' to exit pycom (ctrl-c will be sent to serial)<br/>

Feature:<br/>
* implement serial input/output
* implement ctrl-c transport
