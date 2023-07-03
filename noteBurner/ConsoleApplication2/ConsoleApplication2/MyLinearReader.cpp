#include "MyLinearReader.h"


MyLinearReader::MyLinearReader(AP4_Movie& movie, AP4_ByteStream* fragment_stream ):AP4_LinearReader(movie, fragment_stream) {

	
}
AP4_Result MyLinearReader::ProcessMoof(AP4_ContainerAtom* moof, AP4_Position moof_offset, AP4_Position mdat_payload_offset)
{
	if (!this->AP4_LinearReader::ProcessMoof(moof, moof_offset, mdat_payload_offset)) {
		AP4_SampleDescription* sdescription = this->m_Trackers[0]->m_Track->GetSampleDescription(1);
		if (sdescription->GetType() == AP4_SampleDescription::Type::TYPE_PROTECTED) {
			printf("");
		}
	}
	return AP4_Result();
}
