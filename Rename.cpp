#include<iostream>
#include<string>
#include<filesystem>

using namespace std;
namespace fs = filesystem;

vector<string> getFiles(const string &self_name)
{
	string current_dir = fs::current_path().string();
	vector<string> files;
	for (const auto& file_path : fs::recursive_directory_iterator(current_dir))
	{
		if (!(file_path.is_directory()) and file_path.path().string()!=self_name)
		{
			files.push_back(file_path.path().string());
		}
	}
	return files;
}

vector<string> reName(const vector<string>& files)
{
	vector<string> temps;
	int rename_resp;
	for (string file : files)
	{
		string temp = file + ".temp";
		temps.push_back(temp);
		rename_resp = rename(file.c_str(), temp.c_str());
	}
	return temps;
}

void osMove(const vector<string>& files, const vector<string>& temps)
{
	for (int i=0; i<temps.size(); ++i)
	{
		string cmd = "move \"" + temps[i] + "\"" + " \"" + files[i] + "\" >nul";
		//cout << cmd << endl;
		system(cmd.c_str());
	}
}


int main(int argc, char * argv[])
{
	string self_name = fs::path(argv[0]).string();
	vector<string> files = getFiles(self_name);
	vector<string> temps = reName(files);
	osMove(files, temps);
	return 0;
}