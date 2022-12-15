#include "sample_2_4.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    sample_2_4 w;
    w.show();

    QObject* obj = new sample_2_4;
    QMainWindow* widget = qobject_cast<QMainWindow*>(obj);
    sample_2_4 * myWidget = qobject_cast<sample_2_4*>(widget);
    QLabel* label = qobject_cast<QLabel*>(myWidget);

    return a.exec();
}
