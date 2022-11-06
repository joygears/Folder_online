#include "DiskInfoExtractor.h"

bool DiskInfoExtractor::isMatch()
{
    if (((char*)this->parsedData.getAddressOfIndex(0))[0] == 103) {
        return true;
    }
    
    return false;
}

diskinfo* DiskInfoExtractor::getDiskInfo()
{
   
    int i = 1,j = 0;
    while (i<this->parsedData.getDataLen()) {
        char * rootName = (char *)this->parsedData.getAddressOfIndex(i);
        info[j].lpRootPathName = rootName[0];
        i++;

        byte* driveType = (byte*)this->parsedData.getAddressOfIndex(i);
        info[j].driveType = driveType[0];
        i++;

        int* totalMBs = (int*)this->parsedData.getAddressOfIndex(i);
        info[j].totalMBs = *totalMBs;
        i += 4;

        int* FreeMBs = (int*)this->parsedData.getAddressOfIndex(i);
        info[j].FreeMBs = *FreeMBs;
        i += 4;

        char * szTypeName = (char*)this->parsedData.getAddressOfIndex(i);
        strcpy_s(info[j].typeName, MAX_PATH, szTypeName);
        i += strlen(szTypeName)+1;

        char* szFileSystemName = (char*)this->parsedData.getAddressOfIndex(i);
        strcpy_s(info[j].szFileSystemName, MAX_PATH, szFileSystemName);
        i += strlen(szFileSystemName)+1;
        j++;
    }
    diskCount = j;
    return info;
}
