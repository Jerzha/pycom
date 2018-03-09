#!/usr/bin/env python
import sys
import termios
import threading
import serial

dev = ""
baurdrate = 1500000
se = None
is_exit = False

usage = '''
Usage: ./com <dev> [-b <baurdrate>]
Example:
    ./com /dev/tty.usbxxxxx
    ./com /dev/tty.usbxxxxx -b 115200
'''


def exit_com():
    global is_exit
    is_exit = True
    se.close()


def input_thread():
    global is_exit, se
    cmd = ''
    try:
        while not is_exit:
            ch = sys.stdin.read(1)
            cmd += ch
            if sys.version > '3':
                se.write(bytes(ch, encoding='utf-8'))
            else:
                se.write(ch)
            if cmd == 'exit\n':
                exit_com()
            if ch == '\n':
                cmd = ''
    except serial.serialutil.SerialException:
        pass


def output_thread():
    global is_exit, se
    try:
        while not is_exit:
            ch = se.read()
            if sys.version > '3':
                sys.stdout.write(str(ch, encoding='utf-8'))
            else:
                sys.stdout.write(ch)
            sys.stdout.flush()
    except serial.serialutil.SerialException:
        pass


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print(usage)
        exit(0)

    argi = 1
    while argi < len(sys.argv):
        if sys.argv[argi] == '-b':
            baurdrate = sys.argv[argi + 1]
            argi += 1
        elif sys.argv[argi] == '-h':
            print(usage)
            exit(0)
        else:
            dev = sys.argv[argi]
        argi += 1

    print ("Opening %s %s" % (dev, baurdrate))
    se = serial.Serial(dev, baurdrate)
    if not se.is_open:
        print ('Cannot open %s' % (dev))
        exit(-1)

    old_settings = termios.tcgetattr(sys.stdin)
    old3 = old_settings[3]

    # disable PARMRK for func keys
    # disable ICANON for echo back
    # disable ISIG   for sending ctrl-c
    old_settings[3] = old3 & ~termios.PARMRK & ~termios.ICANON & ~termios.ISIG

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    thread_input = threading.Thread(target=input_thread)
    thread_output = threading.Thread(target=output_thread)

    thread_input.start()
    thread_output.start()

    if thread_input.isAlive():
        thread_input.join()
    if thread_output.isAlive():
        thread_output.join()

    old_settings[3] = old3
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
