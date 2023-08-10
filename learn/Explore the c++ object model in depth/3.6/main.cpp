#include <iostream>


using namespace std;

struct Base1 { int val1; };
struct Base2 { int val2; };
struct Derived : Base1,Base2{int val3;};

void func1(int Derived::*dmp,Derived * pd){
	
	printf("pd->*dmp = %p\n" , pd->*dmp);
	
}

void func2(Derived * pd){
	
	int Base2::*bmp = &Base2::val2;
	printf("int Base2::*bmp = %p\n" , bmp);
	func1(bmp,pd);

}

int main(int argc,char ** argv){
	Derived * pd = new Derived;
	pd->val1 = 1;
	pd->val2 = 2;
	pd->val3 = 3;
	
	int Derived::* dmp = &Derived::val2;
	printf("&Derived::val2 = %p pd->*dmp = %d\n" , dmp,pd->*dmp);
	
	
	return 0;
}

