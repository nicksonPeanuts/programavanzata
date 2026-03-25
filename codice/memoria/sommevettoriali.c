#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h> // informazioni aggiuntive
#include <sys/mman.h> // per mmap
#include <sys/stat.h> // per stat
#include <immintrin.h>


int somma(int *v, int len){
    int sum = 0;
    for(int i = 0; i < len; i++){
        sum += v[i];
    }
    return sum;
}

int sum_vector_sidm(int *vec, int len)
{
    __v8si sumv = {0,0,0,0,0,0,0,0};

    int i;
    for(i =0; i+7 < len; i++){
        // dimmi dove si trova l'indirizzo dell'iesimo elemento del vettore
        // interpretalo come puntatore di un blocco di 8 interi alla volta
        // caricamelo in x
        __v8si x = *(__v8si *) &vec[i];
        sumv += x;
    }

    int sum = sumv[0] + sumv[1] + sumv[2] + sumv[3] + sumv[4] + sumv[5] + sumv[6] + sumv[7];

    for(; i < len; i++){
        sum += vec[i];
    }
    return sum;
}


#define N 1000

int main(int argc, char *argv[])
{
    // PROF DEVE CARICARE CODICE
    return 0;
}