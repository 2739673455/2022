#include<string>
#include<vector>
#include<iostream>
#include<filesystem>

using namespace std;
namespace fs = std::filesystem;

vector<string> getFiles(const string& self_name)
{
	string current_dir = fs::current_path().string();
	vector<string> files;
	for (const auto& file_path : fs::recursive_directory_iterator(current_dir))
	{
		if (!(file_path.is_directory()) and (file_path.path().string() != self_name) and (file_path.path().filename().string() != "Unlock.exe"))
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
	for (string file : files)
	{
		string temp = file + ".temp";
		rename(file.c_str(), temp.c_str());
		cmd = "Unlock.exe \"" + temp + "\"" + " \"" + file + "\"";
		system(cmd.c_str());
	}
	return 0;
}
