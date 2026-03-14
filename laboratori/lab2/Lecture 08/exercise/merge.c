#include "merge.h"

void merge(int * v1, int n1, int * v2, int n2, int * results)
{
  // TODO
  // inizializzimo i due indici
  int i = 0;
  int j = 0;
  int tot = n1 + n2;
  
  // passo fondamentale dell'algoritmo di merge
  while(i < n1 || j < n2)
  {
    if(v1[i] < v2[j]){
      results[i] = v1[i];
      i++;
    }else{
      results[i] = v2[j];
      j++;
    }
  }

  // finito il tutto mettiamo il resto del vettore in result
  if(i >= n1){

  }
}

void merge_branchless(int * v1, int n1, int * v2, int n2, int * results)
{
  // TODO
  
}
