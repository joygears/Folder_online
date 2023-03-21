#include <iostream>

using namespace std;


template<class T> class A{
public:
	static void print(){
		cout << "&m_i: " << &m_i << "m_t: " << &m_t << endl;
	}
	static int m_i;
	static T m_t;
};

template<class T> int A<T>::m_i;
template<class T> T A<T>::m_t;
int main(){
	A<int> x,y,z;
	x.print();
	y.print();
	z.print();
	A<int>::print();

	A<double> m,n,t;
	m.print();
	n.print();
	t.print();
	A<double>::print();
	return 0;
}