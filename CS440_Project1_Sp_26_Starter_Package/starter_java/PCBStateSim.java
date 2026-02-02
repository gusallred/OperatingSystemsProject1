/*
 * CS 440 – PCB Simulator Starter (Java)
 * TODO: Add your name(s) and BearID(s)
 */

import java.util.*;

enum State { NEW, READY, RUNNING, WAITING, TERMINATED }

class PCB {
    int pid;
    String name;
    State state;
    int priority;
    int pc = 0;
    int cpuTime = 0;
}

public class PCBStateSim {
    // TODO: process table (Map<String, PCB>)
    // TODO: READY queue
    // TODO: WAITING queue
    // TODO: RUNNING reference
    // TODO: BearID auto-STATUS interval

    public static void main(String[] args) {
        // TODO: parse args (trace file)
        // TODO: read file line by line
        // TODO: dispatch commands
    }

    // TODO: handlers for CREATE, DISPATCH, TICK, BLOCK, WAKE, EXIT, STATUS, KILL
}
