#include <iostream>
#include <functional>



int (*fun_ptr)(int);

int fun1(int a) {
    return a;
}

int main(int argc, char* argv[]) {
    std::function<int(int)> callback;
    std::cout << "Hello world" << std::endl;

    fun_ptr = fun1; //函数指针fun_ptr指向fun1函数
    callback = fun_ptr; //std::function对象包装函数指针
    std::cout << callback(10) << std::endl; //std::function对象实例调用包装的实体

    return 0;
}