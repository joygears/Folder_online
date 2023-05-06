#include <iostream>
#include <deque>
#include <algorithm>
using namespace std;

class Student{
public:
	Student(string const& name="",int age=0):m_name(name),m_age(age){}
	bool operator==(Student const& that){
		return m_name==that.m_name && m_age==that.m_age; 
	}
	bool operator<(Student const& that){
		return m_age < that.m_age;
	}


private:
	string m_name;
	int m_age;
	friend ostream & operator<<(ostream & os ,Student& stu);
};

ostream & operator<<(ostream & os ,Student& stu){

	os << stu.m_name << " : " << stu.m_age ;
	return os;
}

void print(string const& str, deque<Student>& d){
	cout << str << endl;
	for(deque<Student>::iterator it = d.begin();it!=d.end();++it){

		cout << *it << endl;
	}
	cout << endl <<"-----------------------------------" << endl;
}

int main(){
	string aa = "黄忠";
	deque<Student> di;
	di.push_front(Student("张飞",22));
	di.push_front(Student("赵云",20));
	di.push_front(Student("马超",26));
	di.push_front(Student("关羽",28));
	di.push_front(Student("黄忠",44));
	print("after add node",di);
	di.insert(di.begin(),Student("刘备",30));
	print("after insert node on position of iterator",di);
	di.erase(di.begin());
	print("after erase node on position of iterator",di);
	
	deque<Student>::iterator it = di.begin();
	*it = Student("吕布",36);
	print("after update node on position of iterator",di);

	it = find(di.begin(),di.end(),Student("关羽",28));
	if(it != di.end()){
		di.erase(it);
	}
	print("find after",di);

	sort(di.begin(),di.end());
	
	print("after sort",di);
	return 0;
}