#include <iostream>

using namespace std;


template<class T> class CMath{
	public:
		CMath(T const& t1, T const& t2):m_t1(t1),m_t2(t2){}
	T add(){
		return m_t1 + m_t2;
	}
private:
	T m_t2;
	T m_t1;
};

template<>  char *const CMath<char * const>::add(){
	return strcat(m_t1,m_t2);
} 


int main(){
	char nx[256]="hello",cy[256]=" word";
	CMath<char * const> m4(nx,cy);
	cout << m4.add();
	return 0;
}