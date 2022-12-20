#include "sample_4_4.h"

sample_4_4::sample_4_4(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);
    connect(ui.sliderGreen, &QSlider::valueChanged, this, &sample_4_4::on_sliderRed_valueChanged);
    connect(ui.sliderBlue, &QSlider::valueChanged, this, &sample_4_4::on_sliderRed_valueChanged);
    connect(ui.sliderAlpha, &QSlider::valueChanged, this, &sample_4_4::on_sliderRed_valueChanged);
}

sample_4_4::~sample_4_4()
{}

void sample_4_4::on_sliderRed_valueChanged(int value)
{
    QPalette pal = ui.editColor->palette();
    QColor color;
   color.setRgb(ui.sliderRed->value(), ui.sliderGreen->value(), ui.sliderBlue->value(), ui.sliderAlpha->value());
   pal.setColor(QPalette::ColorRole::Base, color);
   ui.editColor->setPalette(pal);
}
