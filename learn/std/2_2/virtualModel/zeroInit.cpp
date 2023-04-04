#include <iostream>
using namespace std;

class Integer{
public:
	Integer():m_int(0){}
private:
	int m_int;
	friend ostream& operator<<(ostream& os,Integer & that);
};
template<class T> void Func(){
	T t = T();

	cout << t << endl;
}

ostream& operator<<(ostream& os,Integer & that){
	return os << that.m_int;
}

int main(){
	Func<int>();
	Func<Integer>();
	return 0;
}