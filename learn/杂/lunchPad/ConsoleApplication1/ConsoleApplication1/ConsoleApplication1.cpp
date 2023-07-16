
#include<thread>
#include<mutex>
#include<iostream>

std::mutex test;


void t_fun()
{
	test.lock();//重入导致死锁
	std::cout << "hello\n";
	test.unlock();
}

int main(int argc, char* argv[])
{
	test.lock();
	std::thread th(t_fun);
	th.join();

	return 0;
}
