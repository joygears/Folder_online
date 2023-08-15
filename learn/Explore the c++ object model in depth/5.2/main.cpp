#include <iostream>


using namespace std;

class Abstract_base {
	public:
		virtual ~Abstract_base(){};
		virtual void interface() const {}
		virtual const char * mumble() const  { return _mumble; }
	protected:
		char * _mumble;
};

class Concrete_derived : public Abstract_base {
	public:
		Concrete_derived(){
			size();
		}
		inline void Concrete_derived::interface() const {
			Abstract_base::interface();
		}
		virtual int size(){size2();return 1;}
		virtual int size2(){ return 2;
		cout <<"hello" << endl;
		}
};

class Point {
	public:
		Point(float x = 0.0,float y = 0.0):_x(x),_y(y){}
		virtual float z(){}
	private:
		float _x,_y;
};



void mumble(){

	
	
	
}
int main(int argc,char ** argv){
	
		Concrete_derived* concrete = new Concrete_derived;
		concrete->size();
	return 0;
}

