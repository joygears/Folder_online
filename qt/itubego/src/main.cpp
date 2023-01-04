#include <QCoreApplication>
#include "SingleApplication.h"
#include <qDebug>
#include <Windows.h>
#include <QIcon>
#include "config.h"


int main(int argc,char ** argv){
	
	QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling, true); // …Ë÷√∏ﬂDPI
	SingleApplication a(argc, argv);
	QCoreApplication::setOrganizationName("LuckyDog Technology Limited.");
	QCoreApplication::setApplicationName("iTubeGo");
	QCoreApplication::setApplicationVersion("4.1.1");
	QGuiApplication::setQuitOnLastWindowClosed(false);
	if (a.notInitServer()) {
		AllowSetForegroundWindow(a.getAppPID());
		qDebug() << "app exit";
		exit(0);
	}
	a.installEventFilter(&a);
	QApplication::setWindowIcon(QIcon(":/res/appIcon.png"));
	qDebug() << "App dir path : " << QCoreApplication::applicationDirPath();
	preConfig();
	createLogPath();


	return 0;
}

