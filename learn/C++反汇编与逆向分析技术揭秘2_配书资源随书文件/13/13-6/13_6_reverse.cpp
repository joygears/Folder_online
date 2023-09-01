#include <iostream>

class CExcepctionBase {
public:
	CExcepctionBase() {
		printf("CExcepctionBase() \r\n");
	}

};

class CExcepction :public CExcepctionBase {
public:
	CExcepction() {
		printf("CExcepction(int nErrID)\r\n");
	}

};
int main() {

	int input = 119;
	printf(" «Î ‰»Î≤‚ ‘¥ÌŒÛ¬Î :\n");
	scanf("%d", &input);
	try {
		if (input == 110) {
			CExcepction e;
			throw& e;
		}
	}
	
	return 0;
}