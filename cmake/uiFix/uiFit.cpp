#include "uiFit.h"
#include "MyTabWidget.h"
#include "TaskTable.h"
#include "AboutWidget.h"
uiFit::uiFit(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);
    
    tab = new MyTabWidget;
   

    table = new TaskTable;
    about = new AboutWidget;
    tab->addTab(table, QString::fromLocal8Bit("正在下载"));
    tab->addTab(about, QString::fromLocal8Bit("关于"));

    this->setStyleSheet("QMainWindow{background-color: white;}");
    ui.centralWidget->layout()->addWidget(tab);
}

uiFit::~uiFit()
{}
