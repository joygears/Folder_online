#include <iostream>

using namespace std;

class X {
	public:
		X(){}
		~X(){}
		operator int(){return 1;}
		X foo(){ return *this;};
	
};

int main(int argc,char ** argv){
	X xx;
	X yy;
	
	if(xx.foo() || yy.foo()){
		
	}

	return 0;
}

