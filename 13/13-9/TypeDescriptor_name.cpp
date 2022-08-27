#include <stdio.h>
#include <locale.h>
int main(int argc){
	try{
		
		throw L"life is a fuck movie";
		throw "life is a fuck movie";
		throw L'l';
		throw 'l';
		throw L"life is a fuck movie";
		throw 5LL;
	}
	catch(wchar_t * e){
		setlocale(LC_ALL, "chs");
		printf("catch wchar_t %ws",e);
	}
	catch(long long int e){
		printf("catch wchar_t %lld",e);
	}
	
}