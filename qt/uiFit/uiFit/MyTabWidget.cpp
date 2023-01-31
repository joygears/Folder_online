#include "MyTabWidget.h"
#include <QToolBar>
#include <QHBoxLayout>
MyTabWidget::MyTabWidget(QWidget* parent):QWidget(parent){
	
	auto mainLayout = new QHBoxLayout(this);
	
	bar = new QToolBar(this);
	bar->setOrientation(Qt::Vertical);
	bar->setStyleSheet(R"(
		"QToolBar{border-right:1px solid rgb(224,224,224);}"
        "QToolButton{padding:3px;border:none;margin-right:3px;}"
        "QToolButton:checked{background-color:rgb(232,232,232);}"
        "QToolButton:hover{background-color:rgb(232,232,232);}"
        "QToolButton:pressed{background-color:rgb(232,232,232);}"
	}
)");


	mainLayout->addWidget(bar);
	this->setLayout(mainLayout);
	
}