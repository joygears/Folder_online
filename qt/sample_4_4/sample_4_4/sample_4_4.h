#pragma once

#include <QtWidgets/QWidget>
#include "ui_sample_4_4.h"

class sample_4_4 : public QWidget
{
    Q_OBJECT

public:
    sample_4_4(QWidget *parent = nullptr);
    ~sample_4_4();
private slots:
    void on_sliderRed_valueChanged(int value);
private:
    Ui::sample_4_4Class ui;
};
