/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#include "tensor.h"
#include <stdlib.h>
#include <sys/mman.h>

int get_num_elements(Tensor *t) {
    // TODO: Implementare il calcolo del numero totale degli elementi
    return 0;
}

Tensor* create_tensor(int ndim, int32_t *shape) {
    // TODO: Allocare la struct Tensor, i dati float e il data_ref_count
    return NULL;
}

void retain_tensor(Tensor *t) {
    // TODO: Incrementare il reference count del tensore
}

void release_tensor(Tensor *t) {
    // TODO: Decrementare il reference count. Se arriva a zero, gestire la deallocazione (o munmap)
}
