#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Student{

public:
	Student(string name,int age):m_name(name),m_age(age){
		
		//cout <<"默认构造 " <<m_name << " " << this << endl;
	}
	Student(Student & that){
		m_name = that.m_name;
		m_age = that.m_age;
		//cout <<"复制构造 " <<m_name << " " << this << endl;
	}
	~Student(){

		//cout <<"析构 " << m_name << " " << this << endl;
	}
	bool operator==(Student const& that){

		return that.m_name==m_name&&that.m_age==m_age;
	}
	bool operator<(Student const& that){
		return m_age < that.m_age;
	}
private:
	string m_name;
	int m_age;
	friend ostream& operator<<(ostream& os,Student& stu);
	friend class CMP;
};

ostream& operator<<(ostream& os, Student& stu){

	os << stu.m_name  <<" "<< stu.m_age << " ";
	return os;
}
void print(vector<Student> &stus){
	cout <<"-----------------------------------------------------------"<< endl;
	for(vector<Student>::iterator it = stus.begin();it != stus.end() ; ++it)
		cout << *it ;
	cout << endl;
}

class CMP{

public:
	bool operator()(Student const& a,Student const& b){

		return a.m_age > b.m_age;
	}

};

int main(){
	vector<Student> stus;
	stus.push_back(Student("张飞",20));
	stus.push_back(Student("刘备",26));
	stus.push_back(Student("赵云",15));
	stus.push_back(Student("关羽",25));

	print(stus);

	vector<Student>::iterator it = find(stus.begin(),stus.end(),Student("张飞",20));
	if(it!=stus.end())
		stus.erase(it);
	print(stus);
	CMP cmp;
	//sort(stus.begin(),stus.end());
	sort(stus.begin(),stus.end(),cmp);
	print(stus);

	return 0;
}