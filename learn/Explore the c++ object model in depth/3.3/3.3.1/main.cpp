#include <iostream>


using namespace std;

class Point2d{
	public:
		Point2d(float x = 0.0, float y = 0.0): _x(x) , _y(y){};
		
		float x(){ return _x;}
		float y(){return _y;}
		
		void operator+=(Point2d& rhs){
			_x += rhs.x();
			_y += rhs.y();
		}
	protected:
		float _x,_y;
};
class Point3d : public Point2d
{
	public:
		Point3d(float x,float y,float z):Point2d(x,y),_z(z){}
		float z() const {return _z;}
		void z(float z)  { _z = z;}
		void operator+=(Point3d& rhs){
			Point2d::operator+=(rhs);
			_z += rhs.z();
		}
		
	protected:
		float _z;
		
};


class Concrete1{
	public:
	Concrete1(){
		cout << "Concrete1" << endl;
	}
	private:
		int val;
		char c1;
		
};
class Concrete2 : public Concrete1{
	
	private:
		char c2;
		
};
class Concrete3 : public Concrete2{
	
	private:
		
		char c3;
};



struct A{
char c;
long long int a;
};

int main(int argc,char ** argv){
	
	cout << "size of A is " << sizeof(A) << endl;
	Concrete3 concrete;
	cout << "size of Concrete3 is " << sizeof(concrete) << endl;
	
	return 0;
}

