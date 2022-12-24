#include <QApplication>
#include "Sample_4_5.h"
int main(int argc,char ** argv){

	QApplication app(argc,argv);
	Sample_4_5 mainwindow;
	mainwindow.show();
	app.exec();
}