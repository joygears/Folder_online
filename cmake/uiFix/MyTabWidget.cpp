#include "MyTabWidget.h"
#include <QToolBar>
#include <QHBoxLayout>
#include <QStackedWidget>
MyTabWidget::MyTabWidget(QWidget* parent):QWidget(parent){
	
	auto mainLayout = new QHBoxLayout(this);
	
	bar = new QToolBar(this);
	bar->setOrientation(Qt::Vertical);
	bar->setStyleSheet(
		"QToolBar{border-right:1px solid rgb(224,224,224);}"
		"QToolButton{padding:3px;border:none;margin-right:3px;}"
		"QToolButton:checked{background-color:rgb(232,232,232);}"
		"QToolButton:hover{background-color:rgb(232,232,232);}"
		"QToolButton:pressed{background-color:rgb(232,232,232);}"
	);

	stack = new QStackedWidget(this);
	group = new QActionGroup(this);
	group->setExclusive(true);
	
	mainLayout->addWidget(bar);
	mainLayout->addWidget(stack);
	this->setLayout(mainLayout);

	connect(bar, &QToolBar::actionTriggered, this, [stack = this->stack](QAction * act) {
		int idx = act->data().toInt();
		stack->setCurrentIndex(idx);
		});
	
}

void MyTabWidget::addTab(QWidget* widget, QString title)
{
	stack->addWidget(widget);

	int idx = stack->count() - 1;
	auto action = new QAction(title);
	action->setCheckable(true);
	action->setData(idx);
	if (idx == 0)
		action->setChecked(true);
	group->addAction(action);
	bar->addAction(action);

}
