# pycom
A Simple serial tool for MAC OSX / Linux
The serial tool such as minicom cannot support baurdrate more then 1M (e.g. rk3399 using 1500000 for debug),
but pyserial works well.<br/>

## Usage:
* install pyserial first
* ./com /dev/tty.\<dev\> [-b \<baurdrate\>]<br/>
* the default value of baurdrate is 1500000
* entry 'exit' to exit pycom <br/>

## Feature:
* Support serial input/output
* Support ctrl-c transport
* Support all function keys transport

## Q&A:
```
if you got "ImportError: cannot import name properties", please
   sudo easy_install pyserial first
OR sudo pip install pyserial first
```
