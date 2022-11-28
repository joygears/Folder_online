#include "tsignal.h"
#include <QApplication>

int main(int argc, char* argv[])
{
    QApplication a(argc, argv);
    TsignalApp w;
    w.slotFileNew();
    return a.exec();
}