#include <iostream>
#include <bento4/Ap4.h>
#include "bento4/Ap4Atom.h"


int main() {

	AP4_ByteStream* input_stream = NULL;
	AP4_Result result = AP4_FileByteStream::Create(R"(D:\Users\Downloads\0-44462.mp4)",
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





	return 0;
}
