#include <iostream>
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"
#include <map>
int __cdecl transToVideoProfile(char a1);

int main() {

	AP4_ByteStream* input_stream = NULL;
	AP4_Result result = AP4_FileByteStream::Create(R"(0-44306.mp4)",
		AP4_FileByteStream::STREAM_MODE_READ,
		input_stream);

	if (result != AP4_SUCCESS || input_stream == nullptr) {
		// 处理文件打开错误
		return result;
	}
	AP4_File file(*input_stream);
	AP4_Movie* movie = file.GetMovie();
	
	AP4_MoovAtom* moovAtom = movie->GetMoovAtom();
	if (moovAtom == nullptr) {
		// 处理 MoovAtom 获取错误
		return result;
	}


	AP4_List<AP4_Atom>::Item* currentItem = (AP4_List<AP4_Atom>::Item*) * (int*)((char*)moovAtom + 0x34);
	while (currentItem) {

		if (currentItem->GetData()->GetType() == AP4_ATOM_TYPE_PSSH) {
			AP4_PsshAtom* PsshAtom = dynamic_cast<AP4_PsshAtom*>(currentItem->GetData());
			AP4_DataBuffer  Ap4DataBuffer = PsshAtom->GetData();


		}
		currentItem = currentItem->GetNext();
	}


	AP4_Cardinal track_count = movie->GetTracks().ItemCount();
	if (!track_count)
		return 1600;
	AP4_ProtectedSampleDescription* ProtectedSampleDescription;
	AP4_Track* pTrack;
	while (1) {

		AP4_List<AP4_Track>::Item* item = movie->GetTracks().FirstItem();
		pTrack = item->GetData();
		if (!pTrack)
			return 1600;
		AP4_SampleDescription * SampleDescription = pTrack->GetSampleDescription(0);
		if (SampleDescription && SampleDescription->GetType() != AP4_SampleDescription::Type::TYPE_PROTECTED) {
			//处理未加密的track流
		}
		else {
			 ProtectedSampleDescription = dynamic_cast<AP4_ProtectedSampleDescription*>(SampleDescription);
			if (ProtectedSampleDescription)
				break;
		}
	}
	AP4_UI32 schemeType = ProtectedSampleDescription->GetSchemeType();
	if (schemeType == 0x63656E63
		|| schemeType == 0x63626331
		|| schemeType == 0x63656E73
		|| schemeType == 0x63626373
		|| schemeType == 0x70696666)
	{
		printf("protection scheme type: %u\n", schemeType);
	}
	else
	{
		printf("unhandled protection scheme type: %u\n", schemeType);
	}

	AP4_SampleDescription* OriginalSampleDescription = ProtectedSampleDescription->GetOriginalSampleDescription();
	char* format;
	AP4_String codec;
	if (OriginalSampleDescription) {
		format = (char *)AP4_GetFormatName(OriginalSampleDescription->GetFormat());
		OriginalSampleDescription->GetCodecString(codec);

		printf( "format:%s, codec:%s, type:%d \n", format, codec.GetChars(), OriginalSampleDescription->GetType());
	}
	AP4_Atom::Type trackType = pTrack->GetType();
	if (trackType != AP4_Track::TYPE_AUDIO ) {
		if(trackType != AP4_Track::TYPE_VIDEO)
		return 1600;
		AP4_VideoSampleDescription* VideoSampleDescription = dynamic_cast<AP4_VideoSampleDescription*>(OriginalSampleDescription);
		AP4_UI16 width = VideoSampleDescription->GetWidth();
		AP4_UI16 hegiht = VideoSampleDescription->GetHeight();
		std:: string codecStr = codec.GetChars();
		if (codecStr.find("avc1",0) == std::string::npos) {

			if(codecStr.find("vp09",0) == std::string::npos)
				printf( "codec %s not yet handled ", codecStr.c_str());
			/*video_decoder_config[1] = 1;
			video_decoder_config[0] = 3;
			video_decoder_config[2] = 2;*/
		
		}
		else {
			AP4_AvcSampleDescription * AvcSampleDescription = dynamic_cast<AP4_AvcSampleDescription*>(OriginalSampleDescription);
			AP4_UI08 profile = AvcSampleDescription->GetProfile();
			AP4_UI08 level = AvcSampleDescription->GetLevel();
			int videoProfile = transToVideoProfile(profile);
			
		}

	}
	
	AP4_List<AP4_Atom>::Item*  curItem = file.GetTopLevelAtoms().FirstItem();
	AP4_List<AP4_TrakAtom>::Item* trakAtomitem =  moovAtom->GetTrakAtoms().FirstItem();
	AP4_TrakAtom* trakAtom = trakAtomitem->GetData();
	 AP4_MdhdAtom* MdhdAtom = (AP4_MdhdAtom*)*(int*)((char*)trakAtom + 0x44);
	 AP4_UI32  TimeScale = MdhdAtom->GetTimeScale();

	 while (curItem) {

		 if (curItem->GetData()->GetType() == AP4_ATOM_TYPE_SIDX) {
			 AP4_SidxAtom* SidxAtom = dynamic_cast<AP4_SidxAtom*>(curItem->GetData());
			
			
		 }
		 else if (curItem->GetData()->GetType() == AP4_ATOM_TYPE_SSIX) {
			 
		 }
		 curItem = curItem->GetNext();
	 }



	 AP4_ByteStream* input_stream2 = NULL;
	  result = AP4_FileByteStream::Create(R"(0-44306.mp4)",
		 AP4_FileByteStream::STREAM_MODE_READ,
		  input_stream2);

	 AP4_AtomFactory factory;
	 AP4_Atom * currentAtom;
	 AP4_SidxAtom* SidxAtom = 0;;
	 AP4_LargeSize size = 0;
	 AP4_Position pos = 0;
	 AP4_UI64 FirstOffset = 0;
	 while (!factory.CreateAtomFromStream(*input_stream2, currentAtom)) {

		 if (currentAtom->GetType() == AP4_ATOM_TYPE_SIDX) {
			 SidxAtom = dynamic_cast<AP4_SidxAtom*>(currentAtom);
			 size = SidxAtom->GetSize();
			 FirstOffset = SidxAtom->GetFirstOffset();
			 SidxAtom->GetReferences();
			 break;
		 }
		 else if (currentAtom->GetType() == AP4_ATOM_TYPE_SSIX) {

		 }
		 input_stream2->Tell(pos);
	 }

	 AP4_UI64 segPos = pos + size + FirstOffset;

	 const AP4_Array<AP4_SidxAtom::Reference>& References = SidxAtom->GetReferences();
	 std::map<AP4_UI32, AP4_UI32> segs;
	 AP4_UI32 curOffset = segPos;
	 AP4_UI32 segsSize = 0;
	 for (int i = 0; i < References.ItemCount(); i++) {
		 segsSize += References[i].m_ReferencedSize;
		if (segsSize >= 0x100000)
		 {
			segs[curOffset] = segsSize;
			 printf("seg  offset %d  length %d\n", curOffset, segsSize);
			 curOffset += segsSize;
			 segsSize = 0;
			 
		 }
	 }

	 AP4_ByteStream* input_stream3 = NULL;
	 result = AP4_FileByteStream::Create(R"(44306-1993788.mp4)",
		 AP4_FileByteStream::STREAM_MODE_READ,
		 input_stream3);
	 AP4_Sample sample;
	 AP4_DataBuffer sample_data;
	 
	 AP4_LinearReader LinearReader(*movie, input_stream3);
	 LinearReader.EnableTrack(pTrack->GetId());
	 AP4_ByteStream* m_FragmentStream = *(AP4_ByteStream**)(((char*)&LinearReader) + 0x14);
	 AP4_Atom *pAtom;
	 AP4_AtomFactory factory2;
	 factory2.CreateAtomFromStream(*m_FragmentStream, pAtom);
	 AP4_ContainerAtom* moov = dynamic_cast<AP4_ContainerAtom*>(pAtom);
	 //LinearReader.ReadNextSample(pTrack->GetId(), sample, sample_data);
	 
	return 0;
}



int __cdecl transToVideoProfile(char a1)
{
	int result; // eax

	switch (a1)
	{
	case 66:
		result = 2;
		break;
	case 77:
		result = 3;
		break;
	case 88:
		result = 4;
		break;
	case 100:
		result = 5;
		break;
	case 110:
		result = 6;
		break;
	case 122:
		result = 7;
		break;
	case -112:
		result = 8;
		break;
	default:
		result = 0;
		break;
	}
	return result;
}