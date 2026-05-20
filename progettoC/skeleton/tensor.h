/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#ifndef TENSOR_H
#define TENSOR_H

#include <stdint.h>
#include <stdbool.h>
#include <sys/types.h>

#define MAX_DIM 2

// Formato per l'operazione di I/O binario mmap
struct on_disk_tensor {
    int32_t shape[MAX_DIM];
    int32_t ndim;
    off_t data_offset;
};

// Struttura Tensor principale
typedef struct {
    int32_t shape[MAX_DIM];
    int32_t ndim;
    float *data;
    int *data_ref_count; // Contatore per i riferimenti al buffer di memoria
    int ref_count;       // Contatore per i riferimenti alla struct Tensor stessa
    bool is_mmap;
    size_t mmap_size;
    void *mmap_ptr;
} Tensor;

int get_num_elements(Tensor *t);
Tensor* create_tensor(int ndim, int32_t *shape);
void retain_tensor(Tensor *t);
void release_tensor(Tensor *t);

#endif // TENSOR_H
