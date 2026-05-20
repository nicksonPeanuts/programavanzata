/*
 * Nome: Nicolo
 * Cognome: Rossi
 * Matricola: 123456
 */

#include "tensor.h"
#include <stdlib.h>
#include <sys/mman.h>

int get_num_elements(Tensor *t) {
    int n = 1;
    for (int i = 0; i < t->ndim; i++) {
        n *= t->shape[i];
    }
    return n;
}

Tensor* create_tensor(int ndim, int32_t *shape) {
    Tensor *t = malloc(sizeof(Tensor));
    t->ndim = ndim;
    int n = 1;
    for (int i = 0; i < ndim; i++) {
        t->shape[i] = shape[i];
        n *= shape[i];
    }
    t->data = malloc(n * sizeof(float));
    t->data_ref_count = malloc(sizeof(int));
    *(t->data_ref_count) = 1;
    t->ref_count = 1;
    t->is_mmap = false;
    return t;
}

void retain_tensor(Tensor *t) {
    t->ref_count++;
}

void release_tensor(Tensor *t) {
    t->ref_count--;
    if (t->ref_count <= 0) {
        (*(t->data_ref_count))--;
        if (*(t->data_ref_count) <= 0) {
            if (t->is_mmap) {
                munmap(t->mmap_ptr, t->mmap_size);
            } else {
                free(t->data);
            }
            free(t->data_ref_count);
        }
        free(t);
    }
}
