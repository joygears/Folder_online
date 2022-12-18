#include "sample_4_1.h"

sample_4_1::sample_4_1(QWidget *parent)
    : QWidget(parent)
{
    ui.setupUi(this);
    
    
}
void sample_4_1::on_btnCal_clicked() {

    QString strNum = this->ui.EditNum->text();
    QString strSinglePrice = this->ui.EditSinglePrice->text();
    int num = strNum.toInt();
    double singlePrice = strSinglePrice.toDouble();
    double globalPrice = num * singlePrice;
    this->ui.EditGlobalPrice->setText(QString::asprintf("%.2f", globalPrice));
}

void sample_4_1::on_btnTenHex_clicked()
{
    int TexHex = ui.EditTenHex->text().toInt();
    ui.EditTwoHex->setText(QString::number(TexHex,2));
    ui.EditHex->setText(QString::number(TexHex, 16).toUpper());
}

void sample_4_1::on_btnTwoHex_clicked()
{
    bool ok;
    int twoHex = ui.EditTwoHex->text().toInt(&ok,2);
    ui.EditTenHex->setText(QString::number(twoHex, 10));
    ui.EditHex->setText(QString::number(twoHex, 16).toUpper());
}

void sample_4_1::on_btnHex_clicked()
{
    bool ok;
    int twoHex = ui.EditHex->text().toInt(&ok, 16);
    ui.EditTenHex->setText(QString::number(twoHex, 10));
    ui.EditTwoHex->setText(QString::number(twoHex, 2));

}
