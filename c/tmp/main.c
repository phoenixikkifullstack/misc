#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>


static int g_num = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *t_func(void *arg)
{
    while (1)
    {
        pthread_mutex_lock(&mutex);
        g_num += 10;
        sleep(10000);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    pthread_t tids[2];
    pthread_create(&tids[0], NULL, t_func, NULL);

    while (1)
    {
        usleep(1000000);
        g_num += 1;
        printf("[--->>]g_num:%d\n", g_num);
    }

    pthread_join(tids[0], NULL);

    return 0;
}

