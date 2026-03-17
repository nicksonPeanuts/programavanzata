#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>

#include "bst.h"
#include "node.h"


t_node make_t_node(void) {
    t_node tmp = (t_node)malloc(sizeof(struct _tree_node));
    if (tmp == NULL) {
      errno = ENOMEM;
      perror("make_t_node");
      return NULL;
    }
    tmp->value = tmp->left = tmp->right = tmp->parent = NULL;
    tmp->key = 0;
    return tmp;
}

void delete_t_node(t_node tmp) {
    if (tmp == NULL) return;
    if (tmp->value != NULL) free(tmp->value);
    free(tmp);
}

bst make_bst(void) {
    bst tmp = (bst)malloc(sizeof(struct _bst));
    if (tmp == NULL) {
        errno = ENOMEM;
        perror("make_bst");
        return NULL;
    }
    tmp->root = NULL;
    return tmp;
}

static void delete_node_cascade(t_node t) {
    if (t == NULL) return;
    delete_node_cascade(t->left);
    delete_node_cascade(t->right);
    delete_t_node(t);
}

void delete_bst(bst t) {
    if (t != NULL) {
      delete_node_cascade(t->root);
      free(t);
    }
}

void bst_insert(bst t, t_node n) {
    if (t == NULL || n == NULL) return;
    if (t->root == NULL) {
        t->root = n;
        return;
    }
    t_node cfr = t->root;
    while (1) {
        if (n->key > cfr->key) {
            if (cfr->right == NULL) {
                cfr->right = n;
                n->parent = cfr;
                break;
            } else cfr = cfr->right;
        } else {
            if (cfr->left == NULL) {
                cfr->left = n;
                n->parent = cfr;
                break;
            } else cfr = cfr->left;
        }
    }
}

static int node_depth(t_node n) {
    if (n == NULL) return 0;
    int l = node_depth(n->left);
    int r = node_depth(n->right);
    return (l > r ? l : r) + 1;
}

int bst_depth(bst t) {
    return (t != NULL) ? node_depth(t->root) : 0;
}