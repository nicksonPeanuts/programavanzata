/*
 * Nome: Nicolo
 * Cognome: Rossi
 * Matricola: 123456
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "tensor.h"
#include "stack.h"
#include "ops.h"

/*
 * handle_token: Interpreta il singolo token o smista all'operazione corretta.
 */
void handle_token(char *token, FILE *source) {
    if (strcmp(token, "[") == 0) {
        int cap = 16;
        float *buf = malloc(cap * sizeof(float));
        int count = 0;
        char inner[1024];
        while (fscanf(source, "%s", inner) != EOF) {
            if (strcmp(inner, "]") == 0) break;
            if (count >= cap) {
                cap *= 2;
                buf = realloc(buf, cap * sizeof(float));
            }
            buf[count++] = atof(inner);
        }
        int32_t shape[1] = {count};
        Tensor *t = create_tensor(1, shape);
        memcpy(t->data, buf, count * sizeof(float));
        free(buf);
        push_tensor(t);
    } else if (token[0] == '"') {
        char str[1024];
        strcpy(str, token + 1);
        int len = strlen(str);
        while (len == 0 || str[len - 1] != '"') {
            char temp[1024];
            if (fscanf(source, "%s", temp) == EOF) break;
            strcat(str, " ");
            strcat(str, temp);
            len = strlen(str);
        }
        str[len - 1] = '\0';
        push_string(strdup(str));
    } else if (strcmp(token, "+") == 0) { op_binary('+'); }
    else if (strcmp(token, "-") == 0) { op_binary('-'); }
    else if (strcmp(token, "*") == 0) { op_binary('*'); }
    else if (strcmp(token, "<") == 0) { op_binary('<'); }
    else if (strcmp(token, ">") == 0) { op_binary('>'); }
    else if (strcmp(token, "=") == 0) { op_binary('='); }
    else if (strcmp(token, "&") == 0) { op_binary('&'); }
    else if (strcmp(token, "|") == 0) { op_binary('|'); }
    else if (strcmp(token, "!") == 0) { op_not(); }
    else if (strcmp(token, "$") == 0) { op_select(); }
    else if (strcmp(token, "@") == 0) { op_matmul(); }
    else if (strcmp(token, ".") == 0) { op_dot(); }
    else if (strcmp(token, "c") == 0) { op_conv(); }
    else if (strcmp(token, "r") == 0) { op_reshape(); }
    else if (strcmp(token, "_") == 0) { op_ravel(); }
    else if (strcmp(token, "#") == 0) { op_shape(); }
    else if (strcmp(token, "?") == 0) { op_rand(); }
    else if (strcmp(token, "R") == 0) { op_relu(); }
    else if (strcmp(token, "m") == 0) { op_binary('m'); }
    else if (strcmp(token, "M") == 0) { op_binary('M'); }
    else if (strcmp(token, "S") == 0) { op_sum(); }
    else if (strcmp(token, "f") == 0) { op_fill(); }
    else if (strcmp(token, "p") == 0) { op_print(); }
    else if (strcmp(token, "d") == 0) { op_dup(); }
    else if (strcmp(token, "s") == 0) { op_swap(); }
    else if (strcmp(token, "o") == 0) { op_over(); }
    else if (strcmp(token, "D") == 0) { op_drop(); }
    else if (strcmp(token, "(") == 0) { op_read_pgm(); }
    else if (strcmp(token, ")") == 0) { op_write_pgm(); }
    else if (strcmp(token, "{") == 0) { op_read_bin(); }
    else if (strcmp(token, "}") == 0) { op_write_bin(); }
    else {
        fprintf(stderr, "Errore: token sconosciuto '%s'\n", token);
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    srand(time(NULL));

    if (argc < 2) {
        fprintf(stderr, "Uso: tensorforth <file.tf>\n");
        return 1;
    }

    FILE *source = fopen(argv[1], "r");
    if (!source) {
        fprintf(stderr, "Errore in apertura del file %s\n", argv[1]);
        return 1;
    }

    char token[1024];
    while (fscanf(source, "%s", token) != EOF) {
        handle_token(token, source);
    }

    fclose(source);

    while (stack_size > 0) {
        StackElement e = pop();
        if (e.type == TENSOR) release_tensor(e.tensor);
        else free(e.string);
    }

    return 0;
}