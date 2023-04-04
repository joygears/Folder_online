#include <iostream>
using namespace std;
template<class T>class Arrary{
	public:
		T& operator[](size_t i){

			return m_arr[i];
		}
	private:
		T m_arr[10];
};

int main(){
	Arrary<Arrary<int>> m;
	for (int j=0;j<10;j++){
		for (int i=0;i<10;i++)
			m[j][i] = j * 10 +i +1;
	}

		for (int j=0;j<10;j++){
		for (int i=0;i<10;i++)
			cout << m[j][i] << " ";
	}

	return 0;
}