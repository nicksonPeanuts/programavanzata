#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  int sum = 0;
  #pragma omp parallel for

  // ci fosse solo parallel ogni thread esegue il for, molte stampe in più
  for (int i = 0; i < 20; i++) {
    printf("Iterazioni %d\n", i);
  }

  return 0;
}
