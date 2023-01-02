#include <QObject>
#include <QLocalSocket> 
#include <QSharedMemory>

class SingleApplication;
class SingleApplicationPrivate :public QObject {
	Q_OBJECT
public:
	SingleApplicationPrivate(SingleApplication * app);
	void generateHash();
	quint16 initSharedMem();
	quint16 getMemCheckSum();
public slots:
	void slotConnectionEstablished();
	void slotDataAvailable(QLocalSocket*,unsigned int);
	void slotClientConnectionClosed(QLocalSocket*,unsigned int);
public:
	SingleApplication* m_app; // 8
	QSharedMemory*m_sharedMemory; //c
	int m_10; //10
	int m_14; //14
	int m_18 = -1; //18
	QString m_sha256; //1c;
	int m_20; //20
	int m_map; // 24
};

struct sharememory {
	bool m_0;
	int m_4;
	int m_8;
	int m_c;
	quint16 m_checkSum;
};