# CS 440 – PCB Simulator Starter (Python)
# Names: David Gonzalez, Augustus Allred
# Last digits of BearID: 1417 and 9415
# Date: 02/14/2026
#
# Usage: python pcb_state_sim.py -f <trace_file>
# python pcb_state_sim.py -f trace1_happy.txt
# python pcb_state_sim.py -f trace2_errors.txt
# python pcb_state_sim.py -f trace3_kill_extra.txt

import argparse

from enum import Enum
from collections import deque

import handlers


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

        self.BEARID_LAST_DIGIT = max(7, 5)
        self.AUTO_INTERVAL = self.BEARID_LAST_DIGIT + 3


def main():
    # TODO: parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default='trace1_happy.txt', type=str, help="File name")
    args = parser.parse_args()
    trace = open(args.f, "r")
    trace_lines = trace.readlines()
    trace.close()

    system_state = PCBStates()
    print(f"BearID last digit: {system_state.BEARID_LAST_DIGIT}")
    print(f"Auto STATUS every: {system_state.AUTO_INTERVAL} steps\n")
    
    # Read trace file
    print("---- BEGIN LOG ----")
    for line in trace_lines:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue

        line_parts = line.split()
        system_state.step += 1

        # CMD=STATUS
        if line.startswith('STATUS'):
            ''' CMD=STATUS (no args) - print status of all processes '''
            table = handlers.status_snapshot(system_state.process_table, system_state.ready_q, system_state.waiting_q, system_state.running)
            
            print(f"[step={system_state.step}] CMD=STATUS | OK")
            
            print("\n".join(table[:3]) + "\n")
            print("\n".join(table[3:]) + "\n")
            continue

        # CMD=CREATE
        if line.startswith('CREATE'):
            ''' CMD=CREATE <name> <priority> - create process, add to READY '''
            if len(line_parts) != 3:
                ok, msg = False, "Need 2 arguments: name and priority"
            else:
                name = line_parts[1]
                priority = line_parts[2]
                ok, msg, system_state.running = handlers.handle_create(system_state, name, priority)
            pass

        # CMD=DISPATCH
        elif line.startswith('DISPATCH'):
            ''' CMD=DISPATCH (no args) - dispatch next READY process to RUNNING '''
            ok, msg, system_state.running = handlers.handle_dispatch(system_state.process_table, system_state.ready_q, system_state.running)
            pass

        # CMD=TICK
        elif line.startswith('TICK'):
            ''' CMD=TICK <time> - advance time by <time> units, update RUNNING process '''
            if len(line_parts) != 2:
                ok, msg = False, "Need 1 argument: time"
            else:
                n_str = line_parts[1]
                ok, msg, system_state.running = handlers.handle_tick(system_state.process_table, system_state.running, n_str)
            pass

        # CMD=BLOCK
        elif line.startswith('BLOCK'):
            ''' CMD=BLOCK <name> - block the RUNNING process, move to WAITING '''
            if len(line_parts) != 2:
                ok, msg = False, "Need 1 argument: name"
            else:
                name = line_parts[1]
                ok, msg, system_state.running = handlers.handle_block(system_state.process_table, system_state.waiting_q, system_state.running, name)
            pass

        # CMD=WAKE
        elif line.startswith('WAKE'):
            ''' CMD=WAKE <name> - wake the WAITING process with given name, move to READY '''
            if len(line_parts) != 2:
                ok, msg = False, "Need 1 argument: name"
            else:
                name = line_parts[1]
                ok, msg, system_state.running = handlers.handle_wake(system_state.process_table, system_state.ready_q, system_state.waiting_q, system_state.running, name)
            pass

        # CMD=EXIT
        elif line.startswith('EXIT'):
            ''' CMD=EXIT <name> - terminate the RUNNING process, move to TERMINATED '''
            if len(line_parts) != 2:
                ok, msg = False, "Need 1 argument: name"
            else:
                name = line_parts[1]
                ok, msg, system_state.running = handlers.handle_exit(system_state.process_table, system_state.running, name)
            pass

        # CMD=KILL
        elif line.startswith('KILL'):
            ''' CMD=KILL <name> - kill the process with given name, move to TERMINATED '''
            if len(line_parts) != 2:
                ok, msg = False, "Need 1 argument: name"
            else:
                name = line_parts[1]
                ok, msg, system_state.running = handlers.handle_kill(system_state.process_table, system_state.ready_q, system_state.waiting_q, system_state.running, name)
            pass

        # Print command step
        print(f"[step={system_state.step}] CMD={line} | {'OK' if ok else 'ERROR'} | {msg}")

        # Auto-STATUS
        if system_state.step % system_state.AUTO_INTERVAL == 0:
            ''' Auto-STATUS every N steps (N = max last digit of BearIDs) '''
            table = handlers.status_snapshot(system_state.process_table, system_state.ready_q, system_state.waiting_q, system_state.running)
            print("\n".join(table[:3]) + "\n")
            print("\n".join(table[3:]) + "\n")
            pass

    pass
    print("---- END LOG ----\n")

if __name__ == "__main__":
    main()
