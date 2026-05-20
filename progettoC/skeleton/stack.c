/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#include "stack.h"
#include <stdio.h>
#include <stdlib.h>

StackElement stack[MAX_STACK];
int stack_size = 0;

void push_tensor(Tensor *t) {
    // TODO: Implementare l'inserimento sullo stack verificando il MAX_STACK
}

void push_string(char *s) {
    // TODO: Implementare l'inserimento di una stringa sullo stack
}

StackElement pop() {
    StackElement empty;
    // TODO: Implementare il prelievo dallo stack, gestendo l'underflow
    return empty;
}

Tensor* pop_tensor() {
    // TODO: Usare pop() e assicurarsi che sia di tipo TENSOR
    return NULL;
}

char* pop_string() {
    // TODO: Usare pop() e assicurarsi che sia di tipo STRING
    return NULL;
}
