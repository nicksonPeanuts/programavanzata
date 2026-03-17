#ifndef bst_h
#define bst_h

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>

#include "node.h"


// definiamo albero, con un puntatore alla radice dell'albero
struct _bst {
  t_node root;
};

typedef struct _bst *bst;

// Prototipi delle funzioni
t_node make_t_node(void);
void delete_t_node(t_node tmp);
bst make_bst(void);
void delete_bst(bst t);
void bst_insert(bst t, t_node n);
int bst_depth(bst t);

#endif