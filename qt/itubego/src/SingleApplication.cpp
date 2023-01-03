#include "SingleApplication.h"
#include "SingleApplicationPrivate.h"
#include <QSharedMemory>
#include <QTime>
#include <QThread>

SingleApplication::SingleApplication(int argc, char** argv,int arg_8,int arg_c,int arg_10) : QApplication{argc,argv} {
	m_d = new SingleApplicationPrivate(this);
	m_d->m_20 = arg_c;
	m_d->generateHash();
	m_d->m_sharedMemory  = new QSharedMemory(m_d->m_sha256, 0);
	if (m_d->m_sharedMemory->create(24, QSharedMemory::ReadWrite)) {
		
		
		m_d->m_sharedMemory->lock();
		m_d->initSharedMem();
		m_d->m_sharedMemory->unlock();
		

	}
	else {
		if (!m_d->m_sharedMemory->attach(QSharedMemory::ReadWrite)) {
			qCritical() << "SingleApplication: Unable to attach to shared memory block.";
			qCritical() << m_d->m_sharedMemory->errorString();
			exit();
		}
	}
	QTime time;
	sharememory * data = (sharememory*)m_d->m_sharedMemory->data();
	time.start();
	m_d->m_sharedMemory->lock();
	if (m_d->getMemCheckSum() != data->m_checkSum) {
		do {
			if (time.elapsed() > 5000) {
				qWarning() << "SingleApplication: Shared memory block has been in an inconsistent state from more than 5s. Assuming primary instance failure.";
				m_d->initSharedMem();
			}
			m_d->m_sharedMemory->unlock();
			qsrand(QDateTime::currentMSecsSinceEpoch() % -1);
			QThread::sleep((unsigned int)(qrand() / 32767.0 * 10.0));
			m_d->m_sharedMemory->lock();
		} while (m_d->getMemCheckSum() != data->m_checkSum);
	}
	if (data->m_0 == 0) {
		m_d->createServer();
	}
	else {
		if (arg_8 == 0) {
			m_d->m_sharedMemory->unlock();
			m_d->sub_486770(arg_10,1);
			m_d->sub_486610(1);
			exit(0);
		}
		data->m_4++;
		data->m_checkSum = m_d->getMemCheckSum();
		m_d->m_18 = data->m_4;
		if (m_d->m_20 & 4) {
			m_d->sub_486770(arg_10, 2);
		}
	}
	m_d->m_sharedMemory->unlock();
}

bool SingleApplication::notInitServer()
{
	return !m_d->m_server;
}

qint64 SingleApplication::getAppPID()
{
	m_d->m_sharedMemory->lock();
	sharememory* data = (sharememory*)m_d->m_sharedMemory->data();
	m_d->m_sharedMemory->unlock();
	return data->m_appPID;
}

bool SingleApplication::eventFilter(QObject* obj, QEvent* event)
{
	/*if (obj == this && event->type() == QEvent::ApplicationActivate && ((SingleApplication*)obj)->pMainWindow)  //等pMainWindow定义好，然后才能调用show
		((SingleApplication*)obj)->pMainWindow->show();*/
	QObject::eventFilter(obj, event);
	return false;
}
