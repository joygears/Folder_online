#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_sample_2_4.h"
#include <QProgressBar>
#include <QLabel>
#include <QSpinBox>
#include <QFontComboBox>


class sample_2_4 : public QMainWindow
{
    Q_OBJECT
private:
    QProgressBar *processBar;
    QLabel *label;
    QSpinBox* spinFontSize;
    QFontComboBox *fontComboBox;
    void init();
private slots:
    void on_actBold_triggered(bool checked);
    void on_actItalic_triggered(bool checked);
    void on_actUnderline_triggered(bool checked);
public:
    sample_2_4(QWidget *parent = Q_NULLPTR);

private:
    Ui::sample_2_4Class ui;
};
