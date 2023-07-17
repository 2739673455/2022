#include<string>
#include<vector>
#include<iostream>
#include<filesystem>
#include<Windows.h>
#include<thread>
#include<mutex>

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

void convert1(const vector<string> &files,const size_t num_files,int& num_convert1,mutex & mutex1)
{
	string temp_txt;
	while (num_convert1 < num_files)
	{
		mutex1.lock();
		++num_convert1;
		temp_txt = files[num_convert1] + ".txt";
		rename(files[num_convert1].c_str(), temp_txt.c_str());
		mutex1.unlock();
	}
}

void convert2(const vector<string> &files,const size_t num_files, int& num_convert2, int& num_convert1, mutex& mutex1)
{
	string temp_txt;
	while (num_convert2 < num_files)
	{
		mutex1.lock();
		if (num_convert2 > num_convert1)
		{
			mutex1.unlock();
			return;
		}
		Sleep(100);
		temp_txt = files[num_convert2] + ".txt";
		rename(files[num_convert2].c_str(), temp_txt.c_str());
		++num_convert2;
		mutex1.unlock();
	}
}

int main(int argc, char* argv[])
{
	string self_name = fs::path(argv[0]).string();
	vector<string> files = getFiles(self_name);
	size_t num_files = files.size();
	int num_convert1 = -1;
	int num_convert2 = 0;
	mutex mutex1;

	thread convert_thread1(convert1, files, num_files, num_convert1, mutex1);
	thread convert_thread2(convert2, files, num_files, num_convert2, num_convert1, mutex1);
	convert_thread1.join();
	convert_thread2.join();

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
