#include <iostream>
#include <Windows.h>
#include "shobjidl.h"
#include "shlguid.h"


using namespace std;
interface IX {
	virtual void Fx1() = 0;
	virtual void Fx2() = 0;
};

interface IY {
	virtual void FY1() = 0;
	virtual void FY2() = 0;
};

class CA :public IX, public IY {
public :
	virtual void Fx1(){
		cout << __FUNCDNAME__ << endl;
	}
	virtual void Fx2() {
		cout << __FUNCDNAME__ << endl;
	}
	virtual void FY1() {
		cout << __FUNCDNAME__ << endl;
	}
	virtual void FY2() {
		cout << __FUNCDNAME__ << endl;
	}
	virtual void CA1() {

	}
};
bool   GetShortCutFile(WCHAR* ShortcutFile, WCHAR* buf, int nSize)
{
	HRESULT           hres;
	IShellLink * psl;
	IPersistFile* ppf;
	WIN32_FIND_DATA   fd;

	CoInitialize(0);
	hres = CoCreateInstance(CLSID_ShellLink, NULL, CLSCTX_INPROC_SERVER,
		IID_IShellLink, (void**)&psl);
	if (!SUCCEEDED(hres))
		return   false;

	hres = psl->QueryInterface(IID_IPersistFile, (void**)&ppf);
	if (SUCCEEDED(hres))
	{
		//wchar_t  wsz[MAX_PATH];   //buffer   for   Unicode   string
		//MultiByteToWideChar(CP_ACP,0,ShortcutFile,-1,wsz,MAX_PATH);  
		//hres =  ppf->Load(wsz,STGM_READ);
		hres = ppf->Load(ShortcutFile, STGM_READ);
		if (SUCCEEDED(hres))
			hres = psl->GetPath(buf, nSize, &fd, 0);
		ppf->Release();
	}
	psl->Release();

	return  SUCCEEDED(hres);
}
class Disp {

public:
	virtual int __stdcall Disp_fun0(GUID*, void**);
	virtual int __stdcall Disp_fun1(GUID*, void**);
	virtual int __stdcall Disp_fun2();
	virtual int __stdcall Disp_fun3(GUID*, void**);
	virtual int __stdcall Disp_fun4(GUID*, void**);
	virtual int __stdcall loadPath(wchar_t*, int);

};
class PPV {

public:
	virtual int __stdcall ppv_fun0(GUID*, Disp**);
	virtual int __stdcall ppv_fun1(GUID*, Disp**);
	virtual int __stdcall ppv_fun2();
	virtual int __stdcall getPath(char*, int, char*, int);
	virtual int __stdcall ppv_fun4(GUID*, Disp**);
	virtual int __stdcall ppv_fun5(GUID*, Disp**);
	virtual int __stdcall ppv_fun6(GUID*, Disp**);
	virtual int __stdcall ppv_fun7(GUID*, Disp**);
	virtual int __stdcall ppv_fun8(GUID*, Disp**);
	virtual int __stdcall ppv_fun9(GUID*, Disp**);
	virtual int __stdcall ppv_fun10(char*, int);
	virtual int __stdcall ppv_fun11(GUID*, Disp**);
	virtual int __stdcall ppv_fun12(GUID*, Disp**);
	virtual int __stdcall ppv_fun13(GUID*, Disp**);
	virtual int __stdcall ppv_fun14(GUID*, Disp**);
	virtual int __stdcall ppv_fun15(GUID*, Disp**);
	virtual int __stdcall ppv_fun16(char*, int);
	virtual int __stdcall ppv_fun17(GUID*, Disp**);
	virtual int __stdcall ppv_fun18(GUID*, Disp**);
	virtual int __stdcall ppv_fun19(HWND, int);

};

GUID g_riid = { 0x000214EE,0 ,0,{0xC0,0 ,0 ,0 ,0 ,0 ,0 ,0x46 }};
GUID g_rclsid = { 0x21401,0 ,0,{0xC0,0 ,0 ,0 ,0 ,0 ,0 ,0x46 } };
GUID g_ppv1 = { 0x10B,0 ,0,{0xC0,0 ,0 ,0 ,0 ,0 ,0 ,0x46 } };
char g_buffer[4096];
PPV* ppv;
typedef int (__stdcall *ppv_fun1)(char *,int);


int main() {
	CA* ca = new CA();

	IX* ix = ca;
	ix->Fx1();
	ix->Fx2();

	IY* iy = ca;
	iy->FY1();
	iy->FY2();
	delete ca;
	ca = nullptr;
	//char szFileName[] = R"(C:\Users\Public\Desktop\Ñ¸½ÝPDF×ª»»Æ÷.lnk)";
	//wchar_t wszFileName[MAX_PATH];
	//wchar_t realFileName[MAX_PATH];
	//MultiByteToWideChar(0, 1, szFileName, -1, wszFileName, 0x104);
	
	//GetShortCutFile(wszFileName, realFileName, MAX_PATH);
	
	
	Disp* nDisp;
	char szFileName[] = R"(C:\Users\Public\Desktop\Ñ¸½ÝPDF×ª»»Æ÷.lnk)";
	wchar_t wszFileName[MAX_PATH];
	HWND hwnd = ::FindWindow(NULL, TEXT("OllyDbg"));
	char var_1D2C[320];
	char realFileName[224];
	CoInitialize(0);
	if (CoCreateInstance(g_rclsid, 0, 1, g_riid, (LPVOID *)&ppv) >= 0) {
		if ( ppv->ppv_fun0(&g_ppv1, &nDisp) >= 0) {
			
			MultiByteToWideChar(0, 1, szFileName, -1, wszFileName, 0x104);
			if (nDisp->loadPath(wszFileName, 0) >= 0) {
				
				if (ppv->getPath(realFileName, MAX_PATH, var_1D2C, 0) < 0) {
					
					realFileName[0] = 0;
				}
				ppv->ppv_fun2();
				nDisp->Disp_fun2();
			}
			
		}
		
	}
	CoUninitialize();
	IMAGE_NT_HEADERS
		MB_OK
	return 0;
}