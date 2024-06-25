#include "map_func.h"

#define LOG_PRFIX   "[==>>] "
static root_t rt = RB_ROOT;
// int    map_put(root_t *root, char* key, struct _map_info_struct * val);

int main(void)
{
    int rv = 0;
    // struct _map_info_struct * v = calloc(1, sizeof(struct _map_info_struct));
    struct _map_info_struct v = { .id   = 1, .ptv  = NULL};
    rv = map_put(&rt, "hello", &v);
    if (!rv)
        printf(LOG_PRFIX "map_put failed, check your code plz...\n");
    else
        printf(LOG_PRFIX "map_put succeed...\n");

    map_t *r1 = map_get(&rt, "hello");
    if (r1)
        printf(LOG_PRFIX "key:[%s], id:[%d], ptv:[%p]\n", r1->key, r1->val.id, r1->val.ptv);

    return 0;
}