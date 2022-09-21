#include <Windows.h>
#include <iostream>
int main() {
	HANDLE event = CreateEventA(0, 0, 0, "11");
	int error = 0;
	if (event != 0) {
		error = GetLastError();
		if (error != 0xB7) {
			printf("第一次打开一次本程序");
			getchar();
			return 0;
		}
		
	}
	printf("你已经打开一次本程序了");
	getchar();
	return 0;
}