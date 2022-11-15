// getAudio.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <Windows.h>

#define BUF_SIZE 960


DWORD __stdcall audioInputMSGLoop(LPVOID lpThreadParameter);
bool MessageThreadstartSuss();
bool openWaveIn();

class WaveIn;

bool g_recoding = false;
byte lpData[BUF_SIZE];
WaveIn wavein;

int main()
{
    
    wavein.hThread =  CreateThread(0, 0, audioInputMSGLoop, 0, 0, &wavein.threadID);
    g_recoding = true;
    if (MessageThreadstartSuss() == false)
        return 0;
    if (openWaveIn() == true) {

    }

}

bool addBufToWavaIn() {


}
bool openWaveIn() {
    WAVEFORMATEX pwfx;
    pwfx.nChannels = wavein.nChannels;
    pwfx.nSamplesPerSec = wavein.nSamplesPerSec;
    pwfx.wBitsPerSample = wavein.wBitsPerSample;
    pwfx.wFormatTag = WAVE_FORMAT_PCM;
    pwfx.nAvgBytesPerSec = wavein.nSamplesPerSec * wavein.wBitsPerSample * wavein.nChannels / 8;
    pwfx.nBlockAlign = wavein.wBitsPerSample * wavein.nChannels / 8;

    wavein.result = waveInOpen(NULL, -1, &pwfx, NULL, NULL, 1);
    if (wavein.result != 0)
        return 0;
    wavein.result = waveInOpen(&wavein.hwi, WAVE_MAPPER, &pwfx, wavein.threadID, 1, 0x20000);
    return  !wavein.result;
}
bool MessageThreadstartSuss() {
    if (wavein.hThread != 0)
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
                waveInPrepareHeader(hwi, pwh, sizeof(WAVEHDR));
                waveInAddBuffer(hwi, pwh, sizeof(WAVEHDR));
            }
        }

    } while (GetMessageA(&msg, 0, 0, 0));


    return msg.wParam;
}


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
};