#include <iostream>


using namespace std;

class Base1{
	public:
		Base1(){}
		virtual ~Base1(){}
		virtual void speakClearly(){}
		virtual Base1 * clone() const { return 0; }
		virtual void print(){ cout << "Base1::print" << endl;}
	protected:
		float data_Base1;
};

class Base2{
	public:
		Base2(){}
		virtual ~Base2(){}
		virtual void mumble(){}
		virtual Base2 * clone() const { return 0;}
		virtual void print(){ cout << "Base2::print" << endl;}
	protected:
		float data_Base2;
};

class Derived : public Base1,public Base2{
	public:
		Derived(){}
		virtual ~Derived(){}
		virtual Derived * clone() const {return 0;}
		virtual void print(){ cout << "Derived::print" << endl;}
	protected:
		float data_Derived;
	
};

	int main(int argc,char ** argv){
	
		Base2 * obj = new Derived;
		Derived * der = (Derived *)obj->clone();
		
		der->clone();
	
	return 0;
}

