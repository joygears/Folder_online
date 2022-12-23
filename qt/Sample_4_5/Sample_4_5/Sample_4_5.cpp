#include "Sample_4_5.h"
#include <qDebug>
Sample_4_5::Sample_4_5(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);
    
}

void Sample_4_5::on_btnGetTime_clicked()
{
    QDateTime curDataTime = QDateTime::currentDateTime();
    ui.timeEditCurrent->setDateTime(curDataTime);
    ui.lineEditTime->setText(curDataTime.toString("HH:mm:ss"));
    ui.dateEdit->setDate(curDataTime.date());
    ui.lineEditDate->setText(curDataTime.toString("yyyy-MM-dd"));
    ui.dateTimeEdit->setDateTime(curDataTime);
    ui.lineEditDateTime->setText(curDataTime.toString("yyyy-MM-dd HH:mm:ss"));
    
}

void Sample_4_5::on_btnSetTime_clicked()
{
    //获取编辑框的文本
    QString strTime = ui.lineEditTime->text();
    //将文本转换为时间
    QTime time = QTime::fromString(strTime, "HH:mm:ss");
    //将时间设置到时间编辑框
    ui.timeEditCurrent->setTime(time);
}

void Sample_4_5::on_btnSetDate_clicked()
{
    //获取编辑框的文本
    QString strTime = ui.lineEditDate->text();
    //将文本转换为时间
    QTime time = QTime::fromString(strTime, QString::fromLocal8Bit("yyyy-MM-dd"));
    //将时间设置到时间编辑框
    ui.dateEdit->setTime(time);
}

void Sample_4_5::on_btnSetDateTime_clicked()
{
    //获取编辑框的文本
    QString strTime = ui.lineEditDateTime->text();
    //将文本转换为时间
    QTime time = QTime::fromString(strTime, "yyyy-MM-dd HH:mm:ss");
    //将时间设置到时间编辑框
    ui.dateTimeEdit->setTime(time);
}
