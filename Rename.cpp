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
		if (!(file_path.is_directory()) and file_path.path().string() != self_name)
		{
			files.push_back(file_path.path().string());
		}
	}
	return files;
}

void reName(const string & source_file, const string& dest_file)
{
	int rename_resp;
	rename_resp = rename(source_file.c_str(), dest_file.c_str());
}

void osMove(const string & source_file, const string & dest_file)
{
	
	string cmd = "move \"" + source_file + "\"" + " \"" + dest_file + "\" >nul";
	system(cmd.c_str());
}

void backRename(const string & source_file)
{
	int pos;
	pos = source_file.rfind(".");
	string dest_file = source_file.substr(0,pos);
	rename(source_file.c_str(), dest_file.c_str());
}

int main(int argc, char* argv[])
{
	string self_name = fs::path(argv[0]).string();
	vector<string> files = getFiles(self_name);
	int rename_resp;
	string cmd;
	for (string file : files)
	{
		string temp = file + ".temp";
		rename_resp = rename(file.c_str(), temp.c_str());
		osMove(temp, file);
	}
	return 0;
}
