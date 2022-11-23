
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

int main(int argc, char** argv)
{

    int a[5] = { 1,2,3,4,5 };
    
    
   /* ofstream ouF;
    ouF.open("./me.dat", std::ofstream::binary);
    ouF.write(reinterpret_cast<const char*>(a), sizeof(int) * 5);
    ouF.close();*/

    ifstream inF;
    inF.open("./file", std::ifstream::binary);
    inF.seekg(0, std::ios_base::end);
    std::streampos fileSize = inF.tellg();
    int* b = new int[fileSize];
    inF.seekg(0, std::ios_base::beg);
    inF.read(reinterpret_cast<char*>(b), fileSize);
    inF.close();

   // for (int i = 0; i < 5; i++)
   // {
   //     cout << b[i] << endl;
   // }
	//ifstream ifs(R"(./file)", ios::binary);
	//if (!ifs.good())
	//{
	//	cout << "File not found" << endl;
	//	return 0;
	//}
	//vector<char> bufVector((std::istreambuf_iterator<char>(ifs)), (std::istreambuf_iterator<char>()));
	//string buffer(bufVector.begin(), bufVector.end());
    return 0;
}
