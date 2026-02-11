# CS 440 – PCB Simulator Starter (Python)
# TODO: Add your name(s) and BearID(s)

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

class PCBStates:
    def __init__(self):
        process_table = {}    # name -> PCB
        ready_q = deque()     # FIFO of process names
        waiting_q = deque()   # FIFO of process names
        running = None        # process name or None

        step = 0
        next_pid = 1

        BEARID_LAST_DIGIT = 0   # TODO: set this
        AUTO_INTERVAL = BEARID_LAST_DIGIT + 3

# TODO: process table (dict)
# TODO: READY queue (deque)
# TODO: WAITING queue (deque)
# TODO: RUNNING reference
# TODO: BearID auto-STATUS interval

def main():
    # TODO: parse args
    # TODO: read trace file
    # TODO: dispatch commands
    pass

if __name__ == "__main__":
    main()
