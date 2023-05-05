#include <queue>
#include <map>
#include <iostream>

using namespace std;

class Candidate{
public:
	Candidate(string name=""):m_name(name),m_vote(0){}
	string m_name;
	int m_vote;
};
void print(map<char,Candidate> & m){
	cout << endl;
	for(map<char,Candidate>::iterator it = m.begin();it != m.end(); ++it){
		cout << "(" << (*it).first << ")" << (*it).second.m_name << " ";
	}
	cout << endl << "---------------------------";
}

int main(){
	map<char,Candidate> m;
	m.insert(pair<char,Candidate>('A',Candidate("张飞")));
	m.insert(pair<char,Candidate>('B',Candidate("关羽")));
	m['C'] = Candidate("赵云");
	m['D'] = Candidate("马超");
	m['E'] = Candidate("黄忠");

	print(m);

	return 0;
}