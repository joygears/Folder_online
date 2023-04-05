#include <iostream>
using namespace std;

class A{
public:
	template<class T> void foo(){
			cout << "A::foo<T>()" << endl;
	}
};
template<class D> void Func(){
	D d;
	d.template foo<int>();
}

int main()
{
	Func<A>();

	return 0;
}