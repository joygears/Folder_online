#include <iostream>
using namespace std;


class CExcepctionBase {
public:
	CExcepctionBase() {
		printf("CExcepctionBase() \r\n");
	}
	~CExcepctionBase()
	{
		 printf("~CExcepctionBase()\r\n");
	}

};

class CExcepction :public CExcepctionBase {
public:
	CExcepction(int num) {
		printf("CExcepction(int nErrID)\r\n");
		_num = num;
	}
	 CExcepction(CExcepction& e) {
		printf("CExcepction(CExcepction& Excepction)\r\n");
		_num = e._num;
	} 
	 // Getter function for _num
	 int getNum()  {
		 return _num;
	 }


private:
	int _num;
};

class person{
public:
	person(){

		cout << "person" << endl;
	}
	~person(){

		cout << "~person" << endl;
	}


};

void test(CExcepction &e){
	person per;
	throw e;
}
void main() {

	int input = 119;
	printf("请输入错误码：\n");
	scanf("%d", &input);
	try {
		if (input == 110) {
			CExcepction e(110);
			throw &e;
		}

		if (input == 119) {
			CExcepction e(119);
			test(e);
		}

		if (input == 120)
		{
			
			throw new CExcepction(120);
			
			
		}
		throw CExcepction(input);
	}
	catch (CExcepction e) {
		printf("catch(CExcepction &e)\n");
		printf("ErrorId: %d\n",e.getNum());

	}
	catch (CExcepction* e) {
		printf("catch (CExcepction* e)\n");
		printf("ErrorId: %d\n", e->getNum());
	}
	return;
}