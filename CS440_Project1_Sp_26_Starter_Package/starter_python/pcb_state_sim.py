# CS 440 – PCB Simulator Starter (Python)
# TODO: Add your name(s) and BearID(s)

import argparse

from enum import Enum
from collections import deque

class State(Enum):
    NEW = 0
    READY = 1
    RUNNING = 2
    WAITING = 3
    TERMINATED = 4

class PCB:
    def __init__(self, pid, name, priority):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.state = State.NEW
        self.pc = 0
        self.cpuTime = 0

# TODO: process table (dict)
# TODO: READY queue (deque)
# TODO: WAITING queue (deque)
# TODO: RUNNING reference
# TODO: BearID auto-STATUS interval

def main():
    # TODO: parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default='trace1_happy.txt', type=str, help="File name")
    args = parser.parse_args()
    trace = open(args.f, "r")
    trace_lines = trace.readlines()
    trace.close()
    
    # TODO: read trace file
    for line in trace_lines:
        print(line)
    
    # TODO: dispatch commands
    
    pass

if __name__ == "__main__":
    main()
