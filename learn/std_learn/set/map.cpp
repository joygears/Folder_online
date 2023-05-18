#include <set>
#include <iostream>
#include <mutex>
using namespace std;


int main(){
	/*multiset<int> s;
	s.insert(1);
	s.insert(1);
	s.insert(2);
	s.insert(3);
	s.insert(1);
	s.insert(4);
	s.insert(1);
	cout << "节点个数" << s.size() << endl;
	for (set<int>::iterator it = s.begin(); it != s.end(); it++) {
		cout << *it << "	";
	}*/

	static mutex t;
	t.lock();
	cout << "hello world " <<sizeof t<<  endl;
	t.unlock();
	return 0;
}