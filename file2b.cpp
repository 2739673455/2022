#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<cstdio>
#include<sstream>

using namespace std;

vector<string> stringSplit(const string &file1)
{
	vector<string> name_vector;
	stringstream ss(file1);	
	string item;
	while(getline(ss, item, '.'))
	{
		name_vector.push_back(item);
	}
	return name_vector;
}

void file2b(const string &file1)
{
    int c;
	stringstream file2;
	vector<string> name_vector = stringSplit(file1);
	file2<<name_vector[0]<<".dat";
//    char file2[L_tmpnam] = {'\0'};
//    tmpnam(file2);

    ifstream filein(file1, ios_base::in | ios_base::binary); 
    ofstream fileout(file2.str(), ios_base::out);
//    filein.seekg(4096);
	int column = 0;
    while ((c=filein.get())!=EOF) 
    {
		if (column > 15)
		{
			column = 0;
			fileout<<endl;
		}
	    fileout<<c<<" ";
		++column;
    }
    filein.close();
    fileout.close();
}

int main(int argc, char* argv[])
{
    for (int i=1; i<argc; ++i)
    {
		file2b(argv[i]);
    }

    return 0;
}
