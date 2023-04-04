#include <iostream>
using namespace std;

void Max(int x,int y){
	cout << "1:void Max(int x,int y)" << endl;
}

template<class T> void Max(T x,T y) {
	cout << "2:void Max(T x,T y)" << endl;
}

int main(){

	Max(1.0,2);

	return 0;
}