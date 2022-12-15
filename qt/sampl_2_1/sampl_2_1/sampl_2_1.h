#pragma once

#include <QtWidgets/QDialog>
#include "ui_sampl_2_1.h"

class sampl_2_1 : public QDialog
{
    Q_OBJECT

public:
    sampl_2_1(QWidget *parent = Q_NULLPTR);

private:
    Ui::sampl_2_1Class ui;
};
