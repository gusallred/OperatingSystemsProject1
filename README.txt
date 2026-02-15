CS 440 – Programming Assignment 1
PCB & State Transition Simulator
Augustus Allred, David Gonzalez

Course: CS 440 – Operating Systems
Language: Python



1. BearID Auto-STATUS Rule

BearID last digit:
max(5, 7) = 7

Auto-STATUS interval (N + 3):
10

Explanation:
The last digit of the BearID used for this project is 7. According to the assignment specification,
the simulator must automatically print a STATUS snapshot every N + 3 steps. Therefore, the
auto-STATUS interval is 10 steps.



2. Error Handling
(We need to add this when we make last fixes)
Chosen ERROR line:
[step=6] CMD=DISPATCH | ERROR | CPU already running P1

Explanation:
This command is illegal because it violates the simulator’s process state rules. In this case,
the command attempted to perform a DISPATCH, which is not allowed when the CPU is already running.
The error message shows that P1 was already running, and must be blocked, exited, or killed for any
other process to be dispatched. The simulator correctly reports an ERROR and continues execution.



3. Process Lifecycle

Chosen process:
P1

State transitions (from output1.txt):
NEW -> READY -> RUNNING -> WAITING -> READY -> RUNNING -> TERMINATED

Explanation:
Process P1 is created and initially placed in the READY state. It is dispatched to the CPU and
enters the RUNNING state. After executing for some time, it blocks and transitions to WAITING.
Once the I/O operation completes, it is woken and returns to READY. The process is later
dispatched again, executes, and finally terminates.



4. Extra Credit: KILL Command

Description:
The KILL command immediately terminates a specified process regardless of its current state.
If the process is in the READY or WAITING state, it is removed from the corresponding queue.
If the process is RUNNING, it is terminated and the CPU becomes idle. In all cases, the
process’s PCB remains in the process table with state TERMINATED so it continues to appear
in STATUS output.



Notes:
- FIFO scheduling is used for the READY queue.
- Only one process may be in the RUNNING state at a time.
- TERMINATED processes remain in the process table.
- The simulator continues execution after ERROR conditions.
