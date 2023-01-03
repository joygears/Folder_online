#include <QObject>
#include <QLocalSocket> 
#include <QSharedMemory>
#include <QLocalServer>
class SingleApplication;
class SingleApplicationPrivate :public QObject {
	Q_OBJECT
public:
	SingleApplicationPrivate(SingleApplication * app);
	void generateHash();
	quint16 initSharedMem();
	quint16 getMemCheckSum();
	void createServer();
	void sub_486770(int arg_0, int arg_1);
	void sub_486610(int arg_0);
public slots:
	void slotConnectionEstablished();
	void slotDataAvailable(QLocalSocket*,unsigned int);
	void slotClientConnectionClosed(QLocalSocket*,unsigned int);
public:
	SingleApplication* m_app; // 8
	QSharedMemory*m_sharedMemory; //c
	int m_10; //10
	QLocalServer* m_server; //14
	int m_18 = -1; //18
	QString m_sha256; //1c;
	int m_20; //20
	int m_map; // 24
};

struct sharememory {
	bool m_0;
	int m_4;
	quint64 m_appPID;
	
	quint16 m_checkSum;
};