#pragma once

#include <QtWidgets/QWidget>
#include "ui_sample_4_2.h"

class sample_4_2 : public QWidget
{
    Q_OBJECT

public:
    sample_4_2(QWidget *parent = nullptr);
    ~sample_4_2();
private slots:
    void on_btnAppend_clicked();
    void on_btnPrepend_clicked();
    void on_btnCount_clicked();
    void on_btnEnds_clicked();
    void on_btnTrimmed_clicked();
    void on_btnSimple_clicked();
    void on_btnIndexOf_clicked();
    void on_btnLastIndexOf_clicked();
    void on_btnIsNull_clicked();
    void on_btnIsEmpty_clicked();
private:
    Ui::sample_4_2Class ui;
};
