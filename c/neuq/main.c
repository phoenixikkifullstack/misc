#include "async_queue.h"
#include <stdio.h>
#include <stdlib.h>

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
