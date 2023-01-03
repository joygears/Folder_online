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
	mem->m_appPID = -1;
	mem->m_checkSum = qChecksum((char *)m_sharedMemory->data(),16);
	return mem->m_checkSum;
}
quint16 SingleApplicationPrivate::getMemCheckSum()
{
	return qChecksum((char*)m_sharedMemory->data(), 16);
}
void SingleApplicationPrivate::createServer()
{
	QLocalServer::removeServer(m_sha256);
	m_server = new QLocalServer(0);
	m_server->setSocketOptions((m_20 & 1) != 0 ? QLocalServer::UserAccessOption : QLocalServer::WorldAccessOption);
	m_server->listen(m_sha256);
	connect(m_server, &QLocalServer::newConnection, this, &SingleApplicationPrivate::slotConnectionEstablished);
	sharememory * data = (sharememory*)m_sharedMemory->data();
	data->m_0 = true;
	data->m_appPID = QCoreApplication::applicationPid();
	data->m_checkSum = qChecksum((char*)m_sharedMemory->data(), 16);
}
void SingleApplicationPrivate::sub_486770(int arg_0, int arg_1)
{
}
void SingleApplicationPrivate::sub_486610(int arg_0)
{
}
void SingleApplicationPrivate::slotDataAvailable(QLocalSocket*, unsigned int data)
{


}

void SingleApplicationPrivate::slotClientConnectionClosed(QLocalSocket*, unsigned int)
{


}
