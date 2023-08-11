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
		virtual void ppp(float z){}
		virtual float ppp(){return 1;}
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
		virtual float ppp(){return 1;}
		virtual void ppp(float z){}
	protected:
		float _z;
		
};
class Obj_Player
{
public:
     int Sum()
    {
        return 1;
    }
     int Sum(int a)
    {
        return 2;
    }
	int num;
};

	int main(int argc,char ** argv){
	
	// Point3d*  point= new  Point3d(1,2,3);
	// int (Obj_Player:: * Func1)() = (int (Obj_Player::*)())(&Obj_Player::Sum);
	// float (Point3d:: * aa)() const = (float ( Point3d::* )() const)(&Point3d::z);
	
	// printf("&Point3d::z = %p" , aa);
	// printf("&Obj_Player::Sum = %p" , Func1);
	Obj_Player* obj = new Obj_Player;
	int (Obj_Player:: * Func1)() = (int (Obj_Player::*)())(&Obj_Player::Sum);
	int Obj_Player:: * num = &Obj_Player::num;

	printf("obj->*Func1() = %d\n",(obj->*Func1)());
	printf("Obj_Player:: * num = %d\n",obj->*num);
	
	return 0;
}

// #include <iostream>
// using namespace std;

// int main()
// {
    // Obj_Player b;
    // int (Obj_Player:: * Func1)() = (int (Obj_Player::*)())(&Obj_Player::Sum);
    // (b.*Func1)();
    // int (Obj_Player:: * Func2)(int) = (int (Obj_Player::*)(int))(&Obj_Player::Sum);
    // (b.*Func2)(444);
// }