什么是虚继承呢？
下面是一个经典的菱形继承
~~~c++
class A;
class B : public A;
class C : public A;
class D : public B ,public C;
~~~
~~~mermaid
graph TB
A-->B
A-->C
B-->D
C-->D
~~~

这样继承有什么问题呢，请看下图 D的内存结构图

| member     |
| ---------- |
| 虚表指针1  |
| A 成员变量 |
| B 成员变量 |
| 虚表指针2  |
| A 成员变量 |
| C 成员变量 |
| D成员变量  |

 可以看到在没有使用虚继承的情况下程序会生成两份A类的数据成员

如果使用了虚继承，就如下图所示
~~~c++
class A;
class B : public virtual A;
class C : public virtual A;
class D : public B ,public C;
~~~
| member        |
| ------------- |
| 虚表指针1     |
| B虚基类偏移表 |
| B 成员数据    |
| 虚表指针2     |
| C虚基类偏移表 |
| C 成员数据    |
| D成员数据     |
| 虚表指针3     |
| A 成员数据    |

可以看到当B和C使用虚继承的方式继承A的时候，A的base subObject放在了后面，然后使用虚基类偏移表来寻找A base subobject
为什么要在B和C上虚继承A,而不是在D上使用虚继承？
因为是B和C拥有相同的base subObject A，要在它们俩使用虚继承，以让它们共同拥有一份A

### 虚拟继承中类的初始化顺序

根据c++ 构造函数的原则，先构造父类的构造，再构造子类的构造,由于B和C都继承了A且为D的基类子对象，它们对A的构造函数一定不可以发生，否则就会调用A的构造两次，取而代之的是**由最底层的类对虚拟继承的类进行初始化**，因为最底层的类始终只有一个，若再有一个类继承D，则初始化A的任务就会移交给它

~~~c++
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
~~~

我们用`ida`进行分析，首先查看

- b的构造函数

~~~c++
void __fastcall B::B(B *this, int a2)
{
  if ( a2 )  //a2这个标识用来表明是否为最底层的类，若为真，则表示这个类是最底层的类，需要初始化虚继承的基类
  {
    *this = (B)&B::`vbtable';
    A::A((A *)&this[1]);
  }
}
~~~

由于此时的继承关系为

~~~mermaid
graph TB;
A-->B
~~~

所以B是最底层的类，负责初始化虚基类偏移表和A。



- d的构造函数

~~~c++
void __fastcall D::D(D *this, int a2)
{
  if ( a2 )
  {
    this->B = (B)&D::`vbtable'{for `B'};
    this->C = (C)&D::`vbtable'{for `C'};
    A::A((A *)&this[1]);
  }
  B::B(this);
  C::C(&this->C);
}
~~~

由于此时的继承关系为

~~~mermaid
graph TB;
A-->B
A-->C
B-->D
C-->D
~~~

所以D是最底层的类，负责初始化虚基类偏移表和A。

- f的构造函数

~~~c++
void __fastcall F::F(F *this, int a2)
{
  if ( a2 )
  {
    this->B = (B)&F::`vbtable'{for `B'};
    this->C = (C)&F::`vbtable'{for `C'};
    A::A((A *)&this[1]);
  }
  D::D(this);
}
~~~
由于此时的继承关系为
~~~mermaid
graph TB;
A-->B
A-->C
B-->D
C-->D
D-->F
~~~
所以F是最底层的类，负责初始化虚基类偏移表和A。