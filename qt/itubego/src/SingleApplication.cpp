#include "SingleApplication.h"
#include "SingleApplicationPrivate.h"
#include <QSharedMemory>

SingleApplication::SingleApplication(int argc, char** argv,int arg_c) : QApplication{argc,argv} {
	m_d = new SingleApplicationPrivate(this);
	m_d->m_20 = arg_c;
	m_d->generateHash();
	m_d->m_sharedMemory  = new QSharedMemory(m_d->m_sha256, 0);
	if (m_d->m_sharedMemory->create(24, QSharedMemory::ReadWrite)) {
		m_d->m_sharedMemory->lock();
		m_d->sub_487080();
	}
	else {


	}

}