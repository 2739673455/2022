#include<iostream>
#include<fstream>
#include<string>
#include<cstdio>

using namespace std;

void file2Binary(const string& source)
{
	int binary;
	int pos = source.rfind(".");
	string dest = source.substr(0, pos) + ".dat";

	ifstream filein(source, ios_base::in | ios_base::binary);
	ofstream fileout(dest, ios_base::out);
	//    filein.seekg(4096);
	int column = 0;
	while ((binary = filein.get()) != EOF)
	{
		if (column > 15)
		{
			column = 0;
			fileout << endl;
		}
		fileout << binary << " ";
		++column;
	}
	filein.close();
	fileout.close();
}

int main(int argc, char* argv[])
{
	for (int i = 1; i < argc; ++i)
	{
		file2Binary(argv[i]);
	}
	return 0;
}
