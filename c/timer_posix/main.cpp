#if 0
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <signal.h>
#else
#include <cstdio>
#include <ctime>
#include <csignal>
#include <sys/time.h>
#include <cstdlib>
#include <unistd.h>
#include <cstring>    /* memset */
#endif

#define printf_with_time(format, ...)                                        \
{                                                                            \
    struct timespec spec;                                                    \
    clock_gettime(CLOCK_MONOTONIC, &spec);                                    \
    printf("[%lu:%lu]"format"\n", spec.tv_sec, spec.tv_nsec, ##__VA_ARGS__);\
}


void timer_notify_cb(union sigval val)
{
    // printf_with_time("timer expiration");
    printf("timer expiration\n");

}

int main(void)
{
    /* Variable Definition */
    timer_t id;
    struct timespec spec;
    struct sigevent ent;
    struct itimerspec value;
    struct itimerspec get_val;

    /* Init */
    memset(&ent, 0x00, sizeof(struct sigevent));
    memset(&get_val, 0x00, sizeof(struct itimerspec));

    /* create a timer */
    ent.sigev_notify = SIGEV_THREAD;
    ent.sigev_notify_function = timer_notify_cb;
    // printf_with_time("create timer");
    printf("create timer\n");
    timer_create(CLOCK_REALTIME, &ent, &id);        /* CLOCK_REALTIME */

    /* start a timer */
    clock_gettime(CLOCK_REALTIME, &spec);            /* CLOCK_REALTIME */
    value.it_value.tv_sec = spec.tv_sec + 2;
    value.it_value.tv_nsec = spec.tv_nsec + 0;
    value.it_interval.tv_sec = 1;    /* per second */
    value.it_interval.tv_nsec = 0;
    // printf_with_time("start timer");
    printf("start timer\n");
    timer_settime(id, TIMER_ABSTIME, &value, NULL); /* TIMER_ABSTIME */

    while (1)
    {
        sleep(10);
    }
    // printf_with_time("delete timer");
    printf("delete timer\n");
    timer_delete(id);
    return 0;
}

