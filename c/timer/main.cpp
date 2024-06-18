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
#endif

static int count = 0;
static struct itimerval oldtv;

void set_timer()
{
    struct itimerval itv;//结构体的定义在Timer.h
    itv.it_interval.tv_sec = 1;
    itv.it_interval.tv_usec = 60;
    itv.it_value.tv_sec = 1;
    itv.it_value.tv_usec = 0;
    setitimer(ITIMER_REAL, &itv, &oldtv);//向内核注册一个timer信号
}

void signal_handler(int m)
{
    count ++;
    printf("%d\n", count);
}

int main()
{
    /*内核收到setitemer时触发的信号,会激活SIGALRM
      signal这个函数是信号量注册,只要收到SIGALRM就会调用signal_handler
     */
    signal(SIGALRM, signal_handler);
    set_timer();

#if 1
    while(count < 10000);
#else
    while(count < 10000)
    {
        sleep(5);
        printf("verify the sleep func...\n");
    }
#endif

    exit(0);
    return 1;
}

