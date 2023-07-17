#include<string>
#include<vector>
#include<iostream>
#include<filesystem>
#include<Windows.h>
#include<thread>
#include<mutex>
#include<deque>

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

void convert1(const vector<string>& files, deque<string>& filesqueue,int& condition, mutex& mutex1)
{
	string temp_txt;
	for (auto file : files)
	{
		mutex1.lock();
		temp_txt = file + ".txt";
		rename(file.c_str(), temp_txt.c_str());
		cout << file << " convert1" << endl;
		filesqueue.push_back(file);
		mutex1.unlock();
	}
	condition = 1;
}

void convert2(const vector<string>& files, deque<string> &filesqueue, int& condition, mutex& mutex1)
{
	string file;
	string temp_txt;
	while(true)
	{
		mutex1.lock();
		if (!filesqueue.empty())
		{
			Sleep(100);
			file = filesqueue.front();
			filesqueue.pop_front();
			temp_txt = file + ".txt";
			rename(temp_txt.c_str(), file.c_str());
			cout << file << " convert2" << endl;
		}
		else if (condition == 1)
		{
			mutex1.unlock();
			break;
		}
		mutex1.unlock();
	}
}

int main(int argc, char* argv[])
{
	string self_name = fs::path(argv[0]).string();
	vector<string> files = getFiles(self_name);
	deque<string> filesqueue;
	int condition = 0;
	mutex mutex1;

	thread convert_thread1([&]() {convert1(files, filesqueue, condition, mutex1); });
	thread convert_thread2([&]() {convert2(files, filesqueue, condition, mutex1); });
	convert_thread1.join();
	convert_thread2.join();
	cout << "end" << endl;
}
