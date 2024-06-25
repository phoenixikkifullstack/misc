#include "map_func.h"

map_t *map_get(root_t *root, char *str) {
   rb_node_t *node = root->rb_node; 
   while (node) {
        map_t *data = container_of(node, map_t, node);

        //compare between the key with the keys in map
        int cmp = strcmp(str, data->key);
        if (cmp < 0) {
            node = node->rb_left;
        }else if (cmp > 0) {
            node = node->rb_right;
        }else {
            return data;
        }
   }
   return NULL;
}

int map_put(root_t *root, char* key, struct _map_info_struct * val) {
    map_t *data = NULL;
	
    rb_node_t **new_node = &(root->rb_node), *parent = NULL;
    while (*new_node) {
        map_t *this_node = container_of(*new_node, map_t, node);
        int result = strcmp(key, this_node->key);
        parent = *new_node;

        if (result < 0) {
            new_node = &((*new_node)->rb_left);
        }else if (result > 0) {
            new_node = &((*new_node)->rb_right);
        }else {
            memcpy((char *)&(this_node->val), (char *)val, sizeof(struct _map_info_struct));
            return 0;
        }
    }

	data = (map_t*)calloc(1, sizeof(map_t));
	if (data == NULL)
		return 0;
	
    data->key = (char*)calloc(1, (strlen(key)+1)*sizeof(char));
	if (data->key == NULL) {
		free(data);
		return 0;
	}
	
    strcpy(data->key, key);
		
    memcpy((char *)&(data->val), (char *)val, sizeof(struct _map_info_struct));

    rb_link_node(&data->node, parent, new_node);
    rb_insert_color(&data->node, root);

    return 1;
}

map_t *map_first(root_t *tree) {
    rb_node_t *node = rb_first(tree);
    return (rb_entry(node, map_t, node));
}

map_t *map_next(rb_node_t *node) {
    rb_node_t *next =  rb_next(node);
    return rb_entry(next, map_t, node);
}

void map_free(map_t *node){
    if (node != NULL) {
        if (node->key != NULL) {
            free(node->key);
            node->key = NULL;
		}
        free(node);
        node = NULL;
    }
}

hash_map_t *hash_map_get(root_t *root, unsigned int key) {
   rb_node_t *node = root->rb_node; 
   while (node) {
        hash_map_t *data = container_of(node, hash_map_t, node);

        if (data->key > key) {
            node = node->rb_left;
        }else if (data->key < key) {
            node = node->rb_right;
        }else {
            return data;
        }
   }
   return NULL;
}

int hash_map_put(root_t *root, unsigned int key, int caplen) {
    hash_map_t *data = NULL;
	
    rb_node_t **new_node = &(root->rb_node), *parent = NULL;
    while (*new_node) {
        hash_map_t *this_node = container_of(*new_node, hash_map_t, node);
        parent = *new_node;

        if (this_node->key > key) {
            new_node = &((*new_node)->rb_left);
        }else if (this_node->key < key) {
            new_node = &((*new_node)->rb_right);
        }else {
            this_node->caplen = caplen;
            return 0;
        }
    }

	data = (hash_map_t*)calloc(1, sizeof(hash_map_t));
	if (data == NULL)
		return 0;
	
    data->key    = key;
    data->caplen = caplen;

    rb_link_node(&data->node, parent, new_node);
    rb_insert_color(&data->node, root);

    return 1;
}

hash_map_t *hash_map_first(root_t *tree) {
    rb_node_t *node = rb_first(tree);
    return (rb_entry(node, hash_map_t, node));
}

hash_map_t *hash_map_next(rb_node_t *node) {
    rb_node_t *next =  rb_next(node);
    return rb_entry(next, hash_map_t, node);
}

void hash_map_free(hash_map_t *node){
    if (node != NULL) {
        free(node);
        node = NULL;
    }
}