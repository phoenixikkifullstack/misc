#include <unistd.h>
#include <stdio.h>
#include <pthread.h>
#include <map>
#include <string>

using namespace std;
#define THREADS_MAX 3

// static long unsigned int map_size = 0;
static map<string,int> g_file_map;

void *map_write_func_0(void *args)
{
    auto i = 0;
    // for (auto i = 0; i < 5000; i++)
    while(1)
    {
        char str[32] = {0};
        snprintf(str, sizeof(str), "maptest_%08d", i);
        g_file_map.insert(make_pair(str, i));
        i++;
        // printf("[write][0][==>>]str:%s\n", str);
        // sleep(1);
    }
    printf("Write [0], DONE\n");
    return NULL;
}

void *map_write_func_1(void *args)
{
    for (auto i = 5000; i < 10000; i++)
    {
        char str[32] = {0};
        snprintf(str, sizeof(str), "maptest_%08d", i);
        g_file_map.insert(make_pair(str, i));
        // printf("[write][1][==>>]str:%s\n", str);
        // sleep(1);
    }
    printf("Write [1], DONE\n");
    return NULL;
}

static int index = 0;
void *map_read_func_0(void *args)
{
#if 1
    // static int index = 0;
    for (;;)
    {
        map<string,int>::iterator it;
        map<string,int>::iterator it_temp;
        if (!g_file_map.empty())
        {
            for (it = g_file_map.begin(); it != g_file_map.end();)
            {
                it_temp = it;
                // printf("[>>>>>>><<<<<<<][Read][0][==>>]i:%08d,map<%s,%d>\n", i++, it->first.c_str(), it->second);
                if (index % 5000 == 0)
                    printf("[>>>>>>><<<<<<<][Read][0][==>>]index:%08d,map<%s,%d>\n", index, it_temp->first.c_str(), it_temp->second);
                index++;
                it++;
                g_file_map.erase(it_temp);
            }
        }
#if 0
        if (i >= 10000)
            break;
#endif
        sleep(1);
        // usleep(60);
    }
#else
    sleep(100000);
#endif
    return NULL;
}

int main(int argc, char *argv[])
{
    pthread_t tids[THREADS_MAX];

    pthread_create(&tids[0], NULL, &map_write_func_0, NULL);
//    pthread_create(&tids[1], NULL, &map_write_func_1, NULL);
    pthread_create(&tids[2], NULL, &map_read_func_0, NULL);

    pthread_join(tids[0], NULL);
//    pthread_join(tids[1], NULL);
    pthread_join(tids[2], NULL);

    return 0;
}

