#include <iostream>
#include <typeinfo>
using namespace std;

template<class T=short,class D=int> 
class CMath{
public:
	void print(){

		cout <<"type of m_t:" <<typeid(m_t).name() << endl;
		cout <<"type of m_d:" <<typeid(m_d).name() << endl;	
	}

private:
	T m_t;
	D m_d;
};
int main(){
	CMath<double,float> m; 
	m.print();

	return 0;
}