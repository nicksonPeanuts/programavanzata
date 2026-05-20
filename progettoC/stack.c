/*
 * Nome: Nicolo
 * Cognome: Rossi
 * Matricola: 123456
 */

#include "stack.h"
#include <stdio.h>
#include <stdlib.h>

StackElement stack[MAX_STACK];
int stack_size = 0;

void push_tensor(Tensor *t) {
    if (stack_size >= MAX_STACK) {
        fprintf(stderr, "Errore: stack overflow\n");
        exit(1);
    }
    stack[stack_size].type = TENSOR;
    stack[stack_size].tensor = t;
    stack_size++;
}

void push_string(char *s) {
    if (stack_size >= MAX_STACK) {
        fprintf(stderr, "Errore: stack overflow\n");
        exit(1);
    }
    stack[stack_size].type = STRING;
    stack[stack_size].string = s;
    stack_size++;
}

StackElement pop() {
    if (stack_size <= 0) {
        fprintf(stderr, "Errore: stack underflow\n");
        exit(1);
    }
    return stack[--stack_size];
}

Tensor* pop_tensor() {
    StackElement e = pop();
    if (e.type != TENSOR) {
        fprintf(stderr, "Errore: atteso tensore sullo stack\n");
        exit(1);
    }
    return e.tensor;
}

char* pop_string() {
    StackElement e = pop();
    if (e.type != STRING) {
        fprintf(stderr, "Errore: attesa stringa sullo stack\n");
        exit(1);
    }
    return e.string;
}
