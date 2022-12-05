#include "m.h"
int main(int argc, char* argv[]) {
    A ma;    B mb;
    QObject::connect(&ma, &A::s3, &mb, &B::x);  //关联信号和槽，详见后文
    ma.g();   //调用对象mb的成员函数x输出X，可见对象ma和mb之间实现了通信。
    return 0;
}