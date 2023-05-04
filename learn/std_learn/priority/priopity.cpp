#include <queue>
#include <vector>
#include <iostream>

using namespace std;

class CMP{
	public:
		bool operator()(int const& a,int const& b){
			return a>b;
		}
};

int main(){
	priority_queue<int,vector<int>,CMP>  s;
	s.push(1);
	s.push(2);
	s.push(3);
	s.push(4);
	s.push(5);
	s.push(6);
	while(!s.empty()){
		cout << s.top() << endl;
		s.pop();
	}
	return 0;
}