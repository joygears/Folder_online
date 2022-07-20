#include "Hardbreakpoint.h"
DWORD* P4D375C = (DWORD*)0x4D375C;
HINSTANCE* hInstance = (HINSTANCE*)0x004D3B78;
HWND* hWndClient = (HWND*)0x004D3B80;
DLGPROC DialogFunc = (DLGPROC)0x00408E1C;

DWORD* dword_4D375C = (PDWORD)0x4D375C;
t_hardbpoint* hardpointAry = (t_hardbpoint*)0x004D8D70;
t_thread** ppthreadAry = (t_thread**)0x4D7DB0;
void  (*Error)(const char*) = (void  (*)(const char*))0x0045401C;
t_status* g_debugedProcessStatus = (t_status*)0x004D5A5C;
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
int Deletehardwarebreakpoint(int index) {

	if (*dword_4D375C == 0 || index < 0 || index >= 4)
		return -1;

	hardpointAry[index].addr = 0;
	hardpointAry[index].size = 0;
	hardpointAry[index].type = 0;

	if (*g_debugedProcessStatus != 3)
		return 0;

	t_thread* threadAry = *ppthreadAry;

	if (threadAry == 0) {
		Error("Internal error : can't delete hardware breakpoint.");
		return -1;
	}

	for (unsigned int i = 0; i < *g_DebugedThreadCount; i++) {
		SuspendThread(threadAry[i].thread);
	}

	CONTEXT Context;

	for (unsigned int i = 0; i < *g_DebugedThreadCount; i++) {

		Context.ContextFlags = 0x10010;

		if (GetThreadContext(threadAry[i].thread, &Context)) {

			Context.Dr0 = hardpointAry[0].addr;
			Context.Dr1 = hardpointAry[1].addr;
			Context.Dr2 = hardpointAry[2].addr;
			Context.Dr3 = hardpointAry[3].addr;

			int j = 0;
			int esi = 0x400;
			int var_4;

			do {
				if (hardpointAry[j].type != HB_FREE) {

					esi |= 1 << ((j * 2) & 0xFF);

					switch (hardpointAry[j].type) {

						case 1:
							var_4 = 0;
							hardpointAry[j].size = 1;
							break;

						case 2:
							var_4 = 3;
							esi |= 0x100;
							break;

						case 3:
							var_4 = 1;
							esi |= 0x100;
							break;

						case 4:
							var_4 = 2;
							esi |= 0x100;
							break;

						default:
							var_4 = 0;
					}

					switch (hardpointAry[j].size) {

						case 2:
							var_4 |= 4;
							break;

						case 4:
							var_4 |= 0xC;

					}

					esi |= var_4 << (j * 4 + 0x10) & 0xFF;
				}
				j++;
			} while (j < 4);

			Context.Dr7 = esi;

			SetThreadContext(threadAry[i].thread, &Context);
		}

	}

	for (unsigned int i = 0; i < *g_DebugedThreadCount; i++){
		ResumeThread(threadAry[i].thread);
	}

	return 0;
}
int Sethardwarebreakpoint(unsigned long addr, int size, int type) {

	t_thread* threadAry = *ppthreadAry;
	CONTEXT Context;
	//若[4D375C] != 0, 则跳转，否则return - 1, 表示失败
	if (*dword_4D375C == 0)
		return -1;

	if (type == HB_CODE || type == HB_ONESHOT || type == HB_STOPAN || type == HB_TEMP) {
		size = 1;
	}
	else if (type == HB_IO) {
		addr = addr & 0xFFFFF;
	}
	else if (type != HB_FREE && ((size - 1) & addr )!= 0) {
		return -1;
	}

	if (size != 1 && size != 2 && size != 4) {
		return -1;
	}

	int containFlag = 0;
	unsigned int i = 0;
	do {
		if (hardpointAry[i].type != HB_FREE
			&& type == hardpointAry[i].type) {
			//若打的断点是重复断点，则直接返回成功
			if (addr >= hardpointAry[i].addr
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

			Error((char*)"There is no free slot for a new hardware breakpoint.");
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


	for (unsigned int i = 0; i < *g_DebugedThreadCount; i++) {
		Context.ContextFlags = 0x10010;
		if (!GetThreadContext(threadAry[i].thread, &Context)) {
			int a = ::GetLastError();
			continue;
		}
		Context.Dr0 = hardpointAry[0].addr;
		Context.Dr1 = hardpointAry[1].addr;
		Context.Dr2 = hardpointAry[2].addr;
		Context.Dr3 = hardpointAry[3].addr;

		DWORD esi = 0x400;
		int j = 0;
		int var_4;

		do {

			if (hardpointAry[j].type != HB_FREE) {

				esi = esi | (1 << ((j * 2) & 0xFF));

				switch (hardpointAry[j].type) {

				case 1:
				case 5:
				case 6:
				case 7:
					var_4 = 0;
					hardpointAry[j].type = 1;
					break;

				case 2:
					var_4 = 3;
					esi |= 0x100;
					break;

				case 3:
					var_4 = 1;
					esi |= 0x100;
					break;

				case 4:
					var_4 = 2;
					esi |= 0x100;
					break;

				default:
					var_4 = 0;
				}

				switch (hardpointAry[i].type) {

				case 2:
					var_4 |= 4;
					break;

				case 4:
					var_4 |= 0x0C;
				}

				esi |= (var_4 << ((j * 4 + 0x10) & 0xFF));
			}

			j++;

		} while (j < 4);

		Context.Dr7 = esi;

		SetThreadContext(threadAry[i].thread, &Context);
	}
	for (i = 0; i < *g_DebugedThreadCount; i++) {
		ResumeThread(threadAry[i].thread);
	}
	return 0;
}