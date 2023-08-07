#include <iostream>
using namespace std;

class X{};
class Y : public virtual X{};
class Z : public virtual X{};
class A : public Y,public Z {};


int main(int argc,char ** argv){
	
	X x;
	Y y;
	Z z;
	A a;
	cout << "sizeof X 的结果为 " <<  sizeof(x) << endl;
	cout << "sizeof Y 的结果为 " <<  sizeof(y) << endl;
	cout << "sizeof Z 的结果为 " <<  sizeof(z) << endl;
	cout << "sizeof A 的结果为 " <<  sizeof(a) << endl;
	
	return 0;
}

