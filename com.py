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
    new_settings = [27394, 2, 19200, 71, 38400, 38400, ['\x04', '\xff', '\xff', '\x7f', '\x17', '\x15', '\x12', '\x00', '\x03', '\x1c', '\x1a', '\x19', '\x11', '\x13', '\x16', '\x0f', 1, 0, '\x14', '\x00']]
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

    thread_input = threading.Thread(target=input_thread)
    thread_output = threading.Thread(target=output_thread)

    thread_input.start()
    thread_output.start()

    if thread_input.isAlive():
        thread_input.join()
    if thread_output.isAlive():
        thread_output.join()

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
