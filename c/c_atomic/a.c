#include <stdio.h>
// #include <unistd.h>
#include <stdint.h>
#include <pthread.h>

#define ATOMIC_TEST 1
#define THREAD_NUM  2

#if 1
#define atomic_inc(x)       __sync_fetch_and_add((x), 1)
#define atomic_dec(x)       __sync_fetch_and_sub((x), 1)
#define atomic_add(x,y)     __sync_fetch_and_add((x), (y))
#define atomic_sub(x,y)     __sync_fetch_and_sub((x), (y))
#else
#define atomic_inc(x)       __atomic_add_fetch((x), 1, 1)
#define atomic_dec(x)       __atomic_sub_fetch((x), 1, 1)
#define atomic_add(x,y)     __atomic_add_fetch((x), (y), 1)
#define atomic_sub(x,y)     __atomic_sub_fetch((x), (y), 1)
#endif


uint32_t atomic_count = 0;

void *thread_func(void *argc)
{
    int i;
    for (i = 0; i < 1000000; i++)
    {
#if ATOMIC_TEST
        atomic_inc(&atomic_count);
#else
        ++atomic_count;
#endif
    }

    return NULL;
}

int main(int argc,char** argv)
{
    int i;
    pthread_t tids[THREAD_NUM];
    for (i = 0; i < THREAD_NUM; i++)
        pthread_create(&tids[i], NULL, thread_func, NULL);

    for (i = 0; i < THREAD_NUM; i++)
        pthread_join(tids[i], NULL);

    printf("[===>>DONE]count:%u\n", (atomic_count));

    return 0;
}
