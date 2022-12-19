#include "sample_4_2.h"

sample_4_2::sample_4_2(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);

}

sample_4_2::~sample_4_2()
{

}

void sample_4_2::on_btnPrepend_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.editResult->setText(str1.prepend(str2));
}

void sample_4_2::on_btnCount_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.spinBox->setValue(str1.count());
    ui.labSpin->setText("count()");
}
void sample_4_2::on_btnIndexOf_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.spinBox->setValue(str1.indexOf(str2));
    ui.labSpin->setText("indexOf()");
}
void sample_4_2::on_btnLastIndexOf_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.spinBox->setValue(str1.lastIndexOf(str2));
    ui.labSpin->setText("lastIndexOf()");
}

void sample_4_2::on_btnEnds_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.checkBox->setText("endsWith()");
    ui.checkBox->setChecked(str1.endsWith(str2));
}

void sample_4_2::on_btnTrimmed_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    ui.editResult->setText(str1.trimmed());
}

void sample_4_2::on_btnSimple_clicked()
{
    QString str1 = ui.comboBoxStr1->currentText();
    ui.editResult->setText(str1.simplified());
}

void sample_4_2::on_btnAppend_clicked() {

    QString str1 =  ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.editResult->setText(str1.append(str2));
}

void sample_4_2::on_btnIsNull_clicked() {

    QString str1 = ui.comboBoxStr1->currentText();
    QString str2 = ui.comboBoxStr2->currentText();
    ui.checkBox->setText("isNull()");
    ui.checkBox->setChecked(str1.isNull());
}
void sample_4_2::on_btnIsEmpty_clicked() {

    QString str1 = ui.comboBoxStr1->currentText();
    QString str2;
    ui.checkBox->setText("isEmpty()");
    ui.checkBox->setChecked(str1.isEmpty());
    emit ui.btnIsNull->clicked();
}