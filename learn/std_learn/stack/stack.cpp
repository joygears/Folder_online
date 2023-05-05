#include <queue>
#include <vector>
#include <iostream>

using namespace std;

int main(){
	queue<int,vector<int>>  s;
	s.push(1);
	s.push(2);
	s.push(3);
	s.push(4);
	s.push(5);
	s.push(6);
	while(!s.empty()){
		cout << s.front() << endl;
		s.pop();
	}
	return 0;
}