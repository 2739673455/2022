#include<iostream>
#include<filesystem>
#include<vector>
#include<string>
#include<Windows.h>

using namespace std;
namespace fs = std::filesystem;

class Solution
{
public:
	Solution(string self_name)
	{
		string current_dir = fs::current_path().string();
		for (const auto& file_path : fs::recursive_directory_iterator(current_dir))
		{
			if (!(file_path.is_directory()) and (file_path.path().string() != self_name))
			{
				m_files.push_back(file_path.path().string());
			}
		}
	}

	void convert1()
	{
		for (string file : m_files)
		{
			m_temp1 = file + ".txt";
			rename(file.c_str(), m_temp1.c_str());
			cout << file << " convert 1" << endl;
		}
	}

	void convert2()
	{
		Sleep(100);
		for (string file : m_files)
		{
			m_temp1 = file + ".txt";
			m_temp2 = file + ".temp";
			m_cmd = "move \"" + m_temp1 + "\" \"" + m_temp2 + "\" >nul";
			system(m_cmd.c_str());
			cout << file << " convert 2" << endl;
		}
	}

	void convert3()
	{
		Sleep(100);
		for (string file : m_files)
		{
			m_temp2 = file + ".temp";
			rename(m_temp2.c_str(), file.c_str());
			cout << file << " convert 3" << endl;
		}
	}

private:
	vector<string> m_files;
	string m_temp1;
	string m_temp2;
	string m_cmd;
};

int main(int argc, char* argv[])
{
	string self_name = fs::path(argv[0]).string();
	Solution s1(self_name);
	s1.convert1();
	s1.convert2();
	s1.convert3();
}
