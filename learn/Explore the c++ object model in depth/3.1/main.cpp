#include <iostream>
#include "foo.h"

using namespace std;


class Point3d
{
	public:
		Point3d(float v_x,float v_y,float v_z):x(v_x),y(v_y),z(v_z){}
		float X() const {return x;}
		void X(float new_x)  { x = new_x;}
	private:
		float x,y,z;
};


int main(int argc,char ** argv){
	Point3d point(1,2,3);
	point.X(5);
	cout << point.X() << endl;
	
	
	return 0;
}

