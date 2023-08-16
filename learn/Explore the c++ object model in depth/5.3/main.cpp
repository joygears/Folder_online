#include <iostream>
using namespace std;

class Point {
	public:
		Point(float x = 0.0,float y = 0.0):_x(x),_y(y){}
		virtual float z(){return 0.0;}
	private:
		float _x,_y;
};

class Point3d :  public  Point {
	public:
		Point3d(float x = 0.0 , float y = 0.0, float z = 0.0):Point(x,y),_z(z){}

	protected:
		float _z;
};


int main(int argc,char ** argv){
	Point3d a,b;
	a = b;
		
	return 0;
}

