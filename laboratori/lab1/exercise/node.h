#ifndef node_h
#define node_h
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>

// definiamo il nodo

struct _tree_node {
  int key;
  void *value;
  struct _tree_node *left;
  struct _tree_node *right;
  struct _tree_node *parent;
};

// puntatore alla struttura, il tipo t node
typedef struct _tree_node *t_node;

t_node make_t_node (void);
void delete_t_node (t_node tmp);
#endif