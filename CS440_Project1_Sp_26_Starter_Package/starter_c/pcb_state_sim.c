/*
 * CS 440 – PCB Simulator Starter (C)
 * TODO: Add your name(s) and BearID(s)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    NEW, READY, RUNNING, WAITING, TERMINATED
} State;

typedef struct PCB {
    int pid;
    char name[32];
    State state;
    int priority;
    int pc;
    int cpuTime;
    struct PCB *next;
} PCB;

// TODO: process table
// TODO: READY queue
// TODO: WAITING queue
// TODO: RUNNING pointer
// TODO: BearID auto-STATUS interval

int main(int argc, char *argv[]) {
    // TODO: parse args
    // TODO: read trace file
    // TODO: dispatch commands
    return 0;
}

// TODO: implement command handlers
