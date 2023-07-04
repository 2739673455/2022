#include <string>
#include <vector>
#include <filesystem>
#include <fstream>
#include <iostream>

using namespace std;
namespace fs = std::filesystem;

vector<string> getAllFilesIncludeSubfolders(string path) {
    vector<string> files;
    for (const auto& entry : fs::recursive_directory_iterator(path)) {
        if (!entry.is_directory()) {
            files.push_back(entry.path().string());
        }
    }
    return files;
}

void copyFile(string source, string dest) {
    ifstream src(source, ios::binary);
    ofstream dst(dest, ios::binary);
    dst << src.rdbuf();
}

void renameFile(string source, string dest, string currentDir) {
    string cmd = "\"" + currentDir + "\\Unlock.exe\"";
    cmd += " -sourcePath=\"" + source + "\" -destPath=\"" + dest + "\"";
    system(cmd.c_str());

    //2
    string cmd = "move \"" + source + "\" \"" + dest + "\"";
    system(cmd.c_str());

    //3
    string cmd = "ren \"" + source + "\" \"" + dest + "\"";
    system(cmd.c_str());
}

int main(int argc, char* argv[]) {
    string currentDir = fs::current_path().string();
    string selfName = (fs::path(argv[0])).filename().string();
    vector files = getAllFilesIncludeSubfolders(currentDir);
    for (string file : files) {
        if (file.find(selfName) != string::npos || file.find("Unlock.exe") != string::npos) {
           continue;
        }
        string temp = file + ".temp";
        copyFile(file, temp);
        fs::remove(file);

        //3
        file = (fs::path(file)).filename().string();

        renameFile(temp, file, currentDir);
    }
    return 0;
}