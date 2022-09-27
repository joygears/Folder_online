
#include <iostream>
#include <Windows.h>

int exception_filter(LPEXCEPTION_POINTERS pExceptionptrs) {
    if (pExceptionptrs->ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION)
        return EXCEPTION_EXECUTE_HANDLER;
    else 
        return EXCEPTION_CONTINUE_SEARCH;
}

int main()
{
    int* a = 0;
    __try {

        *a = 1;
    }
    __except (exception_filter(GetExceptionInformation())) {
        MessageBox(0, TEXT("捕获内存访问异常成功"), 0, 0);
    }
}


