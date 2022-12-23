#include "Sample_4_5.h"
#include <qDebug>
Sample_4_5::Sample_4_5(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);
    timer.setInterval(1000);
    timer.stop();
    connect(&timer, &QTimer::timeout, this, &Sample_4_5::displayTime);
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
    QDate time = QDate::fromString(strTime, QString::fromLocal8Bit("yyyy-MM-dd"));
    //将时间设置到时间编辑框
    ui.dateEdit->setDate(time);
}

void Sample_4_5::on_btnSetDateTime_clicked()
{
    //获取编辑框的文本
    QString strTime = ui.lineEditDateTime->text();
    //将文本转换为时间
    QDateTime time = QDateTime::fromString(strTime, "yyyy-MM-dd HH:mm:ss");
    //将时间设置到时间编辑框
    ui.dateTimeEdit->setDateTime(time);
}

void Sample_4_5::on_calendarWidget_selectionChanged()
{
    //获取日历被选中的时间
    QDate date = ui.calendarWidget->selectedDate();
    QString dataString = date.toString(QString::fromLocal8Bit("yyyy年MM月dd日"));
    ui.lineEditSelectedDate->setText(dataString);
    
}

void Sample_4_5::on_btnSetInternal_clicked()
{
    // 从spinInternal获取时间间隔
    int value = ui.spinInternal->value();
    //在QTime设置时间间隔
    timer.setInterval(value);
}

void Sample_4_5::on_btnStart_clicked()
{
    ui.btnStart->setEnabled(false);
    ui.btnSetInternal->setEnabled(false);
    ui.btnStop->setEnabled(true);

    //开启定时器
    timer.start();

    timeCount.start();
}

void Sample_4_5::on_btnStop_clicked()
{
    ui.btnStart->setEnabled(true);
    ui.btnSetInternal->setEnabled(true);
    ui.btnStop->setEnabled(false);
    timer.stop();
    int elapsed = timeCount.elapsed();
    int hour = elapsed / 3600000;
    elapsed -= 3600000 * hour;
    int minute = elapsed / 60000;
    elapsed -= minute * 60000;
    int second = elapsed/1000;

    ui.labelEcilpse->setText(QString::asprintf(QString::fromLocal8Bit("流逝时间: %d时%d分%d秒").toUtf8(), hour, minute, second));
}

void Sample_4_5::displayTime()
{
    //获取当前时间的时分秒
    int hour = QTime::currentTime().hour();
    int minute = QTime::currentTime().minute();
    int second = QTime::currentTime().second();
    // 设置时分秒的LCDNumber
    ui.lcdHour->display(hour);
    ui.lcdMinute->display(minute);
    ui.lcdSecond->display(second);

}

