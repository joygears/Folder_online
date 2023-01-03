#include "widget.h"
#include "./ui_widget.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_btnClearCombo_clicked()
{
    ui->comboBox->clear();
}

void Widget::on_checkEditable_stateChanged(int state)
{
    
    ui->comboBox->setEditable(state);

}

void Widget::on_comboBox_currentTextChanged(const QString& text)
{   if(!text.isEmpty())
        ui->plainTextEdit->appendPlainText(text);
}

void Widget::on_comboBox_2_currentTextChanged(const QString& text)
{
    if (!text.isEmpty()) {
        
        ui->plainTextEdit->appendPlainText(text+QString::fromLocal8Bit("区号：")+ui->comboBox_2->currentData().toString());
    }
}

void Widget::on_checkReadable_clicked(bool checked)
{
    ui->plainTextEdit->setReadOnly(checked);
}

void Widget::on_btnMap_clicked()
{
    ui->comboBox_2->clear();
    QIcon icon(":/third/images/Cursor_Laser_Pointer.ico");
    QMap<QString, int> map;
    map.insert(QString::fromLocal8Bit("北京"), 10);
    map.insert(QString::fromLocal8Bit("天津"), 20);
    map.insert(QString::fromLocal8Bit("南京"), 30);
    foreach(auto key,map.keys()) {
        ui->comboBox_2->addItem(icon, key, map.value(key));
    }
}

void Widget::on_btnInitList_clicked()
{
    QIcon icon(":/third/images/msys2.ico");
    ui->comboBox->clear();
    for (int i = 0; i < 20; i++)
        ui->comboBox->addItem(icon, QString::asprintf("item %d", i + 1));

}

