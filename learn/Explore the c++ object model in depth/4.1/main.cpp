#include <iostream>


using namespace std;


class Point2d{
	public:
		Point2d(float x = 0.0, float y = 0.0): _x(x) , _y(y){};
		
		float x(){ return _x;}
		float y(){return _y;}
		virtual float z() const {return 1;}
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
		virtual float z() const {return _z;}
		virtual void z(float z)  { _z = z;}
		virtual void operator+=(Point3d& rhs){
			Point2d::operator+=(rhs);
			_z += rhs.z();
		}
		
	protected:
		float _z;
		
};


	int main(int argc,char ** argv){
	
	Point3d*  point= new  Point3d(1,2,3);
	
	point->Point3d::z();
	return 0;
}

