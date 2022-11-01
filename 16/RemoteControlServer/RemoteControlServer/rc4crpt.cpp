#include "rc4crpt.h"
void rc4_init(char* keyAry, char* key, int len) {
    int  data[256] = { 0, };
    int i = 0;
    do {
        keyAry[i] = i;
        data[i] = key[i % len];
        i++;
    } while (i < 256);

    int j = 0;
    int mod = 0;
    int temp = 0;
    do {

        mod += (unsigned char)keyAry[j] + data[j];
        mod %= 256;
        temp = keyAry[j];
        //printf("%X\n", mod);
        keyAry[j] = keyAry[mod];
        keyAry[mod] = temp;
        j++;
    } while (j < 256);
}

void rc4_cryp(char* keyAry, char* data, int len) {

    unsigned int i = 0, j = 0, k = 0, temp = 0;
    if (len > 0) {
        do {
            j++;
            j = j % 256;
            temp = (unsigned char)keyAry[j];
            k += temp;
            k %= 256;
            keyAry[j] = keyAry[k];
            keyAry[k] = temp;
            data[i] = data[i] ^ keyAry[((unsigned char)keyAry[j] + temp) % 256];
            i++;
        } while (i < len);
    }
}

