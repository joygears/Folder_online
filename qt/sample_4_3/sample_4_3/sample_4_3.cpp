#include "sample_4_3.h"

sample_4_3::sample_4_3(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);
    void (QSpinBox:: * valueChanged)(int) = &QSpinBox::valueChanged;
    connect(ui.spinNum, valueChanged,this, &sample_4_3::on_btnCal_clicked);
    void (QDoubleSpinBox:: * doubleValueChanged)(double) = &QDoubleSpinBox::valueChanged;
    connect(ui.spinSingle, doubleValueChanged, this, &sample_4_3::on_btnCal_clicked);
    
}

sample_4_3::~sample_4_3()
{}
void sample_4_3::on_btnDec_clicked()
{
    int num;
    num = ui.spinDec->value();
    ui.spinBin->setValue(num);
    ui.spinHex->setValue(num);
}
void sample_4_3::on_btnBin_clicked()
{
    int num;
    num = ui.spinBin->value();
    ui.spinDec->setValue(num);
    ui.spinHex->setValue(num);
}
void sample_4_3::on_btnHex_clicked()
{
    int num;
    num = ui.spinHex->value();
    ui.spinBin->setValue(num);
    ui.spinDec->setValue(num);

}
void sample_4_3::on_btnCal_clicked() {
    int num;
    double single, global;
    num = ui.spinNum->value();
    single = ui.spinSingle->value();
    global = num * single;
    ui.spinGlobal->setValue(global);
}