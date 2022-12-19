#pragma once

#include <QtWidgets/QWidget>
#include "ui__2_globalDefine.h"

class _2_globalDefine : public QWidget
{
    Q_OBJECT

public:
    _2_globalDefine(QWidget *parent = nullptr);
    ~_2_globalDefine();

private:
    Ui::_2_globalDefineClass ui;
};
