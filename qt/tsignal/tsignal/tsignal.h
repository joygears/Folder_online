#pragma once

#include <QMainWindow>
#include <QObject>
// 必须继承QObject才能使用信号和槽
class TsignalApp :public QMainWindow
{
public:
    TsignalApp();
    void slotFileNew();
    Q_OBJECT
        // 信号声明区
signals:
    // 声明信号 mySignal()
    void mySignal();
    // 声明信号 mySignal(int)
    void mySignal(int x);
    // 声明信号 mySignalParam(int,int)
    void mySignalParam(int x, int y);
    // 槽声明区
public slots:
    // 声明槽函数 mySlot()
    void mySlot();
    // 声明槽函数 mySlot(int)
    void mySlot(int x);
    // 声明槽函数 mySignalParam (int，int)
    void mySlotParam(int x, int y);
   // TsignalApp* mySlot2();
};