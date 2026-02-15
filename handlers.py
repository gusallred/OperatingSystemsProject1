# handlers.py
# Command handlers

from collections import deque
from enum import Enum

import pcb_state_sim as sim


def queue_str(q: deque) -> str:
    """Helper function to convert a deque to a string for display."""
    return "[" + ", ".join(list(q)) + "]"

def remove_from_queue(q: deque, pid: int):
    """Remove name from deque if it exists. Returns True if removed."""
    try:
        q.remove(pid)
        return True
    except ValueError:
        return False
    
def status_snapshot(process_table, ready_q, waiting_q, running):
    """Return a list of lines to print for STATUS"""
    lines = []
    lines.append(f"RUNNING: {running if running is not None else 'NONE'}")
    lines.append(f"READY: {queue_str(ready_q)}")
    lines.append(f"WAITING: {queue_str(waiting_q)}")
    lines.append("TABLE:")
    lines.append("PID  NAME  STATE       PRIO  PC  CPUTIME")

    #Print in PID order
    for pcb in sorted(process_table.values(), key=lambda p: p.pid):
        lines.append(f"{pcb.pid:<5}{pcb.name:<6}{pcb.state.name:<12}{pcb.priority:<6}{pcb.pc:<4}{pcb.cpuTime:<9}")
    return lines


# Handlers return:
# (ok: bool, msg: str, new_running: str|None)
# They mutate process_table / queues in place.
def handle_create(system_state, name, priority_str):
    """CREATE <name> <priority>"""
    if name in system_state.process_table:
        return False, f"Error: Process {name} already exists", system_state.running
    
    try:
        priority = int(priority_str)
    except ValueError:
        return False, "Priority must be an integer", system_state.running
    
    if priority < 0:
        return False, "Priority must be non-negative", system_state.running
    
    pid = system_state.next_pid
    system_state.next_pid += 1

    pcb = sim.PCB(pid, name, priority)
    pcb.state = sim.State.READY

    system_state.process_table[name] = pcb
    system_state.ready_q.append(name)

    return True, f"{name}: NEW -> READY (pid={pid})", system_state.running

def handle_dispatch(process_table, ready_q, running):
    """Dispatch is illegal if a process is already RUNNING"""
    if running is not None:
        return False, f"CPU is already running {running}", running
    
    # If no ready processes, return error
    if len(ready_q) == 0:
        return False, "no READY processes", running
    
    # FIFO: pop from front of READY queue
    name = ready_q.popleft()
    pcb = process_table[name]

    # Move READY -> RUNNING
    pcb.state = sim.State.RUNNING
    running = name

    return True, f"{name}: READY -> RUNNING", running


def handle_tick(process_table, running, n_str):
    """Must have RUNNING process to tick"""
    if running is None:
        return False, "CPU is idle", running
    
    # Parse n
    try:
        n = int(n_str)
    except ValueError:
        return False, f"tick amount must be an integer", running
    
    if n < 0:
        return False, f"tick amount must be non-negative", running
    
    pcb = process_table[running]

    # Update PC and CPU time
    pcb.pc += n
    pcb.cpuTime += n

    return True, f"{pcb.name}: pc+={n}, cpuTime+= {n}", running


def handle_block(process_table, waiting_q, running, name):
    """Must have RUNNING process to block"""
    if running is None:
        return False, "CPU is idle", running
    
    # BLOCK <name> must match the RUNNING process
    if name != running:
        return False, f"{name} does not match RUNNING process", running
    
    pcb = process_table[name]

    # RUNNING -> WAITING and CPU becomes idle
    pcb.state = sim.State.WAITING
    waiting_q.append(name)
    running = None

    return True, f"{name}: RUNNING -> WAITING", running


def handle_wake(process_table, ready_q, waiting_q, running, name):
    """Must exist in process_table to wake"""
    if name not in process_table:
        return False, f"{name} does not exist", running
    
    pcb = process_table[name]

    # Must currently be WAITING to wake
    if pcb.state != sim.State.WAITING:
        return False, f"{name} is not WAITING", running
    
    # Remove from WAITING and add to READY
    if not remove_from_queue(waiting_q, name):
        return False, f"{name} not found in WAITING queue", running
    
    pcb.state = sim.State.READY
    ready_q.append(name)

    return True, f"{name}: WAITING -> READY", running


def handle_exit(process_table, running, name):
    """Must exist in process_table to kill"""
    if name not in process_table:
        return False, f"{name} does not exist", running
    
    pcb = process_table[name]

    # EXIT <name> must match the RUNNING process
    if name != running:
        return False, f"{name} is not the running process", running
    
    pcb = process_table[name]

    # RUNNING -> TERMINATED and CPU becomes idle
    pcb.state = sim.State.TERMINATED
    running = None

    return True, f"{name}: RUNNING -> TERMINATED", running


def handle_kill(process_table, ready_q, waiting_q, running, name):
    """Terminate regardless of state"""
    if name not in process_table:
        return False, f"{name} does not exist", running
    
    pcb = process_table[name]

    if pcb.state == sim.State.TERMINATED:
        return False, f"{name} is already TERMINATED", running
    
    if pcb.state == sim.State.READY:
        remove_from_queue(ready_q, name)
        pcb.state = sim.State.TERMINATED
        return True, f"{name}: READY -> TERMINATED", running
    
    if pcb.state == sim.State.WAITING:
        remove_from_queue(waiting_q, name)
        pcb.state = sim.State.TERMINATED
        return True, f"{name}: WAITING -> TERMINATED", running
    
    if pcb.state == sim.State.RUNNING:
        pcb.state = sim.State.TERMINATED
        running = None
        return True, f"{name}: RUNNING -> TERMINATED", running
    
    # If NEW, just mark as TERMINATED
    pcb.state = sim.State.TERMINATED
    return True, f"{name}: NEW -> TERMINATED", running