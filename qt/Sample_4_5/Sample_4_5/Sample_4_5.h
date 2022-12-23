#pragma once

#include <QtWidgets/QWidget>
#include "ui_Sample_4_5.h"

class Sample_4_5 : public QWidget
{
    Q_OBJECT

public:
    Sample_4_5(QWidget *parent = Q_NULLPTR);
private slots:
    void on_btnGetTime_clicked();
    void on_btnSetTime_clicked();
    void on_btnSetDate_clicked();
    void on_btnSetDateTime_clicked();
private:
    Ui::Sample_4_5Class ui;
};
