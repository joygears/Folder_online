#include <iostream>
#include <vector>

using namespace std;

class Student{

public:
	Student(string name){
		m_name = name ;
		//cout <<"默认构造 " <<m_name << " " << this << endl;
	}
	Student(Student & that){
		m_name = that.m_name;
		//cout <<"复制构造 " <<m_name << " " << this << endl;
	}
	~Student(){

		//cout <<"析构 " << m_name << " " << this << endl;
	}
private:
	string m_name;
	friend ostream& operator<<(ostream& os,Student& stu);
};

ostream& operator<<(ostream& os,Student& stu){

	os << stu.m_name ;
	return os;
}

int main(){
	vector<Student> stus;
	stus.push_back(Student("zhangsan"));
	stus.push_back(Student("lisi"));

	for(vector<Student>::iterator it = stus.begin();it != stus.end() ; ++it)
		cout << *it << endl;

	return 0;
}