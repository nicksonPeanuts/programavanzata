#include <stdio.h>
#include <omp.h>
#include <stdlib.h>




int main(int argc, char *argv[])
{
    printf("a\n");

    // facciamo un blocco
    // ordine dei thread dipende dalla schedule del sistema operativo
    #pragma omp parallel
    {
        int n_thread = omp_get_thread_num();
        printf("saluti dal thread %d\n", n_thread);
    }
    printf("d\n");


    // sommiamo elementi di un vettore

    const int n = 1<<20;

    int *v = (int *)malloc(n * sizeof(int));

    for(int i = 0; i < n; i++){
        v[i] = rand() % 100;
    }
    // facciamo una somma in parallelo di tutti gli elementi

    // sum rompe le palle
    int sum = 0;

    #pragma omp parallel
    {
        int n_thread = omp_get_thread_num();
        int slice_size = n/omp_get_num_threads();

        // inizio e fine
        int start = n_thread * slice_size;
        int end = (n_thread+1)*slice_size;

        int partial_sum = 0;

        for(int i = start; i < end; i++){
            // v è definito all'esterno, quindi è usato da TUTTI
            partial_sum += v[i];
        }
        printf("Somma parziale  terminata dal thread: %d con somma parziale: %d\n", n_thread, partial_sum);

        // casini! non si fa
        // sum += partial_sum;
        // correggiamo 
        #pragma omp critical
        {
            sum += partial_sum;
        }
    }
    printf("somma totale: %d\n", sum);

    return 0;
}