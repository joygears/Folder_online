#include <QWidget>
#include <QTimer>
#include "uiSample_4_5.h"
class Sample_4_5:public QWidget
{
	Q_OBJECT
public:
	Sample_4_5(QWidget *parent=nullptr);
private slots:
	void on_btnGetTime_clicked(); // method index==0
	void on_btnSetTime_clicked(); // method index==1
	void on_btnSetDate_clicked(); // method index==2
	void on_btnSetDateTime_clicked(); // method index==3
	void  on_calendarWidget_selectionChanged(); // method index==4
	void  on_btnSetInternal_clicked(); // method index==5
	void  on_btnStart_clicked();
	void  on_btnStop_clicked();
	void displayTime();
private:
	ui_Sample_4_5 ui; //0x30
	QTimer timer; //0x190
	QTime time;
};