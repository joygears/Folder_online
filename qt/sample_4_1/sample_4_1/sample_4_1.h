#pragma once

#include <QtWidgets/QWidget>
#include "ui_sample_4_1.h"

class sample_4_1 : public QWidget
{
    Q_OBJECT

public:
    sample_4_1(QWidget *parent = Q_NULLPTR);
private slots:
    void on_btnCal_clicked();
    void on_btnTenHex_clicked();
    void on_btnTwoHex_clicked();
    void on_btnHex_clicked();
private:
    Ui::sample_4_1Class ui;
};
