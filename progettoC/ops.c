/*
 * Nome: Nicolo
 * Cognome: Rossi
 * Matricola: 123456
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
    Tensor *a = pop_tensor(); // Top
    Tensor *b = pop_tensor(); // Sotto Top
    if (a->ndim != b->ndim) {
        fprintf(stderr, "Errore: dimensioni incompatibili in %c\n", op);
        exit(1);
    }
    for (int i = 0; i < a->ndim; i++) {
        if (a->shape[i] != b->shape[i]) {
            fprintf(stderr, "Errore: shape incompatibili in %c\n", op);
            exit(1);
        }
    }
    Tensor *c = create_tensor(a->ndim, a->shape);
    int n = get_num_elements(a);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        float va = a->data[i];
        float vb = b->data[i];
        if (op == '+') c->data[i] = va + vb;
        else if (op == '-') c->data[i] = va - vb;
        else if (op == '*') c->data[i] = va * vb;
        else if (op == '<') c->data[i] = (va < vb) ? 1.0f : 0.0f;
        else if (op == '>') c->data[i] = (va > vb) ? 1.0f : 0.0f;
        else if (op == '=') c->data[i] = (va == vb) ? 1.0f : 0.0f;
        else if (op == '&') c->data[i] = (va != 0.0f && vb != 0.0f) ? 1.0f : 0.0f;
        else if (op == '|') c->data[i] = (va != 0.0f || vb != 0.0f) ? 1.0f : 0.0f;
        else if (op == 'm') c->data[i] = (va < vb) ? va : vb;
        else if (op == 'M') c->data[i] = (va > vb) ? va : vb;
    }
    release_tensor(a);
    release_tensor(b);
    push_tensor(c);
}

void op_not() {
    Tensor *a = pop_tensor();
    Tensor *c = create_tensor(a->ndim, a->shape);
    int n = get_num_elements(a);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        c->data[i] = (a->data[i] == 0.0f) ? 1.0f : 0.0f;
    }
    release_tensor(a);
    push_tensor(c);
}

void op_select() {
    Tensor *m = pop_tensor(); // Top
    Tensor *a = pop_tensor();
    Tensor *b = pop_tensor();
    Tensor *c = create_tensor(a->ndim, a->shape);
    int n = get_num_elements(a);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        c->data[i] = (m->data[i] == 1.0f) ? a->data[i] : b->data[i];
    }
    release_tensor(m);
    release_tensor(a);
    release_tensor(b);
    push_tensor(c);
}

void op_matmul() {
    Tensor *a = pop_tensor(); // Top (sinistra)
    Tensor *b = pop_tensor(); // Sotto Top (destra)
    if (a->ndim != 2 || b->ndim != 2 || a->shape[1] != b->shape[0]) {
        fprintf(stderr, "Errore: shape incompatibili per matmul\n");
        exit(1);
    }
    int32_t shape[2] = {a->shape[0], b->shape[1]};
    Tensor *c = create_tensor(2, shape);
    int M = a->shape[0];
    int K = a->shape[1];
    int N = b->shape[1];
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            float sum = 0.0f;
            for (int k = 0; k < K; k++) {
                sum += a->data[i * K + k] * b->data[k * N + j];
            }
            c->data[i * N + j] = sum;
        }
    }
    release_tensor(a);
    release_tensor(b);
    push_tensor(c);
}

void op_dot() {
    Tensor *a = pop_tensor();
    Tensor *b = pop_tensor();
    if (a->ndim != 1 || b->ndim != 1 || a->shape[0] != b->shape[0]) {
        fprintf(stderr, "Errore: shape incompatibili per dot\n");
        exit(1);
    }
    int32_t shape[1] = {1};
    Tensor *c = create_tensor(1, shape);
    int n = a->shape[0];
    float sum = 0.0f;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += a->data[i] * b->data[i];
    }
    c->data[0] = sum;
    release_tensor(a);
    release_tensor(b);
    push_tensor(c);
}

void op_conv() {
    Tensor *k = pop_tensor(); // Top (kernel)
    Tensor *a = pop_tensor(); // Sotto Top (immagine)
    if (a->ndim != 2 || k->ndim != 2) {
        fprintf(stderr, "Errore: convoluzione richiede tensori 2D\n");
        exit(1);
    }
    Tensor *c = create_tensor(2, a->shape);
    int H = a->shape[0];
    int W = a->shape[1];
    int KH = k->shape[0];
    int KW = k->shape[1];
    int padH = KH / 2;
    int padW = KW / 2;
    
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; j++) {
            float sum = 0.0f;
            for (int ki = 0; ki < KH; ki++) {
                for (int kj = 0; kj < KW; kj++) {
                    int r = i + ki - padH;
                    int c_idx = j + kj - padW;
                    if (r >= 0 && r < H && c_idx >= 0 && c_idx < W) {
                        sum += a->data[r * W + c_idx] * k->data[ki * KW + kj];
                    }
                }
            }
            c->data[i * W + j] = sum;
        }
    }
    release_tensor(a);
    release_tensor(k);
    push_tensor(c);
}

void op_reshape() {
    Tensor *s = pop_tensor(); // Top (shape)
    Tensor *a = pop_tensor(); // Sotto Top (tensor da modificare)
    if (s->ndim != 1 || s->shape[0] > MAX_DIM || s->shape[0] < 1) {
        fprintf(stderr, "Errore: tensore forma non valido per reshape\n");
        exit(1);
    }
    int new_n = 1;
    int32_t new_shape[MAX_DIM];
    for(int i = 0; i < s->shape[0]; i++) {
        new_shape[i] = (int32_t)s->data[i];
        new_n *= new_shape[i];
    }
    if (new_n != get_num_elements(a)) {
        fprintf(stderr, "Errore: numero di elementi incompatibile in reshape\n");
        exit(1);
    }
    
    Tensor *t = malloc(sizeof(Tensor));
    t->ndim = s->shape[0];
    for (int i = 0; i < t->ndim; i++) {
        t->shape[i] = new_shape[i];
    }
    t->data = a->data;
    t->data_ref_count = a->data_ref_count;
    (*(t->data_ref_count))++; // Riferimento al data incrementato
    t->ref_count = 1;
    t->is_mmap = a->is_mmap;
    t->mmap_size = a->mmap_size;
    t->mmap_ptr = a->mmap_ptr;
    
    release_tensor(a);
    release_tensor(s);
    push_tensor(t);
}

void op_ravel() {
    Tensor *a = pop_tensor();
    Tensor *t = malloc(sizeof(Tensor));
    t->ndim = 1;
    t->shape[0] = get_num_elements(a);
    t->data = a->data;
    t->data_ref_count = a->data_ref_count;
    (*(t->data_ref_count))++;
    t->ref_count = 1;
    t->is_mmap = a->is_mmap;
    t->mmap_size = a->mmap_size;
    t->mmap_ptr = a->mmap_ptr;
    
    release_tensor(a);
    push_tensor(t);
}

void op_shape() {
    Tensor *a = pop_tensor();
    int32_t shape[1] = {a->ndim};
    Tensor *s = create_tensor(1, shape);
    for (int i = 0; i < a->ndim; i++) {
        s->data[i] = (float)a->shape[i];
    }
    release_tensor(a);
    push_tensor(s);
}

void op_rand() {
    Tensor *s = pop_tensor();
    if (s->ndim != 1 || s->shape[0] > MAX_DIM || s->shape[0] < 1) {
        fprintf(stderr, "Errore: shape invalida in rand\n");
        exit(1);
    }
    int32_t shape[MAX_DIM];
    for (int i = 0; i < s->shape[0]; i++) {
        shape[i] = (int32_t)s->data[i];
    }
    Tensor *a = create_tensor(s->shape[0], shape);
    int n = get_num_elements(a);
    for (int i = 0; i < n; i++) {
        a->data[i] = (float)rand() / (float)RAND_MAX;
    }
    release_tensor(s);
    push_tensor(a);
}

void op_relu() {
    Tensor *a = pop_tensor();
    Tensor *c = create_tensor(a->ndim, a->shape);
    int n = get_num_elements(a);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        c->data[i] = (a->data[i] < 0.0f) ? 0.0f : a->data[i];
    }
    release_tensor(a);
    push_tensor(c);
}

void op_sum() {
    Tensor *a = pop_tensor();
    int32_t shape[1] = {1};
    Tensor *c = create_tensor(1, shape);
    int n = get_num_elements(a);
    float sum = 0.0f;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        sum += a->data[i];
    }
    c->data[0] = sum;
    release_tensor(a);
    push_tensor(c);
}

void op_fill() {
    Tensor *v = pop_tensor(); // Top (valori)
    Tensor *s = pop_tensor(); // Sotto Top (shape)
    if (s->ndim != 1 || s->shape[0] > MAX_DIM || s->shape[0] < 1) {
        fprintf(stderr, "Errore: forma non valida in fill\n");
        exit(1);
    }
    int32_t shape[MAX_DIM];
    for (int i = 0; i < s->shape[0]; i++) {
        shape[i] = (int32_t)s->data[i];
    }
    Tensor *a = create_tensor(s->shape[0], shape);
    int n = get_num_elements(a);
    int vn = get_num_elements(v);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        a->data[i] = v->data[i % vn];
    }
    release_tensor(v);
    release_tensor(s);
    push_tensor(a);
}

void op_print() {
    Tensor *a = pop_tensor();
    printf("Tensor(shape=[");
    for(int i = 0; i < a->ndim; i++) {
        printf("%d", a->shape[i]);
        if(i < a->ndim - 1) printf(", ");
    }
    printf("], data=[");
    int n = get_num_elements(a);
    for(int i = 0; i < n; i++) {
        printf("%g", a->data[i]);
        if(i < n - 1) printf(", ");
    }
    printf("])\n");
    release_tensor(a);
}

void op_dup() {
    StackElement e = pop();
    if (e.type == TENSOR) {
        retain_tensor(e.tensor);
        push_tensor(e.tensor);
        push_tensor(e.tensor);
    } else {
        char *s = strdup(e.string);
        push_string(e.string);
        push_string(s);
    }
}

void op_swap() {
    StackElement a = pop();
    StackElement b = pop();
    if (a.type == TENSOR) push_tensor(a.tensor); else push_string(a.string);
    if (b.type == TENSOR) push_tensor(b.tensor); else push_string(b.string);
}

void op_over() {
    StackElement a = pop();
    StackElement b = pop();
    if (b.type == TENSOR) {
        retain_tensor(b.tensor);
        push_tensor(b.tensor);
    } else push_string(strdup(b.string));
    
    if (a.type == TENSOR) push_tensor(a.tensor); else push_string(a.string);
    
    if (b.type == TENSOR) push_tensor(b.tensor); else push_string(strdup(b.string));
}

void op_drop() {
    StackElement a = pop();
    if (a.type == TENSOR) release_tensor(a.tensor);
    else free(a.string);
}

void op_read_pgm() {
    char *filename = pop_string();
    FILE *f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Errore: impossibile aprire %s\n", filename);
        exit(1);
    }
    char magic[3];
    int res = fscanf(f, "%2s", magic);
    if (res <= 0 || strcmp(magic, "P5") != 0) {
        fprintf(stderr, "Errore: file %s non è un PGM valido\n", filename);
        exit(1);
    }
    int width, height, maxval;
    res = fscanf(f, "%d %d %d", &width, &height, &maxval);
    if (res <= 0) {
        fprintf(stderr, "Errore lettura header PGM\n");
        exit(1);
    }
    fgetc(f); // Ignora newline residuo
    
    int32_t shape[2] = {height, width};
    Tensor *t = create_tensor(2, shape);
    unsigned char *img = malloc(width * height);
    if (fread(img, 1, width * height, f) != (size_t)(width * height)) {
        fprintf(stderr, "Attenzione: lettura PGM incompleta\n");
    }
    fclose(f);
    
    int n = width * height;
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        t->data[i] = (float)img[i] / (float)maxval;
    }
    free(img);
    free(filename);
    push_tensor(t);
}

void op_write_pgm() {
    char *filename = pop_string();
    Tensor *a = pop_tensor();
    if (a->ndim != 2) {
        fprintf(stderr, "Errore: PGM output richiede un tensore 2D\n");
        exit(1);
    }
    FILE *f = fopen(filename, "wb");
    if (!f) {
        fprintf(stderr, "Errore: impossibile aprire %s\n", filename);
        exit(1);
    }
    int height = a->shape[0];
    int width = a->shape[1];
    fprintf(f, "P5\n%d %d\n255\n", width, height);
    
    int n = width * height;
    unsigned char *img = malloc(n);
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        float v = a->data[i];
        if (v < 0.0f) v = 0.0f;
        if (v > 1.0f) v = 1.0f;
        img[i] = (unsigned char)(v * 255.0f);
    }
    fwrite(img, 1, n, f);
    fclose(f);
    free(img);
    free(filename);
    release_tensor(a);
}

void op_read_bin() {
    char *filename = pop_string();
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "Errore: impossibile aprire %s\n", filename);
        exit(1);
    }
    struct stat st;
    fstat(fd, &st);
    void *mmap_ptr = mmap(NULL, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
    close(fd);
    if (mmap_ptr == MAP_FAILED) {
        fprintf(stderr, "Errore: mmap fallita\n");
        exit(1);
    }
    struct on_disk_tensor *odt = (struct on_disk_tensor*)mmap_ptr;
    Tensor *t = malloc(sizeof(Tensor));
    t->ndim = odt->ndim;
    for (int i = 0; i < t->ndim; i++) {
        t->shape[i] = odt->shape[i];
    }
    t->data = (float*)((char*)mmap_ptr + odt->data_offset);
    t->data_ref_count = malloc(sizeof(int));
    *(t->data_ref_count) = 1;
    t->ref_count = 1;
    t->is_mmap = true;
    t->mmap_size = st.st_size;
    t->mmap_ptr = mmap_ptr;
    free(filename);
    push_tensor(t);
}

void op_write_bin() {
    char *filename = pop_string();
    Tensor *a = pop_tensor();
    FILE *f = fopen(filename, "wb");
    if (!f) {
        fprintf(stderr, "Errore: impossibile aprire %s\n", filename);
        exit(1);
    }
    struct on_disk_tensor odt;
    odt.ndim = a->ndim;
    for (int i = 0; i < MAX_DIM; i++) {
        odt.shape[i] = (i < a->ndim) ? a->shape[i] : 0;
    }
    odt.data_offset = 64;
    fwrite(&odt, sizeof(struct on_disk_tensor), 1, f);
    int padding = 64 - sizeof(struct on_disk_tensor);
    if (padding > 0) {
        char *pad = calloc(padding, 1);
        fwrite(pad, 1, padding, f);
        free(pad);
    }
    int n = get_num_elements(a);
    fwrite(a->data, sizeof(float), n, f);
    fclose(f);
    free(filename);
    release_tensor(a);
}
