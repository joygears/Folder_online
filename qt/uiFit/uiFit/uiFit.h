#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_uiFit.h"

class uiFit : public QMainWindow
{
    Q_OBJECT

public:
    uiFit(QWidget *parent = nullptr);
    ~uiFit();

private:
    Ui::uiFitClass ui;
};
