#include <iostream>
using namespace std;
	
template<class T>
class CMath{
public:
	CMath(T  x,T  y):m_t1(x),m_t2(y){}
	T add(){
		cout << "add function" << endl;
		return m_t1+m_t2;
	}
private:
	T m_t1;
	T m_t2;
};

void hello(){

	cout << "hello" << endl;
}

int main(){
	CMath<int> caltor(1,2);

	return 0;
}