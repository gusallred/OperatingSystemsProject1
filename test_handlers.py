from collections import deque
from pcb_handlers import State, handle_dispatch, handle_tick, handle_block, handle_wake, handle_exit


class PCB:
    def __init__(self, pid, name, priority):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.state = State.READY
        self.pc = 0  # Program counter
        self.cpu_time = 0  # Total CPU time used


process_table = {"P1": PCB(1, "P1", 3), "P2": PCB(2, "P2", 1)}
ready_q = deque(["P1", "P2"])
waiting_q = deque()
running = None

ok, msg, running = handle_dispatch(process_table, ready_q, waiting_q, running)
print(ok, msg, "running = ", running)

ok, msg, running = handle_tick(process_table, ready_q, waiting_q, running, "4")
print(ok, msg, "P1 pc = ", process_table["P1"].pc)

ok, msg, running = handle_block(process_table, ready_q, waiting_q, running, "P1")
print(ok, msg, "running = ", running, "waiting = ", list(waiting_q))