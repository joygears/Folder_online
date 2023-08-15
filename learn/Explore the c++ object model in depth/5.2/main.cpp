#include <iostream>


using namespace std;

class Abstract_base {
	public:
		virtual ~Abstract_base(){};
		virtual void interface() const = 0;
		virtual const char * mumble() const  { return _mumble; }
	protected:
		char * _mumble;
};
void Abstract_base::interface() const {
	
	
}

class Concrete_derived : public Abstract_base {
	public:
		Concrete_derived(){}
		inline void Concrete_derived::interface() const {
			Abstract_base::interface();
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
	
		
	
	return 0;
}

