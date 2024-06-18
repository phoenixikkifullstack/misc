#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdint.h>

#define PORT 60000
#define MAX_SIZE 128

int main()
{
    int sockfd;
    int fromlen = sizeof(struct sockaddr);
    char buf[MAX_SIZE] = "hello world...hello world...hello world...hello world...";
    struct sockaddr_in serv_addr;
    uint32_t count = 14000000;

    bzero(&serv_addr, sizeof(struct sockaddr_in));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr("172.16.130.97");

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        printf("create socket error!\n");
        exit(1);
    }

    /* worker... */
    while (count--)
    {
        if ( sendto(sockfd, buf, MAX_SIZE, 0,
                    (const struct sockaddr *)&serv_addr,
                    sizeof(struct sockaddr)) < 0 )
        {
            printf("send error!\n");
            exit(1);
        }
    }

    close(sockfd);
    return 0;
}
