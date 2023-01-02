#include "SingleApplicationPrivate.h"
#include "SingleApplication.h"
#include <QCryptographicHash>
#include <Windows.h>
SingleApplicationPrivate::SingleApplicationPrivate(SingleApplication* app){
	m_app = app;
}
void SingleApplicationPrivate::slotConnectionEstablished() {


}

void SingleApplicationPrivate::generateHash()
{
	TCHAR userName[257] = {0,};
	DWORD len = 257;
	QCryptographicHash cryptographicHash(QCryptographicHash::Sha256);
	cryptographicHash.addData("SingleApplication",17);
	cryptographicHash.addData(QCoreApplication::applicationName().toUtf8());
	cryptographicHash.addData(QCoreApplication::organizationName().toUtf8());
	cryptographicHash.addData(QCoreApplication::organizationDomain().toUtf8());
	
	if ((m_20 & 8) == 0)
		cryptographicHash.addData(QCoreApplication::applicationVersion().toUtf8());
	if ((m_20 & 16) == 0)
		cryptographicHash.addData(QCoreApplication::applicationFilePath().toLower().toUtf8());
	if ((m_20 & 1) != 0)
		if (GetUserNameW(userName, &len))
			cryptographicHash.addData(QString::fromWCharArray(userName).toLower().toUtf8());
		else
			cryptographicHash.addData(qgetenv("USERNAME"));
	m_sha256 = cryptographicHash.result().toBase64().replace("/", "_");
		
	
}


quint16  SingleApplicationPrivate::initSharedMem()
{
	sharememory*  mem = (sharememory*)m_sharedMemory->data();
	mem->m_0 = false;
	mem->m_4 = 0;
	mem->m_8 = -1;
	mem->m_c = -1;
	mem->m_checkSum = qChecksum((char *)m_sharedMemory->data(),16);
	return mem->m_checkSum;
}
quint16 SingleApplicationPrivate::getMemCheckSum()
{
	return qChecksum((char*)m_sharedMemory->data(), 16);
}
void SingleApplicationPrivate::slotDataAvailable(QLocalSocket*, unsigned int data)
{


}

void SingleApplicationPrivate::slotClientConnectionClosed(QLocalSocket*, unsigned int)
{


}
