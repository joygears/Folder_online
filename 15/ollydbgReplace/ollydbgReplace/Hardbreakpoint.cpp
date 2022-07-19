#include "Hardbreakpoint.h"
DWORD * P4D375C = (DWORD*)0x4D375C;
HINSTANCE* hInstance = (HINSTANCE*)0x004D3B78;
HWND *hWndClient = (HWND*)0x004D3B80;
DLGPROC DialogFunc = (DLGPROC)0x00408E1C;

DWORD* dword_4D375C = (PDWORD)0x4D375C;
t_hardbpoint* hardpointAry = (t_hardbpoint*)0x004D8D70;
t_thread** ppthreadAry = (t_thread**)0x4D7DB0;
void  (*Error)(const char *) = (void  (*)(const char*))0x0045401C;
t_status* g_debugedProcessStatus =(t_status*)0x004D5A5C;
PDWORD dword_4CD2E8 = (PDWORD)0x4CD2E8;
PDWORD g_DebugedThreadCount = (PDWORD)0x004D7D98;
int Hardbreakpoints(int arg_0)
{
    if (*P4D375C == 0) {
        return -1;
    }
    *dword_4CD2E8 = arg_0;
    return DialogBoxParamA(*hInstance, "DIA_HARD", *hWndClient, DialogFunc, 0);
}

int Sethardwarebreakpoint(int addr, int size, int type) {
    DWORD edi;
    t_thread* threadAry = *ppthreadAry;
    //若[4D375C] != 0, 则跳转，否则return - 1, 表示失败
    if (*dword_4D375C == 0)
        return -1;
   
    if (type == HB_CODE || type == HB_ONESHOT || type == HB_STOPAN || type == HB_TEMP) {
        size = 1;
    }
    else if (type == HB_IO) {
        edi = addr & 0xFFFFF;
    }
    else if (type != HB_FREE && size - 1 & addr != 0) {
        return -1;
    }

    if (size != 1 && size != 2 && size != 4) {
        return -1;
    }
   
    int containFlag = 0;
    int i = 0;
    do {
   
        //若打的断点是重复断点，则直接返回成功
        if (hardpointAry[i].type != HB_FREE
            && type == hardpointAry[i].type
            && addr >= hardpointAry[i].addr
            && hardpointAry[i].addr + hardpointAry[i].size >= addr + size) {
            return 0;
        }
         //若当前断点包含了之前打的断点，则覆盖之前的断点
        if (addr <= hardpointAry[i].addr
            && hardpointAry[i].addr + hardpointAry[i].size <= addr + size) {
            hardpointAry[i].addr = addr;
            hardpointAry[i].size = size;
            containFlag = true;
        }
        i++;
      
    } while (i < 4);

    if (containFlag == false) {

        i = 0;

        //这个循环是检测硬件断点表是否还可以增加断点
        do {
            if (hardpointAry[i].type == HB_FREE)
                break;
            i++;

        } while (i < 4);

        if (i >= 4) {

            if (type == HB_ONESHOT || type == HB_STOPAN || type == HB_TEMP) {
                return -1;
            }

            if (Hardbreakpoints(1)) {
                return -1;
            }

            i = 0;

            do {

                if (hardpointAry[i].type == HB_FREE)
                    break;

                i++;

            } while (i < 4);

        }

        if (i >= 4) {

            Error((char *)"There is no free slot for a new hardware breakpoint.");
            return -1;
        }

        //将当前断点的信息记录到断点表中
        hardpointAry[i].addr = addr;
        hardpointAry[i].size = size;
        hardpointAry[i].type = type;
    }

    if (*g_debugedProcessStatus != t_status::STAT_RUNNING || type == 5 || type == 6 || type == 7) return 0;

    if (threadAry == 0) {
        Error((char*)"Internal error : don't know how to set hardware breakpoint.");
        return -1;
    }

    for (i = 0; i < *g_DebugedThreadCount; i++) {
        SuspendThread(threadAry[i].thread);
    }


    return 0;
}