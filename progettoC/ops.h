/*
 * Nome: Nicolo
 * Cognome: Rossi
 * Matricola: 123456
 */

#ifndef OPS_H
#define OPS_H

#include "tensor.h"
#include "stack.h"

void op_binary(char op);
void op_not(void);
void op_select(void);
void op_matmul(void);
void op_dot(void);
void op_conv(void);
void op_reshape(void);
void op_ravel(void);
void op_shape(void);
void op_rand(void);
void op_relu(void);
void op_sum(void);
void op_fill(void);
void op_print(void);
void op_dup(void);
void op_swap(void);
void op_over(void);
void op_drop(void);
void op_read_pgm(void);
void op_write_pgm(void);
void op_read_bin(void);
void op_write_bin(void);

#endif // OPS_H
