#include <iostream>
using namespace std;

template<class T> class Base{
	public:
		virtual void foo(){
			cout  << "Base<T>::foo" <<endl;
		}


};

int main(){
	Base<int> b;
	b.foo();

	return 0;
}