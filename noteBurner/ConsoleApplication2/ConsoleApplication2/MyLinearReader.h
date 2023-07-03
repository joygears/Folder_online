#pragma once
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"
class MyLinearReader :
    public AP4_LinearReader
{
  
public:

    MyLinearReader(AP4_Movie& movie, AP4_ByteStream* fragment_stream = NULL);
    virtual AP4_Result ProcessMoof(AP4_ContainerAtom* moof,
        AP4_Position       moof_offset,
        AP4_Position       mdat_payload_offset);

};

