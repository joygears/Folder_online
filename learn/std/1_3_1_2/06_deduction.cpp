#include <iostream>
using namespace std;

template<class D,class T> T Max(T x,T y){
    D t;
    return x > y ? x : y; 
} 

int main(){

    cout << Max<string>(1,2) << endl;

    return 0;
}