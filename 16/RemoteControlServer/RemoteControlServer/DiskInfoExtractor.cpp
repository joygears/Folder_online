#include "DiskInfoExtractor.h"

bool DiskInfoExtractor::isMatch()
{
    if (((char*)this->parsedData.getAddressOfIndex(0))[0] == 103) {
        return true;
    }
    
    return false;
}
