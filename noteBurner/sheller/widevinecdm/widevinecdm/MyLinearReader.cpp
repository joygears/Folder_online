#include <Windows.h>
#include <sstream>
#include "MyLinearReader.h"
#include <bento4/Ap4SencAtom.h>
#include "MySampleReader.h"
#include "MySampleDecrypter.h"
#include "widevinecdm.h"
#include "webNetwork.h"
MyLinearReader::MyLinearReader(AP4_Movie& movie, AP4_ByteStream* fragment_stream ):AP4_LinearReader(movie, fragment_stream) {

	
}
AP4_Result MyLinearReader::ProcessMoof(AP4_ContainerAtom* moof, AP4_Position moof_offset, AP4_Position mdat_payload_offset)
{
	curSegIndex++;

	stringstream ss;
	ss.setf(ios::fixed);
	ss << "decryptProgress:" << curSegIndex / segCount;
	sendMessage(ss.str());
	if (!this->AP4_LinearReader::ProcessMoof(moof, moof_offset, mdat_payload_offset)) {
		
		MySampleDecrypter* decrypter = nullptr;
		
		moof = 0;
		AP4_TfhdAtom* tfhd = 0;
		AP4_TrexAtom* trex = 0;
		this->m_Fragment->GetTrafAtom(this->m_Trackers[0]->m_Track->GetId(), moof);
		if (moof) {
			tfhd = dynamic_cast<AP4_TfhdAtom*>(moof->GetChild(AP4_ATOM_TYPE_TFHD));
			AP4_MoovAtom* m_MoovAtom = this->m_Movie.GetMoovAtom();
			AP4_ContainerAtom * mvex = dynamic_cast<AP4_ContainerAtom*>(m_MoovAtom->GetChild(AP4_ATOM_TYPE_MVEX));
			if(trex)
				trex = dynamic_cast<AP4_TrexAtom*>(mvex->GetChild(AP4_ATOM_TYPE_TREX));
		}
		int index = 0;
		if (trex)
			index = trex->GetDefaultSampleDescriptionIndex();
		if (tfhd && (tfhd->GetFlags() & 2 )!= 0) {
			index = tfhd->GetSampleDescriptionIndex();
		}
		if (index) {
			index--;
		}
	
			
		AP4_SampleDescription* sdescription = this->m_Trackers[0]->m_Track->GetSampleDescription(index);
		AP4_UI32 timeScale  = this->m_Trackers[0]->m_Track->GetMovieTimeScale();
		if (sdescription->GetType() == AP4_SampleDescription::Type::TYPE_PROTECTED) {

			AP4_ProtectedSampleDescription* ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(sdescription);
			AP4_ProtectionSchemeInfo* SchemeInfo = ProtectedSampleDescription->GetSchemeInfo();
			AP4_ContainerAtom* SchiAtom = SchemeInfo->GetSchiAtom();
			AP4_CencTrackEncryption* cenc = dynamic_cast<AP4_CencTrackEncryption*>(SchiAtom->GetChild(AP4_ATOM_TYPE_TENC));
			EncryptionScheme protectedType = (EncryptionScheme)(ProtectedSampleDescription->GetSchemeType() == 0x63656E63 ? EncryptionScheme::kCenc : EncryptionScheme::kCbcs);
			if (!cenc) {

				//SchiAtom->GetChild()  100D8019
			}
			const AP4_UI08* kid = cenc->GetDefaultKid();
			AP4_SencAtom* SencAtom = dynamic_cast<AP4_SencAtom*>(moof->GetChild(AP4_ATOM_TYPE_SENC));
			
			AP4_CencSampleEncryption* CencSampleEncryption = (AP4_CencSampleEncryption*)(((char*)SencAtom) + 0x28);
			AP4_CencSampleInfoTable* table = 0;
			AP4_UI08 m_DefaultCryptByteBlock = 0;
			AP4_UI08 m_DefaultSkipByteBlock = 0;
			if (!CencSampleEncryption || (CencSampleEncryption->GetOuter().GetFlags() & 1)==0){
				AP4_UI08 DefaultPerSampleIvSize = cenc->GetDefaultPerSampleIvSize();
				AP4_UI08 m_DefaultConstantIvSize = cenc->GetDefaultConstantIvSize();
				 m_DefaultCryptByteBlock = cenc->GetDefaultCryptByteBlock();
				 m_DefaultSkipByteBlock = cenc->GetDefaultSkipByteBlock();
				const AP4_UI08* m_DefaultConstantIv = 0;
				if (m_DefaultConstantIvSize) {
					m_DefaultConstantIv = cenc->GetDefaultConstantIv();
				}
				if (CencSampleEncryption) {
					CencSampleEncryption->CreateSampleInfoTable(0, m_DefaultCryptByteBlock, m_DefaultSkipByteBlock, DefaultPerSampleIvSize, m_DefaultConstantIvSize, m_DefaultConstantIv, table);
				}
			}
			
			
			decrypter = new MySampleDecrypter(kid, 16, table, timeScale, m_DefaultCryptByteBlock, m_DefaultSkipByteBlock, protectedType);
		}
		else {
			decrypter = new MySampleDecrypter(0, 16, 0, timeScale, 0, 0, EncryptionScheme::kUnencrypted);
		}

		this->m_Trackers[0]->m_Reader = new MySampleReader(decrypter);
		
	}
	return AP4_Result();
}
