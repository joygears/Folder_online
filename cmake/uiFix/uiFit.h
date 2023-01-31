#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_uiFit.h"

class MyTabWidget;
class AboutWidget;
class TaskTable;

class uiFit : public QMainWindow
{
    Q_OBJECT

public:
    uiFit(QWidget *parent = nullptr);
    ~uiFit();

private:
    Ui::uiFitClass ui;
    MyTabWidget* tab;
    AboutWidget* about;
    TaskTable* table;
};
