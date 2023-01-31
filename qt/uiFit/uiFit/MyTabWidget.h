#pragma once
#include <QWidget>
class QToolBar;
class  QStackedWidget;
class MyTabWidget :public QWidget
{
	Q_OBJECT
public:
	MyTabWidget(QWidget* parent = nullptr);
private:
	QToolBar* bar;
	QStackedWidget* stack;
};

