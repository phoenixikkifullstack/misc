#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/inotify.h>
#include <string.h>
#include <unistd.h>

#include <sys/select.h>

#define EVENT_SIZE  ( sizeof (struct inotify_event) )
#define BUF_LEN     ( 1024 * ( EVENT_SIZE + 16 ) )
#define WATCH_PATH      "/home/cheny/personal_prj/tmp"

#define MAXLEN 1024

char buffer[BUF_LEN];
fd_set set;
fd_set rset;
int check_set[MAXLEN];
int max_fd;
int arrlen = 0;

static void handle_read(int fd)
{
    int length = read( fd, buffer, BUF_LEN );

    if ( length < 0 ) {
        perror( "read" );
    }

    int i = 0;
    while ( i < length ) {
        struct inotify_event *event = ( struct inotify_event * ) &buffer[ i ];
        if ( event->len ) {
            if ( event->mask & IN_CREATE ) {
                if ( event->mask & IN_ISDIR ) {
                    printf( "The directory %s was created.\n", event->name );
                }
                else {
                    printf( "The file %s was created.\n", event->name );
                }
            }
            else if ( event->mask & IN_DELETE ) {
                if ( event->mask & IN_ISDIR ) {
                    printf( "The directory %s was deleted.\n", event->name );
                }
                else {
                    printf( "The file %s was deleted.\n", event->name );
                }
            }
            else if ( event->mask & IN_MODIFY ) {
                if ( event->mask & IN_ISDIR ) {
                    printf( "The directory %s was modified.\n", event->name );
                }
                else {
                    printf( "The file %s was modified. wd:%d\n", event->name ,event->wd);
                }
            }
        }
        i += EVENT_SIZE + event->len;
    }
    memset(buffer, 0, BUF_LEN);
}

static void do_select()
{
    int i = 0;
    while(1)
    {
        set = rset;
        int nready = select(max_fd+1, &set, NULL, NULL, NULL);
        if(nready == -1)
        {
            perror("error select !");
            exit(-1);
        }else if(nready == 0){
            printf("timeout!");
            continue;
        }

        //轮询数据连接
        for(i = 0; i < arrlen; ++i)
        {
            int set_fd = check_set[i];
            if(FD_ISSET(set_fd, &set))
            {
                handle_read(set_fd);
            }
        }
    }
}

static void AddFd(int fd)
{
    FD_SET(fd, &rset);
    check_set[arrlen++] = fd;

    if(max_fd < fd)
        max_fd = fd;
}

int main( int argc, char **argv )
{

    int fd = inotify_init();
    if ( fd < 0 ) {
        perror( "inotify_init" );
    }
    int wd = inotify_add_watch( fd, WATCH_PATH, IN_OPEN | IN_MOVED_TO | IN_MODIFY | IN_CREATE | IN_DELETE );

#if 0
    //也可以直接用fd不用重新inotify_init
    int fd2 = inotify_init();
    int wd2 = inotify_add_watch( fd2, "./tmp1",IN_MODIFY | IN_CREATE | IN_DELETE );
#endif

    //初始化
    FD_ZERO(&rset);
    int i = 0;
    for(i = 0;i < MAXLEN; ++i)
        check_set[i] = -1;
    //添加监控fd
    AddFd(fd);
#if 0
    AddFd(fd2);
#endif

    //select轮询
    do_select();

    inotify_rm_watch(fd,wd);
#if 0
    inotify_rm_watch(fd2,wd2);
#endif
    close(fd);
#if 0
    close(fd2);
#endif

    exit( 0 );
}
