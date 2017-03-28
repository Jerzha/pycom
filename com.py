#!/usr/bin/env python
from time import sleep

import serial
import signal
import sys
import thread

dev = sys.argv[1]
se = serial.Serial(dev, 1500000)
is_exit = False
buff = ""


def handle_sigint_tstp(sig, f):
    se.write(chr(0x03))


def exit_com():
    global is_exit
    is_exit = True
    se.close()

signal.signal(signal.SIGINT, handle_sigint_tstp)
signal.signal(signal.SIGTSTP, handle_sigint_tstp)


def input_thread():
    global is_exit, se
    while not is_exit:
        cmd = sys.stdin.readline()
        if cmd.strip() == 'quit':
            exit_com()
        se.write(cmd)


def output_thread():
    global is_exit, se
    while not is_exit:
        line = se.readline()
        print str(line).rstrip('\n')

if not se.is_open:
    print 'Cannot open', dev
    exit(-1)

thread.start_new_thread(input_thread, ())
thread.start_new_thread(output_thread, ())

while not is_exit:
    sleep(1)

print "bye \n"