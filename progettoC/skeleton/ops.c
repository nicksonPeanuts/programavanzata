/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#include "ops.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

void op_binary(char op) {
    // TODO: Pop di due tensori, controllo validita', computazione parallela (+, -, *, <, >, =, &, |, m, M), push risultato
}

void op_not() {
    // TODO: Negazione logica su tutti i valori di un tensore
}

void op_select() {
    // TODO: Selezione condizionale tra due tensori usando un tensore maschera
}

void op_matmul() {
    // TODO: Moltiplicazione tra matrici a@b con due for innestati e OpenMP
}

void op_dot() {
    // TODO: Prodotto scalare tra due vettori (riduzione OpenMP)
}

void op_conv() {
    // TODO: Convoluzione 2D applicando un kernel k ad una matrice a, con padding zero
}

void op_reshape() {
    // TODO: Modifica logica delle dimensioni del tensore sfruttando il reference counting
}

void op_ravel() {
    // TODO: Conversione in tensore 1D (appiattimento) sfruttando il reference counting
}

void op_shape() {
    // TODO: Estrazione della shape sottoforma di tensore 1D
}

void op_rand() {
    // TODO: Generazione di un tensore con numeri casuali [0, 1]
}

void op_relu() {
    // TODO: Applica Rectified Linear Unit, ponendo a 0 i negativi
}

void op_sum() {
    // TODO: Somma totale di tutti gli elementi
}

void op_fill() {
    // TODO: Generazione di tensore di forma s ripetendo i valori di v
}

void op_print() {
    // TODO: Stampa formato Tensor(shape=[...], data=[...])
}

void op_dup() {
    // TODO: Duplicazione del top element con incremento del ref_count
}

void op_swap() {
    // TODO: Inversione dei primi due elementi dello stack
}

void op_over() {
    // TODO: Replica del secondo elemento in cima allo stack
}

void op_drop() {
    // TODO: Pop e deallocazione/decremento del top element
}

void op_read_pgm() {
    // TODO: Lettura file PGM (formato P5 binario), push tensore [0, 1]
}

void op_write_pgm() {
    // TODO: Scrittura file PGM binario (rimappando da [0, 1] a [0, 255])
}

void op_read_bin() {
    // TODO: Lettura tensore custom binario allocato via mmap (nessuna copia, ma riferimenti condivisi a PROT_READ)
}

void op_write_bin() {
    // TODO: Scrittura tensore su disco custom padding garantito 64 bytes
}
