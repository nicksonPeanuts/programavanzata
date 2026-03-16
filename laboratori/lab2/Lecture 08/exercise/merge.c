#include "merge.h"

void merge(int * v1, int n1, int * v2, int n2, int * results)
{
  // inizializzimo i due indici
  int i = 0;
  int j = 0;
  int h = 0;
  
  // passo fondamentale dell'algoritmo di merge
  while(i < n1 && j < n2)
  {
    if(v1[i] < v2[j]){
      results[h] = v1[i];
      i++;
    }else{
      results[h] = v2[j];
      j++;
    }
    h++;
  }

  // finito il tutto mettiamo il resto del vettore in result
  // v2 tutto già messo
  while(i <= n1){
    results[h] = v1[i];
    i++;
  }
  // v1 tutto già inserito
  while(j <= n1){
    results[h] = v2[j];
    j++;
  }
}

void merge_branchless(int * v1, int n1, int * v2, int n2, int * results)
{
  // TODO
  // implementazione di una merge branchless
  int i, j, k;
  i = 0;
  j = 0;
  k = 0;

  while(i < n1 && j < n2)
  {
    int val_a = v1[i];
    int val_b = v2[j];

    // pick_a = 0 se val_a >= val_b, altrimenti pick_a = 1
    int pick_a = val_a < val_b;
    int pick_b = !pick_a;

    results[k] = pick_a*val_a + pick_b*val_b;
    i += pick_a;
    j += pick_b;

  }

  while(i <= n1){
    results[k] = v1[i];
    i++;
  }
  // v1 tutto già inserito
  while(j <= n1){
    results[k] = v2[j];
    j++;
  }
}
