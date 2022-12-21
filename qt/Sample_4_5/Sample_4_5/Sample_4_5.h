#pragma once

#include <QtWidgets/QWidget>
#include "ui_Sample_4_5.h"

class Sample_4_5 : public QWidget
{
    Q_OBJECT

public:
    Sample_4_5(QWidget *parent = Q_NULLPTR);

private:
    Ui::Sample_4_5Class ui;
};
