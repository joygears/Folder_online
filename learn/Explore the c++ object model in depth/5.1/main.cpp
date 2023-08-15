class A{ public: A(){}};
class B : public virtual A{};
class C : public virtual A{};
class D : public B,public C{};
class F : public D{};

int main(int argc,char ** argv){
	
	B b;
	D d;
	F f;	
	
	return 0;
}

