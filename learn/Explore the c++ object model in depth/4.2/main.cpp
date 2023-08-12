#include <iostream>


using namespace std;

class Point {
	public:
		virtual ~Point(){}
		virtual Point* mult(float)=0;
		float x() const {return _x;}
		virtual float y() const {return 0;}
		virtual float z() const {return 0;}
		
	protected:
		Point(float x = 0.0 ){}
		float _x;
};
 class Point2d : public Point{
	 public:
		Point2d(float x = 0.0, float y = 0.0): Point(x) , _y(y){};
		~Point2d(){}
		Point* mult(float){return 0;}
		float y() const {return _y;}
		
	protected:
		float _y;
 };
class Point3d : public Point2d
{
	public:
		Point3d(float x,float y,float z):Point2d(x,y),_z(z){}
		~Point3d(){}
		Point* mult(float){return 0;}
		float z() const {return 0;}
		
	protected:
		float _z;
		
 };


	int main(int argc,char ** argv){
	
		Point3d point(1,2,3);
		
	
	return 0;
}

