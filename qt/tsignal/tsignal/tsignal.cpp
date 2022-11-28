#include "tsignal.h"
#include <QMessageBox>
TsignalApp::TsignalApp()
{
    // 将信号 mySignal() 与槽 mySlot() 相关联
    connect(this, SIGNAL(mySignal()), SLOT(mySlot()));
    // 将信号 mySignal(int) 与槽 mySlot(int) 相关联
    connect(this, SIGNAL(mySignal(int)), SLOT(mySlot(int)));
    // 将信号 mySignalParam(int,int) 与槽 mySlotParam(int,int) 相关联
    connect(this, SIGNAL(mySignalParam(int, int)), SLOT(mySlotParam(int, int)));
    
}
// 定义槽函数 mySlot()
void TsignalApp::mySlot()
{
    QMessageBox::about(this, "Tsignal", "This is a signal/slot sample withoutparameter.");
}
// 定义槽函数 mySlot(int)
void TsignalApp::mySlot(int x)
{
    QMessageBox::about(this, "Tsignal", "This is a signal/slot sample with oneparameter.");
}
// 定义槽函数 mySlotParam(int,int)
void TsignalApp::mySlotParam(int x, int y)
{
    char s[256];
    sprintf(s, "x:%d y:%d", x, y);
    QMessageBox::about(this, "Tsignal", s);
}
void TsignalApp::slotFileNew()
{
    // 发射信号 mySignal()
    emit mySignal();
    // 发射信号 mySignal(int)
    emit mySignal(5);
    // 发射信号 mySignalParam(5，100)
    emit mySignalParam(5, 100);
}