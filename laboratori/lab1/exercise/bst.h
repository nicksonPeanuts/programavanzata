#ifndef BST_H
#define BST_H

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

typedef struct _tree_node *t_node;

// definiamo albero
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