#include "async_queue.h"
#include <stdio.h>
#include <stdlib.h>
// #include "utarray.h"
#include "utextend.h"

#if 1
typedef struct _test_t {
    UT_array    *tag;
    // int          k;
} test_t;

int main(void)
{
    test_t *t_list = calloc(1, sizeof(test_t));
    utarray_new(t_list->tag, &ut_ptr_icd);
    // TODO
    for (int i = 0; i < 10; ++i)
    {
        int *p = calloc(1, sizeof(int));
        *p = i * 2 + 1;
        // utarray_push_back(t_list->tag, &p);
        utarray_push_back(t_list->tag, p);
    }

    // utarray_foreach(t_list->tag, int **, p_i)
    utarray_foreach(t_list->tag, int *, p_i)
    {
        // int *p = *p_i;
        int p = *p_i;
        printf("==>> i:[%d]\n", p);
    }
}


#else
static uint64_t qkey_func(void *e)
{
    return 0;
}

static bool qexp_func(void *e)
{
    return false;
}

static void qfree_func(void *e)
{
    return ;
}

int main(void)
{
    int rv = 0;
    (void)rv;

    neu_async_queue_t *aqueue = neu_async_queue_new(qkey_func, qexp_func, qfree_func, 10);
    if (!aqueue)
    {
        printf("neu_async_queue_new failed...\n");
        exit(0);
    }
    // TODO: enqueue/deque samples...

    neu_async_queue_destroy(aqueue);

    return 0;
}
#endif