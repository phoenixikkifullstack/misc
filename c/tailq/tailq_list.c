#include <stdio.h>
#include <stdlib.h>
// #include <sys/queue.h>
#include "queue.h"
#include <sys/time.h>

/*
    queue.h file get from https://svnweb.freebsd.org/base/head/sys/sys/queue.h
*/
struct QUEUE_ITEM{
    int value;  
    TAILQ_ENTRY(QUEUE_ITEM) entries;
};  
TAILQ_HEAD(headname,QUEUE_ITEM) queue_head;

#define ITEM_NUM 5000000
#define TRAVERSAL 20

int main(int argc,char **argv){
    struct QUEUE_ITEM *item;
    long long totaltime = 0;
    struct timeval start,end;
    long long metric[TRAVERSAL];
    int i = 0;
    
    TAILQ_INIT(&queue_head);
    for(i=1;i<ITEM_NUM;i+=1){
        item=(struct QUEUE_ITEM *)malloc(sizeof(struct QUEUE_ITEM));
        item->value=i;
        TAILQ_INSERT_TAIL(&queue_head, item, entries);
    }
    
    for (i = 0; i < TRAVERSAL; i++)
    {
        gettimeofday(&start,NULL);
        TAILQ_FOREACH(item, &queue_head, entries)
        {
            item->value++;
        }   
        gettimeofday(&end,NULL);
        metric[i] = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec); // get the run time by microsecond
    }
   
    totaltime = 0;
    for (i=0;i<TRAVERSAL;i++)
    {
        totaltime += metric[i];
    }

    printf("TAILQ traversal time is %lld us\n", totaltime/TRAVERSAL);

    for (i = 0; i < TRAVERSAL; i++)
    {
        gettimeofday(&start,NULL);
        TAILQ_FOREACH_REVERSE(item, &queue_head, headname,entries)
        {
            item->value++;
        }   
        gettimeofday(&end,NULL);
        metric[i] = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec); // get the run time by microsecond
    }
    
    totaltime = 0;
    for (i=0;i<TRAVERSAL;i++)
    {
        totaltime += metric[i];
    }
    
    printf("TAILQ reverse traversal time is %lld us\n", totaltime/TRAVERSAL);
    return 0; 
}