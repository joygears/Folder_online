// getAudio.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <fstream>
#include <Windows.h>
#pragma comment(lib,"Winmm.lib")

#define BUF_SIZE 960

using namespace std;

DWORD __stdcall audioInputMSGLoop(LPVOID lpThreadParameter);

class WaveIn {
public:
    HANDLE hThread = 0;
    DWORD threadID = 0;
    int nChannels = 1;
    int nSamplesPerSec = 8000;
    int wBitsPerSample = 16;
    HWAVEIN hwi = 0;
    MMRESULT result;
    LPWAVEHDR  pwhs = 0;

    bool openWaveIn();
    bool MessageThreadstartSuss();
    bool addBufToWavaIn();
    bool startWaveIn();
    bool runRecord();
    void stopRecod();
    bool resetWaveIn();
    bool releaseBufHeader();
    bool closeWaveInput();
    bool overThread();
};

bool g_recoding = false;
byte lpData[BUF_SIZE];
WaveIn wavein;

int main()
{
    
    wavein.hThread =  CreateThread(0, 0, audioInputMSGLoop, 0, 0, &wavein.threadID);
    wavein.runRecord();

    getchar();
    wavein.stopRecod();
    return 0;
}

bool WaveIn::overThread() {
    DWORD ExitCode;
    
    if (!this->hThread)
        return true;
    PostThreadMessageA(this->threadID, WM_QUIT, 0, 0);
    int i = 50;
    do {
        if (GetExitCodeThread(this->hThread, &ExitCode) != 0x103) {
            this->hThread = 0;
            return true;
        }
    } while (i);

    TerminateThread(this->hThread, 0);
    this->hThread = 0;
    return true;
}
bool WaveIn::closeWaveInput() {
    if (this->hwi == 0)
        return false;
    this->result = waveInClose(this->hwi);
    this->hwi = 0;
    return !this->result;
}
bool WaveIn::releaseBufHeader() {
    if (!this->pwhs)
        return false;
    int i = 0;
    do {
        this->result = waveInUnprepareHeader(this->hwi, &this->pwhs[i], sizeof(WAVEHDR));
        if (this->result)
            Sleep(100);
        else {
            if (pwhs[i].lpData != 0) {
                delete pwhs[i].lpData;
            }
        }
        i++;
    } while (i < 7);
    delete this->pwhs;
    return true;
}
bool WaveIn::resetWaveIn() {

    if (this->hwi == 0)
        return false;
    this->result = waveInReset(this->hwi);
    return !this->result;
}

void WaveIn::stopRecod() {
    g_recoding = false;
    this->resetWaveIn();
    this->releaseBufHeader();
    if (this->closeWaveInput()) {
        this->overThread();
    }
}
bool WaveIn::runRecord() {
    g_recoding = true;
    if (wavein.MessageThreadstartSuss() == false)
        return 0;
    if (wavein.openWaveIn() == true) {
        if (wavein.addBufToWavaIn() != false) {
            if (wavein.startWaveIn())
                return true;
        }
    }
}
bool WaveIn::startWaveIn() {
    if (this->hwi == 0)
        return false;
    this->result = waveInStart(this->hwi);
    return !this->result;
}

bool WaveIn::addBufToWavaIn() {
    result = waveInReset(hwi);
    if (result)
        return false;

    this->pwhs = new WAVEHDR[7];
    int i = 0;
    do {

        this->pwhs[i] = { 0, };
        this->pwhs[i].lpData = new char[BUF_SIZE];
        this->pwhs[i].dwBufferLength = BUF_SIZE;
        this->result = waveInPrepareHeader(this->hwi, &this->pwhs[i], sizeof(WAVEHDR));
        if (this->result)
            return false;
        this->result =  waveInAddBuffer(this->hwi, &this->pwhs[i], sizeof(WAVEHDR));
        if (this->result)
            return false;
        i++;

    } while (i < 7);

    return true;
}
bool WaveIn::openWaveIn() {
    WAVEFORMATEX pwfx;
    pwfx.nChannels = nChannels;
    pwfx.nSamplesPerSec = nSamplesPerSec;
    pwfx.wBitsPerSample = wBitsPerSample;
    pwfx.wFormatTag = WAVE_FORMAT_PCM;
    pwfx.nAvgBytesPerSec = nSamplesPerSec * wBitsPerSample * nChannels / 8;
    pwfx.nBlockAlign = wBitsPerSample *nChannels / 8;

    result = waveInOpen(NULL, -1, &pwfx, NULL, NULL, 1);
    if (result != 0)
        return 0;
    result = waveInOpen(&hwi, WAVE_MAPPER, &pwfx, threadID, 1, 0x20000);
    return  !wavein.result;
}
bool WaveIn::MessageThreadstartSuss() {
    if (hThread != 0)
        return true;
    return false;
}

DWORD __stdcall audioInputMSGLoop(LPVOID lpThreadParameter){

    MSG msg = {0,};
    if (GetMessageA(&msg, 0, 0, 0) == 0)
        return msg.wParam;

    do {
        HWAVEIN hwi = (HWAVEIN)msg.wParam;
        LPWAVEHDR pwh = (LPWAVEHDR)msg.lParam;
        if(g_recoding != true)
            return msg.wParam;

        if (msg.message == 0x3c0) {
            waveInUnprepareHeader(hwi, pwh, sizeof(WAVEHDR));
            if (pwh->dwBytesRecorded == BUF_SIZE) {
                memcpy(lpData, pwh->lpData, BUF_SIZE);

                std::ofstream outFile;
                //打开文件
                outFile.open("1.mp3",ios::binary| ios::app);
                outFile << lpData;
                outFile.close();
                waveInPrepareHeader(hwi, pwh, sizeof(WAVEHDR));
                waveInAddBuffer(hwi, pwh, sizeof(WAVEHDR));
            }
        }

    } while (GetMessageA(&msg, 0, 0, 0));


    return msg.wParam;
}


