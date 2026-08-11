/*
 * Nome: 
 * Cognome: 
 * Matricola: 
 */

#include "tensor.h"
#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>
#include <string.h>


// torna il numero di elementi del tensore
int get_num_elements(Tensor *t) {
    int num_elements = 1;
    for(int i = 0; i < t->ndim; i++){
        num_elements *= t->shape[i];
    }
    return num_elements;
}


// crea un tensore dato ndim e shape
Tensor* create_tensor(int ndim, int32_t *shape) {
    Tensor *t = (Tensor*)malloc(sizeof(Tensor));
    if (t == NULL) {
        fprintf(stderr, "Errore allocazione memoria\n");
        exit(1);
    }
    
    // 1) inizializzazione
    t->ndim = ndim;
    for (int i = 0; i < ndim; i++) {
        t->shape[i] = shape[i];
    }
    
    int num_elements = get_num_elements(t);
    
    // 2) allocazione dati
    t->data = (float*)malloc(num_elements * sizeof(float));
    if (t->data == NULL) {
        fprintf(stderr, "Errore allocazione memoria\n");
        exit(1);
    }
    
    // 3. ALLOCHIAMO IL CONTATORE (deve essere UN SOLO int!)
    t->data_ref_count = (int*)malloc(sizeof(int));
    if (t->data_ref_count == NULL) {
        fprintf(stderr, "Errore allocazione memoria\n");
        exit(1);
    }
    
    // 4. IMPOSTIAMO I VALORI DI PARTENZA DEI CONTATORI E FLAGS
    *(t->data_ref_count) = 1;  // 1 riferimento ai dati
    t->ref_count = 1;          // 1 riferimento al tensore
    t->is_mmap = false;        // Di default non è da file binario
    
    // 5. RITORNIAMO IL TENSORE CREATO (questo mancava!)
    return t;
}


void retain_tensor(Tensor *t) {
    t->ref_count++;
}

void release_tensor(Tensor *t) {
    t->ref_count--; // Tolgo un riferimento alla "scatola" Tensore
    
    if (t->ref_count == 0) {
        // La scatola Tensore va distrutta. Ma i dati?
        // Riduciamo il contatore dei dati:
        *(t->data_ref_count) -= 1;
        
        // SOLO SE nessuno usa più questi dati li eliminiamo:
        if (*(t->data_ref_count) == 0) {
            if (t->is_mmap) {
                munmap(t->mmap_ptr, t->mmap_size);
            } else {
                free(t->data);
            }
            free(t->data_ref_count); // eliminiamo anche il contatore
        }
        // Infine eliminiamo sempre la "scatola"
        free(t);
    }
}



