#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h> // informazioni aggiuntive
#include <sys/mman.h> // per mmap
#include <sys/stat.h> // per stat
#include <unistd.h>


void write_vector(int len)
{
    FILE *fd = fopen("mmap_vector_demo", "w+");

    // file descriptor
    int fdnum = fileno(fd);
    // il file non esiste, quidni non si può mappare
    // sistemiamo

    ftruncate(fdnum, len * sizeof(int));

    // mappiamo il mappabile
    int *data = mmap((void *)0, len * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, fdnum, 0);

    for(int i = 0; i < len; i++){
        data[i] = i;
    }   

    // puliamo la cucina
    munmap(data, len * sizeof(int));
    fclose(fd);
}


void read_vector(int len)
{
    FILE *fd = fopen("mmap_vector_demo", "r+");

    // file descriptor
    int fdnum = fileno(fd);
    // il file non esiste, quidni non si può mappare
    // sistemiamo

    ftruncate(fdnum, len * sizeof(int));

    // mappiamo il mappabile
    int *data = mmap((void *)0, len * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, fdnum, 0);

    int sum = 0;
    for(int i = 0; i < len; i++){
        sum +=data[i];
    }   
    printf("Somma dei valori nel file è: %d\n", sum);
    // puliamo la cucina
    munmap(data, len * sizeof(int));
    fclose(fd);
}


int main(int argc, char *argv[])
{
    const int len = 10000;
    write_vector(len);
    read_vector(len);

    return 0;
}