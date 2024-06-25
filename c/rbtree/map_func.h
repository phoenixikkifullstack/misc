#ifndef _MAP_FUNC_H
#define _MAP_FUNC_H

#include "rbtree.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

struct _map_info_struct
{
	int    id;
	char * ptv;
};

struct map {
    struct rb_node node;
    char *key;
    struct _map_info_struct val;
};

struct _hash_map {
    struct rb_node node;
    unsigned int key;
    int          caplen;
    time_t       stTime;
};

typedef struct map map_t;
typedef struct _hash_map hash_map_t;
typedef struct rb_root root_t;
typedef struct rb_node rb_node_t;

map_t *map_get(root_t *root, char *str);
int    map_put(root_t *root, char* key, struct _map_info_struct * val);
map_t *map_first(root_t *tree);
map_t *map_next(rb_node_t *node);
void   map_free(map_t *node);

hash_map_t *hash_map_get(root_t *root, unsigned int key);
int       hash_map_put(root_t *root, unsigned int key, int caplen);
hash_map_t *hash_map_first(root_t *tree);
hash_map_t *hash_map_next(rb_node_t *node);
void      hash_map_free(hash_map_t *node);

#endif  //_MAP_H

/* vim: set ts=4 sw=4 sts=4 tw=100 */
