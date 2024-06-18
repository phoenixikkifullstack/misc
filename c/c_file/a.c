#include <stdio.h>
#include <string.h>

int main(int argc,char** argv)
{
    FILE *fp = NULL;
    char load_file[] = "./eve.json";
    char line[8196];
    int n = 0;

    fp = fopen(load_file,"r");
    if(!fp) {
        printf("can not load file!");
        return 1;
    }

    while(!feof(fp)) {
        memset(line, 0, sizeof(line));
        fgets(line, sizeof(line), fp);
        ++n;
    }

    // printf("%s",line);
    printf("n:%d\n", n);
    fclose(fp);
    return 0;
}
