## c++复制赋值操作符

**若当前类定义了复制赋值操作符，当然使用定义的，若没定义，则会按位复制对象，若基类或者成员有定义复制赋值操作符，则触发它们定义的复制赋值操作符，其它没定义的基类和成员则按位复制**

~~~c++
#include <iostream>
using namespace std;

class Point {
	public:
		Point(float x = 0.0,float y = 0.0):_x(x),_y(y){}
		Point & operator=(const Point &p ){
			_x = p._x;
			_y = p._y;
			return *this;
		}
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
~~~

看上面子类`Point3d`没有定义复制赋值操作符`operator=`,但是基类定义了复制赋值操作符，下面我们查看`ida`的分析

~~~c++
Point3d *__fastcall Point3d::operator=(Point3d *this, const Point3d *__that)
{
  Point::operator=(this, __that);
  this->_z = __that->_z;
  return this;
}
~~~

可以看到虽然我们没有定`Point3d::operator=`,但是`Point3d`的子对象`Point`中含有复制赋值操作符，所以自动合成了`Point3d::operator=`，其中Point使用它自己的复制赋值操作符，而`Point3d`自己的成员`z`,则采用按位复制



但是**有一种情况即使基类或者成员没有定义复制赋值操作符，也不会按位复制，而是自动生成复制赋值操作符，那就是类中函数虚函数或类中含有虚继承。**为什么要这样呢，主要是为了**避免复制虚表指针或者虚基类偏移表**

~~~c++
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
~~~

看上面代码Point多加了一个虚函数`z`,所以这样对象中就会虚表指针。而且`Point`和`Point3d`都没有了复制赋值操作符。查看`ida`的分析

~~~c++
Point3d *__fastcall Point3d::operator=(Point3d *this, const Point3d *__that)
{
  Point::operator=(this, __that);
  this->_z = __that->_z;
  return this;
}
~~~

可以看到和前面几乎是一样的，虽然`Point`和`Point3d`都没有了复制赋值操作符，但是由于含有虚表指针，为了避免虚表指针被复制，所以自动生成了operator=，避免了虚表指针被复制

> 为什么不能复制虚表指针呢，是因为对象的虚表不一定是属于本类的虚表，也有可能是基类的，如果直接复制过去的话，会导致调用虚函数的时候调用错误

