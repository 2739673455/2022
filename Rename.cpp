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
	int feedback;
	string cmd;
	string temp_txt;
	string temp_temp;


	for (string file : files)
	{
		temp_txt = file + ".txt";
		cmd = "move \"" + file + "\"" + " \"" + temp_txt + "\" >nul";
		system(cmd.c_str());
	}

	for (string file : files)
	{
		temp_txt = file + ".txt";
		feedback = rename(temp_txt.c_str(), file.c_str());
	}



	////all
	//for (string file : files)
	//{
	//	temp_txt = file + ".txt";
	//	feedback = rename(file.c_str(), temp_txt.c_str());
	//}
	//system("pause");

	//for (string file : files)
	//{
	//	temp_txt = file + ".txt";
	//	temp_temp = file + ".temp";
	//	feedback = rename(temp_txt.c_str(), temp_temp.c_str());

	//	cmd = "ahh.exe \"" + temp_temp + "\"" + " \"" + file + "\"";
	//	system(cmd.c_str());
	//}
}
