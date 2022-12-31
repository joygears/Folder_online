#include "Sample_4_5.h"
Sample_4_5::Sample_4_5(QWidget *parent){
		this->ui.setUI(this);
		timer.setInterval(1000);
		timer.stop();
		connect(&timer, &QTimer::timeout, this, &Sample_4_5::displayTime);
}

void Sample_4_5::on_btnGetTime_clicked(){
	QDateTime dataTime = QDateTime::currentDateTime();
	ui.timeEditCurrent->setDateTime(dataTime);
	
	ui.lineEditTime->setText(dataTime.toString("HH:mm:ss"));
	 ui.dateEdit->setDate(dataTime.date());
	
	 ui.lineEditDate->setText(dataTime.toString("yyyy-MM-dd"));
	ui.dateTimeEdit->setDateTime(dataTime);
	 ui.lineEditDateTime->setText(dataTime.toString("yyyy-MM-dd HH:mm:ss"));
}

void Sample_4_5::on_btnSetTime_clicked(){
	ui.timeEditCurrent->setTime(QTime::fromString(ui.lineEditTime->text(),"HH:mm:ss"));
}

void Sample_4_5::on_btnSetDate_clicked(){
	ui.dateEdit->setDate(QDate::fromString(ui.lineEditDate->text(),QString::fromLocal8Bit("yyyy-MM-dd",-1)));
}

void Sample_4_5::on_btnSetDateTime_clicked()
{
	QString text = this->ui.lineEditDateTime->text();
	QDateTime dateTime = QDateTime::fromString(text, "yyyy-MM-dd HH:mm:ss");
	this->ui.dateTimeEdit->setDateTime(dateTime);
}

void Sample_4_5::on_calendarWidget_selectionChanged()
{
	QDate date = this->ui.calendarWidget->selectedDate();
	
	QString dateStr = date.toString(QString::fromLocal8Bit("yyyy年MM月dd日"));
	
	this->ui.lineEditSelectedDate->setText(dateStr);
	
}

void Sample_4_5::on_btnSetInternal_clicked()
{
	int internal; // eax
	internal = this->ui.spinInternal->value();
	timer.setInterval(internal);
}

void Sample_4_5::on_btnStart_clicked()
{
	ui.btnStart->setEnabled(false);
	ui.btnSetInternal->setEnabled(false);
	ui.btnStop->setEnabled(true);
	
	timer.start();
	time.start();
}

void Sample_4_5::on_btnStop_clicked()
{
	ui.btnStart->setEnabled(true);
	ui.btnSetInternal->setEnabled(true);
	ui.btnStop->setEnabled(false);
	timer.stop();
	int v2 = time.elapsed();
	int v3 = v2 / 3600000;
	int v4 = v2 % 3600000 / 60000;
	int v5 = v2 % 3600000 % 60000 / 1000;
	
	QString v9 =QString::asprintf(QString::fromLocal8Bit("流逝时间: %d时%d分%d秒").toUtf8(), v3, v4, v5);
	this->ui.labelEcilpse->setText( v9);

}



void Sample_4_5::displayTime()
{
	int v3 = QTime::currentTime().hour();
	int v5 = QTime::currentTime().minute();
	int v7 = QTime::currentTime().second();

	this->ui.lcdHour->display(v3);
	this->ui.lcdMinute->display(v5);
	this->ui.lcdSecond->display( v7);
}

