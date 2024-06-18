#include <string>
#include <iostream>
#include <fstream>

using namespace std;

string input_file = "/home/cheny/personal_prj/cpp_file/eve.json";
string query;

int i = 0;

int main(int argc, char *argv[]) {
    std::ifstream in(input_file);
    while(getline(in,query)) {
        // cout<<query<<endl;
        ++i;
    }

    cout << "i:" << i << endl;

    return 0;
}
