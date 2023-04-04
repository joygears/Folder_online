#include <iostream>
#include <typeinfo>
using namespace std;

template<class T=int,class D=short> 
class CMath{


public:
	void print(){

		cout << "type of T : " << typeid(T).name() << endl;
		cout << "type of D : " << typeid(D).name() << endl;
	}

private:
	T m_t;
	D m_d;
};

int main(){
	CMath<> m;
	m.print();
	return 0;
}