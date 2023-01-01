#include <QObject>
#include <QLocalSocket> 
#include <QSharedMemory>

class SingleApplication;
class SingleApplicationPrivate :public QObject {
	Q_OBJECT
public:
	SingleApplicationPrivate(SingleApplication * app);
	void generateHash();
	void sub_487080();
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

