#include "Sample_4_5.h"
Sample_4_5::Sample_4_5(QWidget *parent){
		this->ui.setUI(this);


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