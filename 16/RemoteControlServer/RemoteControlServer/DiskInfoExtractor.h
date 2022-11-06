#pragma once
#include "DataExtractor.h"



class diskinfo {
public:
    char lpRootPathName;
    byte  driveType;
    int totalMBs;
    int FreeMBs;
    char  typeName[MAX_PATH];
    char szFileSystemName[MAX_PATH];
};

class DiskInfoExtractor :
    public DataExtractor
{
public :
    bool isMatch();
    diskinfo* getDiskInfo();

    diskinfo info[MAX_PATH];
    int diskCount;
};

