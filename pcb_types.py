# pcb_types.py
# Types for PCB state simulation
# # Last digits of BearID: 9415 and 1417

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
        self.process_table = {}    # name -> PCB
        self.ready_q = deque()     # FIFO of process names
        self.waiting_q = deque()   # FIFO of process names
        self.running = None        # process name or None

        self.step = 0
        self.next_pid = 1

        self.BEARID_LAST_DIGIT = max(5, 7)
        self.AUTO_INTERVAL = self.BEARID_LAST_DIGIT + 3