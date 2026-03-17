#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h> // informazioni aggiuntive
#include <sys/mman.h> // per mmap
#include <sys/stat.h> // per stat





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
    char * data;
    struct stat sbuf;

    // non usiamo open ( basso livello ), ma si può usare 
    // system call uguale, leggermente meno codice eseguito con open... irrilevante per piccole cose
    FILE * f = fopen("mmap_demo", "r+");
    int fd = fileno(f); // ottenere file id
    stat("mmap_demo", &sbuf); // passiamo indirizzo del buffer da riempire
    
    // void 0 -> non importa dove 
    data = mmap((void *)0, sbuf.st_size, PROT_READ, MAP_SHARED, fd, 0);


    for(int i = 0; i < 10; i++){
        printf("%c %c\n", data[i], getc(f));
    }

    // unmappiamo la memoria di quei dati
    munmap(data, sbuf.st_size);
    fclose(f);

    return 0;
}