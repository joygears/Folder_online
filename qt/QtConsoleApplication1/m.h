
#ifndef M_H   
#define M_H
#include<QObject>
#include <iostream>
using namespace std;

class A :public QObject {   //信号和槽必须继承自QObject类
    Q_OBJECT             //必须添加该宏
    //public signals:void s1(int);  //错误signals前不能有访问控制符。
signals:void s();          //使用signals关键字声明信号，信号的语法与声明函数相同。
signals:void s(int, int);   //正确，信号可以有参数，也可以重载。
//void s2(){}          //错误，信号只需声明，不能定义。
       void s3();           //注意：这仍是声明的一个信号
public:                //信号声明结束后，重新使用访问控制符，表示以下声明的是成员函数。
    void g() {
        emit s3();   /*发射信号，其语法与调用普通函数相同，在信号与槽关联之前，发射的信号不会调用相应的槽函数。*/
        // emit: s3();  //错误，emit后不能有冒号。
    }
};

class B :public QObject {
    Q_OBJECT
public slots:                 //使用slots关键字声明槽
    void x() { cout << "X" << endl; }  /*正确，槽就是一个普通函数，只是需要使用slots关键字，且能和信号相关联。*/
            //slots: void x(){}   //错误，声明槽时需要指定访问控制符。
public:
    void g() { // emit s3();  //错误，在类B中对于标识符s3是不可见的
    }
};

#endif // M_H