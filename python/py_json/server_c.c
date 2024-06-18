#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdint.h>
#include <pthread.h>

#define PORT 60000
#define MAX_SIZE 128

static uint32_t count = 0;

/* peek the `count` value */
void *counting_thread(void *arg)
{
    while(1)
    {
        sleep(10);
        printf("[--->>]count:%u\n", count);
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    int sockfd;
    int len = sizeof(struct sockaddr);
    char buf[MAX_SIZE];
    struct sockaddr_in serv_addr;
    pthread_t tid;
    pthread_create(&tid, NULL, counting_thread, NULL);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        printf("创建socket失败！");
        exit(1);
    }

    bzero(&serv_addr, sizeof(struct sockaddr_in));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr("172.16.130.97");

    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(struct sockaddr)) < 0)
    {
        printf("绑定失败");
        exit(1);
    }

    while (1)
    {
        if (recvfrom(sockfd, buf, MAX_SIZE, 0, (struct sockaddr *)&serv_addr, &len) < 0)
        {
            printf("接收失败");
            exit(1);
        }
        else
            count ++;


        // usleep(60);
    }

    close(sockfd);
    pthread_join(tid, NULL);

    return 0;
}

