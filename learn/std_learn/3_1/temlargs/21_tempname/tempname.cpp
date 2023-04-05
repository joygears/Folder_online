#include <iostream>
using namespace std;

class A{
public:
	class B{
	public:
		void foo(){

				cout << "A::B::foo()" << endl;
		}

	};


};

template<class T> void Func(){
	typename T::B b;
	b.foo();

}

int main(){
	Func<A>();

	return 0;
}