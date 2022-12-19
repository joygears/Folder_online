#include "_2_globalDefine.h"
#include <QtWidgets/QApplication>
#include <qDebug>
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    /*_2_globalDefine w;
    w.show();*/
    QList<QString> List;
    List.append("Monday");
    List.append("Tuesday");
    List.append("Wednesday");
    QString str = List[0];
    qDebug() << str;
    return a.exec();
}
