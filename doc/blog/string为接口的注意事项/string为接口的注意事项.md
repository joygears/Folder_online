## string为接口的注意事项

### 问题描述

​    在一个应用程序中用到了另外一个库的`dll`，向`dll`的接口传递std::string参数时报错。由于这方面的问题比较多，所以我进行了深入研究。

### 前置知识

在vs项目右键 -> 属性 ->C/C++ ->代码生成->运行库,有四个选项，`/MD ` 、`/MDd`、`/MT`、`/MTd`

#### 含有`D`的选项

若设置了这种选项，那么就会和其他设置了含有`D`的选项的模块共同维护一块堆内存，即使跨模块释放也没关系

#### 含有`T`的选项

若设置了这种选项，那么该模块就会自己维护一块堆内存，不允许跨模块释放

#### 含有`d`的选项

若设置了这种选项，那么该模块使用的stl标准库就是debug版本的

#### 不含`d`的选项

若设置了这种选项，那么该模块使用的stl标准库就是release版本的

#### std::string的内存结构

**Debug版本**

~~~c++
struct string{
    std::string::Proxy * _Myproxy
	union Bxty{
		char Buf[0x10];
		char * Ptr;
	};
	Bxty bxty;
#ifdef _WIN64
	unsigned __int64 Mysize;
	unsigned __int64 Myres;
#else
	unsigned int Mysize;
	unsigned int Myres;
#endif
}
~~~

**Release版本**

~~~c++
struct string{
	union Bxty{
		char Buf[0x10];
		char * Ptr;
	};
	Bxty bxty;
#ifdef _WIN64
	unsigned __int64 Mysize;
	unsigned __int64 Myres;
#else
	unsigned int Mysize;
	unsigned int Myres;
#endif
}
~~~

可以看到Debug的std::string比Release的std::string就是多了一个指针`_Myproxy`

> 大部分`stl`的类都是这样的

### 场景模拟



#### 跨模块释放

##### 源代码

_`dll`_

`lib.h`

~~~c++
#include <iostream>
__declspec(dllexport) void test(std::string str);
~~~



`lib.cpp`

~~~c++
#include <lib.h>
void test(std::string str) {
	std::cout << str << std::endl;
}
~~~

编译版本为Debug x86, 运行库选项为 `/MDd`

_`应用程序`_

~~~
#include <iostream>
#include <lib.h>
int main()
{
	std::string str = "aaaaaaaaaaaaaaaaaaaaaa";
	test(str);
	getchar();
}

~~~

编译版本为Debug x86, 运行库选项为 `/MTd`

> 字符串的大小要大于0xF，std::string才会创建一块内存去维护它

##### 现象

 _报错_

![image-20230505173448192](imgs\image-20230505173448192.png)

_调用堆栈_

![image-20230505173727992](imgs\image-20230505173727992.png)

##### 原因分析

为什么会发生跨模块释放呢？

![image-20230505174539789](imgs\image-20230505174539789.png)

看上图的反汇编窗口中红色方框标记的位置，在传递test函数的参数时，首先分配了`0x1C`个栈内存,这刚好是std::string Debug版本的大小，然后调用了std::string 的复制构造函数，将`str`的字符串复制到栈参数中，此时会创建一块内存用于存放复制的字符串

下面查看test中的代码

![image-20230505175024629](imgs\image-20230505175024629.png)

发现在打印完了栈参数的变量后，居然直接在函数内部调用了std::string的析构函数，此函数会把自身维护的内存释放掉，这样在主程序中创建内存，在`dll`中释放内存，发生了跨模块释放。

而为什么不允许跨模块释放呢，因为主程序使用的运行库选项是`/MTd`,这是个含有`T`的选项，所以自己会维护一块堆，不允许跨模块释放

#### 内存结构错乱，字符串乱码

##### 源代码

_`dll`_

`lib.h`

~~~c++
#include <iostream>
__declspec(dllexport) void test(std::string str);
~~~



`lib.cpp`

~~~c++
#include <lib.h>
void test(std::string str) {
	std::cout << str << std::endl;
}
~~~

编译版本为Release x86, 运行库选项为 `/MD`

_`应用程序`_

~~~
#include <iostream>
#include <lib.h>
int main()
{
	std::string str = "aaaaaaaaaaaaaaaaaaaaaa";
	test(str);
	getchar();
}

~~~

编译版本为Release x86, 运行库选项为 `/MDd`

##### 现象

现在主程序和`dll`的运行库都不含`T`，应该没问题了吧，但是还是发生了错误

![image-20230505180756756](imgs\image-20230505180756756.png)

随后报错

![image-20230505192410897](imgs\image-20230505192410897.png)

##### 原因分析

首先是乱码，由于主程序的运行库选项是`/MDd`，这个选项是含`d`,所以在分配栈内存时是使用std::string的Debug版本，char * 指针`Ptr`是存放在类内存的0x4处，而dll的运行库选项是`/MD，这个选项是不含`d`的，它在使用主程序传过来的std::string时，使用的是Release版本,它认为Ptr存放在0x0中，所以在打印的时候打印错位置了，导致的乱码

而堆损坏同样是这个原因，在test函数打印完字符串，析构std::string的时候，它认为Ptr在0x0处，但实际上Ptr是主程序传递的，Ptr在0x4,0x0处的指针指向的并不是一个堆，所以报了堆已损坏的错误



### 结论

最好不要使用stl容器当做动态库的接口，如果实在需要的话，得保证运行库保持一致，可以编两份，一份Release,一份Debug，给第三方调试和使用