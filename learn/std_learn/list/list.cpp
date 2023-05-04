#include <iostream>
#include <list>

using namespace std;
void print(string str,list<int> & ls){
	cout << str << endl;
	for(list<int>::iterator it = ls.begin();it != ls.end();++it){
		cout <<*it<< " ";
	}
	cout << endl << "------------------";

}

int main(){

	list<int> ls;
	for(int i=0;i<5;i++)
		ls.push_front(10+i);
	for(int i=0;i<5;i++)
		ls.push_back(10-i);
	print("first",ls);
	ls.unique();
	print("after unique",ls);
	ls.sort();
	print("after sort  ",ls);

	list<int> lst;
	lst.push_back(1000);
	lst.push_back(2000);
	lst.push_back(3000);
	lst.push_back(4000);
	ls.splice(ls.begin(),lst);
	print("ls:",ls);
	print("lst",lst);
}