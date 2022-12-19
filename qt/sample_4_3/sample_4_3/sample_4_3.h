#pragma once

#include <QtWidgets/QWidget>
#include "ui_sample_4_3.h"

class sample_4_3 : public QWidget
{
    Q_OBJECT

public:
    sample_4_3(QWidget *parent = nullptr);
    ~sample_4_3();
private slots:
    void on_btnCal_clicked();
    void on_btnDec_clicked();
    void on_btnBin_clicked();
    void on_btnHex_clicked();
private:
    Ui::sample_4_3Class ui;
};
