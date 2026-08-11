#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>





/**
 * ISTRUZIONI PER L'ESERCIZIO:
 * 1. M è n x n (row-major)
 * 2. K è m x m (row-major)
 * 3. Mout è (n-m) x (n-m) (row-major)
 * 4. Implementa Mout[i][j] = sum(M[i+h][j+k] * K[h][k])
 * 5. Usa OpenMP per parallelizzare il calcolo.
 */

void f(float *M, float *K, int n, int m, float *Mout) {
    
    // Scrivi qui il tuo codice...
    // Suggerimento: pensa a quale ciclo è più conveniente parallelizzare.
#pragma omp parallel for collapse(2)
    for(int i = 0; i < (n-m); i++){
        for(int j = 0; j < (n-m); j++){
            
            float acc = 0;

            for(int h = 0; h < m; h++){
                for(int k = 0; k <m; k++){
                    acc += M[(i + h) * n + (j + k)] * K[h * m + k];
                }
            }
            Mout[i*(n-m) + j] = acc; 
        }
    }
    
}


int main(int argc, char*argv)
{

    printf("THREAD TESTER");

#pragma omp parallel
    {
        int n_thread = omp_get_thread_num();
        printf("saluti dal thread %d\n", n_thread);
    }


}
