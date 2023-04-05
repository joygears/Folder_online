#include <iostream>

using namespace std;


template<class T,class D> class CMath{
	public:
		static void foo(){

			cout << "1:CMath<T,D>::foo" << endl;
		}

};

template<class T> class CMath<T,short> {
	public:
		static void foo(){
			cout << "2:CMath<T,short>::foo" << endl;

		}


};


int main(){
	CMath<int,double>::foo();
	CMath<int,short>::foo();
	return 0;
}