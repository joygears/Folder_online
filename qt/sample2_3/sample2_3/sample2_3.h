#pragma once

#include <QtWidgets/QDialog>
#include "ui_sample2_3.h"
#include "myUI.h"
class sample2_3 : public QDialog
{
    Q_OBJECT

public:
    sample2_3(QWidget *parent = nullptr);
    ~sample2_3();
    private slots:
        void setTextColor();
private:
    Ui::sample2_3Class ui;
    myUI mui;
};
