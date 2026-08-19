/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#ifndef STACK_H
#define STACK_H

#include "tensor.h"
#define MAX_STACK 1024

typedef enum { TENSOR, STRING } TokenType;

// Elemento dello stack
typedef struct {
    TokenType type;
    union {
        Tensor *tensor;
        char *string;
    };
} StackElement;

extern StackElement stack[MAX_STACK];
extern int stack_size;

void push_tensor(Tensor *t);
void push_string(char *s);
StackElement pop(void);
Tensor* pop_tensor(void);
char* pop_string(void);

#endif // STACK_H
