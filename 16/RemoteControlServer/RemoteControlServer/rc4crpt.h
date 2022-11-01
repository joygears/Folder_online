#pragma once

void rc4_init(char* keyAry, char* key, int len);
void rc4_cryp(char* keyAry, char* data, int len);