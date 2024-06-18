#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

#define BOOL int
#define TRUE 1
#define FALSE 0

static void daemon_init(void)
{
    pid_t   pid;

    pid = fork();
    if(pid != 0)
        exit(0);

    setsid();
    signal(SIGHUP,SIG_IGN);

    pid = fork();
    if(pid != 0)
        exit(0);
}

static void StopSuricata(pid_t pid)
{
    int status;
    if(pid > 0)
    {
        printf("Try to stop Suricata(pid:%d)", pid);
        kill(pid, SIGTERM);
        pid = waitpid(pid, &status, 0);
        printf("Suricata(pid:%d) is stopped", pid);
    }
}

static pid_t StartSuricata()
{
    pid_t pid;

    pid = fork();
    if(pid == 0)
    {
        // char para[64] = { 0 };
        printf("[===>>>]Starting Suricata......");
        // snprintf(para, 64, "-c /opt/firewall/ips/conf/netvine_engine.yaml --af-packet");
        execl("/opt/firewall/ips/bin/netvine_engine", "netvine_engine", "-c", "/opt/firewall/ips/conf/netvine_engine.yaml", "--af-packet", NULL);
        exit(-1);
    }

    return pid;
}

static BOOL bExit=FALSE;
static void exit_notify(int signo)
{
    bExit = TRUE;
    signal(SIGTERM, exit_notify);	
}

int main (int argc, char *argv[])
{
    int SuricataPid = 0, pid = 0, status = 0;

    daemon_init();

    signal(SIGHUP, SIG_IGN);
    signal(SIGUSR1, SIG_IGN);
    signal(SIGUSR2, SIG_IGN);
    signal(SIGTERM, exit_notify);

    while(TRUE)
    {
        if(bExit)
        {
            printf("[===>>>]monitor exiting ......\n\n");
            StopSuricata(SuricataPid);
            exit(0);
        }

        if(SuricataPid == 0)
            SuricataPid = StartSuricata();
        else
        {
            pid = waitpid(SuricataPid, &status, WNOHANG);
            if(pid == SuricataPid)
            {
                printf("[===>>>]restarting Suricata......\n");
                SuricataPid = StartSuricata();
            }
        }

        sleep(1);
    }

    return 0;
}

