#include <iostream>
#include <thread>
#include <condition_variable>

using namespace std;
#include "func.h"
 
int main()
{	
	/*mutex mtx;
	condition_variable cv;
	bool start = false;
	cout << "prepare" << endl;

	thread obj([&]() {
		cout << "start" << endl;
		start = true;
		cv.notify_one();

		});
	obj.detach();
	unique_lock<mutex> lk(mtx);
	cv.wait(lk, [&]() {return start; });
	cout << "over" << endl;*/
	int a = 0;
	auto b = [&]() {
		return a;
	};

	Function(b);

}