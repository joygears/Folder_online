#include <QWidget>
#include <QTimer>
#include "uiSample_4_5.h"
class Sample_4_5:public QWidget
{
	Q_OBJECT
public:
	Sample_4_5(QWidget *parent=nullptr);
private slots:
	void on_btnGetTime_clicked();
private:
	ui_Sample_4_5 ui; //0x30
	QTimer timer; //0x190
	int m_1b0;
};