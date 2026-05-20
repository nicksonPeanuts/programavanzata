#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 1000000

int * random_vector(int len)
{
  int * v = (int *) malloc(len * sizeof(int));
  for (int i = 0; i < len; i++) {
    v[i] = rand() % 100;
  }
  return v;
}

int sum_small_values_branchless(int * v, int len, int threshold)
{
  volatile int sum = 0;
  for (int i = 0; i < len; i++) {
    sum += (v[i] < threshold) * v[i];
  }
  return sum;
}


int main(int argc, char * argv[])
{
  srand(time(NULL));
  int * v = random_vector(SIZE);
  printf("Without branches\n");
  sum_small_values_branchless(v, SIZE, 50);
  return 0;
}
