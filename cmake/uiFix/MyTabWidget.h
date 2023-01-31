#pragma once
#include <QWidget>
class QToolBar;
class  QStackedWidget;
class QActionGroup;
class MyTabWidget :public QWidget
{
	Q_OBJECT
public:
	MyTabWidget(QWidget* parent = nullptr);
	void addTab(QWidget* widget, QString title);
private:
	QToolBar* bar;
	QStackedWidget* stack;
	QActionGroup* group;
};

