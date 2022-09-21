// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>

void rc4_init(char* keyAry,  char* key, int len) {
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

int main()
{
    char key[10] = { 0x4D,0x6F ,0x74 ,0x68 ,0x65 ,0x72 ,0x33 ,0x36 ,0x30 ,0 };
    char keyAry[256];
    char data[1000] = { 0xCD,0x29,0x99,0xFE };
    rc4_init(keyAry, key, 10);
    
    rc4_cryp(keyAry, data, 4);

    rc4_init(keyAry, key, 10);
    rc4_cryp(keyAry, data, 4);
    int a = 0;
}


