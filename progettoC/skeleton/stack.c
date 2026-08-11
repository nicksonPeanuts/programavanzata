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


/*
    IMPLEMENTAZIONU DELLE OPERAZIONI DELLO STACK
*/


// INSERIMENTO DI UN TENSOR NELLO STACk
void push_tensor(Tensor *t) {
    if (stack_size == MAX_STACK) {
        printf("Stack overflow\n");
        exit(1);
    }
    stack[stack_size].type = TENSOR;
    stack[stack_size].tensor = t;
    stack_size++;
}

// INSERIMENTO DI UNA STRINGA NELLO STACK
void push_string(char *s) {
    if (stack_size == MAX_STACK) {
        printf("Stack overflow\n");
        exit(1);
    }
    stack[stack_size].type = STRING;
    stack[stack_size].string = s;
    stack_size++;
}

// PRELIEVO DEL TOP DALLO STACK
StackElement pop() {
    if (stack_size == 0) {
        printf("Stack underflow\n");
        exit(1);
    }
    stack_size--;

    return stack[stack_size];
}

// PRELIEVO DI UN TENSOR DAL TOP DALLO STACK
Tensor* pop_tensor() {
    StackElement e = pop();
    if (e.type != TENSOR) {
        printf("Stack element is not a tensor\n");
        exit(0);
    }
    return e.tensor;
}


// PRELIEVO DI UNA STRINGA DAL TOP DALLO STACK
char* pop_string() {
    StackElement e = pop();
    if (e.type != STRING) {
        printf("Stack element is not a string\n");
        exit(0);
    }
    return e.string;
}
