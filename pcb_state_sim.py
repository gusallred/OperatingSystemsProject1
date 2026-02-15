# CS 440 – PCB Simulator Starter (Python)
# Names: Augustus Allred, David Gonzalez
# Last digits of BearID: 9415 and 1417
# Date: 02/14/2026
#
# Usage: python pcb_state_sim.py -f <trace_file>
# python pcb_state_sim.py -f trace1_happy.txt
# python pcb_state_sim.py -f trace2_errors.txt
# python pcb_state_sim.py -f trace3_kill_extra.txt

import argparse

import pcb_handlers as handlers
import pcb_types as types


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default='trace1_happy.txt', type=str, help="File name")
    args = parser.parse_args()
    trace = open(args.f, "r")
    trace_lines = trace.readlines()
    trace.close()

    system_state = types.PCBStates()
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
