#include <stdlib.h>
#include <stdio.h>
  
#define BUF_SIZE 1024
char buf[BUF_SIZE];

int main(void)
{
    FILE * p_file = NULL;

    p_file = popen("pwd", "r");
    if (!p_file) {
        fprintf(stderr, "Erro to popen");
        goto _exit;
    }

    while (fgets(buf, BUF_SIZE, p_file) != NULL) {
        fprintf(stdout, "%s", buf);
    }
    pclose(p_file);

_exit:
    return 0;
}