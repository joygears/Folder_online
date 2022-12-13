#include "sample2_3.h"

sample2_3::sample2_3(QWidget *parent)
    : QDialog(parent)
{
    ui.setupUi(this);
    mui.setUI(this);

    //connect(, &QAbstractButton::clicked, this, &sample2_3::setTextColor);
}

sample2_3::~sample2_3()
{}

void sample2_3::setTextColor() {

}
