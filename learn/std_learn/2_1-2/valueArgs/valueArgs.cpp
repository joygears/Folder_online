#include <iostream>
using namespace std;

template<class T=int,size_t S=15>

class Array{
public:

	T& operator[](size_t i){

		return m_ary[i];
	}
	size_t size(){

		return S;
	}
private:
	T m_ary[S];
};
int main(){
	Array <int,20> a;
	for(int i=0;i<a.size();i++){
		a[i]=i+1;

	}
	for(int i=0;i<a.size();i++){
		cout << a[i] << " ";
	}
	return 0;
}