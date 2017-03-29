#!/usr/bin/env python
import sys
import termios
import threading

import serial

dev = sys.argv[1]
se = serial.Serial(dev, 1500000)
is_exit = False


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
            sys.stdout.write(ch)
            sys.stdout.flush()
    except serial.serialutil.SerialException:
        pass


if __name__ == '__main__':
    if not se.is_open:
        print 'Cannot open', dev
        exit(-1)

    old_settings = termios.tcgetattr(sys.stdin)
    old3 = old_settings[3]
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
