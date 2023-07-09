#include<string>
#include <iconv.h>

using namespace std;

string convertUTF8ToGBK(const string& sourceStr) 
{
    iconv_t iconvH = iconv_open("GBK", "UTF-8");
    if (iconvH == (iconv_t)(-1)) {
        cerr << "failed to open iconvHandle" << endl;
        return "";
    }

    size_t srcLen = sourceStr.length();
    size_t destLen = srcLen;
    char* dest = new char[destLen];

    char* srcPtr = const_cast<char*>(sourceStr.c_str());
    char* destPtr = dest;
    if (iconv(iconvH, &srcPtr, &srcLen, &destPtr, &destLen) == -1) {
        cerr << "convert failed" << endl;
        iconv_close(iconvH);
        delete[] dest;
        return "";
    }

    string destStr(dest, destPtr-dest);
    iconv_close(iconvH);
    delete[] dest;
    return destStr;
}

string convertGBKToUTF8(const string& sourceStr) 
{
    iconv_t iconvH = iconv_open("UTF-8", "GBK");
    if (iconvH == (iconv_t)(-1)) {
        cerr << "failed to open iconvHandle" << endl;
        return "";
    }

    size_t srcLen = sourceStr.length();
    size_t destLen = srcLen * 2;
    char* dest = new char[destLen];

    char* srcPtr = const_cast<char*>(sourceStr.c_str());
    char* destPtr = dest;
    if (iconv(iconvH, &srcPtr, &srcLen, &destPtr, &destLen) == -1) {
        cerr << "convert failed" << endl;
        iconv_close(iconvH);
        delete[] dest;
        return "";
    }

    string destStr(dest, destPtr-dest);
    iconv_close(iconvH);
    delete[] dest;
    return destStr;
}
