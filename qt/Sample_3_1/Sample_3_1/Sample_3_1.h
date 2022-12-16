#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_Sample_3_1.h"
#include "QPerson.h"
class Sample_3_1 : public QMainWindow
{
    Q_OBJECT

public:
    Sample_3_1(QWidget *parent = nullptr);
    ~Sample_3_1();
private slots:
    void on_btnGrowBoy_clicked();
    void on_btnGrowGirl_clicked();
    void on_spinBoxBoy_valueChanged(int value);
    void on_spinBoxGirl_valueChanged(int value);
    void on_AgeChanged(unsigned value);
    void on_btnMetaData_clicked();
private:
    Ui::Sample_3_1Class ui;
    QPerson *boy;
    QPerson* girl;
};
