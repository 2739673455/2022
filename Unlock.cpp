#include <iostream>
#include<string>

int main(int argc, char * argv[])
{
    using namespace std;
    string source_file, dest_file;
    source_file = argv[1];
    dest_file = argv[2];
    rename(source_file.c_str(), dest_file.c_str());
    return 0;
}
