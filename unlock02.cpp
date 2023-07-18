#include<iostream>
#include<filesystem>
#include<vector>
#include<string>
#include<Windows.h>

using namespace std;
namespace fs = std::filesystem;

vector<string> getFiles(const string& self_name)
{
	string current_dir = fs::current_path().string();
	vector<string> files;
	for (const auto& file_path : fs::recursive_directory_iterator(current_dir))
	{
		if (!(file_path.is_directory()) and (file_path.path().string() != self_name) and (file_path.path().filename().string() != "ahh.exe"))
		{
			files.push_back(file_path.path().string());
		}
	}
	return files;
}

int main(int argc, char* argv[])
{
	string self_name = fs::path(argv[0]).string();
	vector<string> files = getFiles(self_name);
	string cmd;
	string temp1;
	string temp2;
	for (string file : files)
	{
		temp1 = file + ".txt";
		rename(file.c_str(), temp1.c_str());
		cout << file << "convert 1" << endl;
	}
	Sleep(100);
	for (string file : files)
	{
		temp1 = file + ".txt";
		temp2 = file + ".temp";
		cmd = "move \"" + temp1 + "\" \"" + temp2 + "\" >nul";
		system(cmd.c_str());
		cout << file << "convert 2" << endl;
	}
	Sleep(100);
	for (string file : files)
	{
		temp2 = file + ".temp";
		rename(temp2.c_str(), file.c_str());
		cout << file << "convert 3" << endl;
	}
}
