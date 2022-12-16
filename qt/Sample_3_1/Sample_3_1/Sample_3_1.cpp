#include "Sample_3_1.h"
#include <QMetaProperty>
Sample_3_1::Sample_3_1(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);
    boy = new QPerson(QString::fromLocal8Bit("小明"));
    girl = new QPerson(QString::fromLocal8Bit("小红"));
    boy->setProperty("score", 80);
    girl->setProperty("score", 81);
    boy->setProperty("age", 11);
    girl->setProperty("age", 12);
    boy->setProperty("sex", "boy");
    girl->setProperty("sex", "girl");

    connect(boy, &QPerson::ageChanged, this, &Sample_3_1::on_AgeChanged);
    connect(girl, &QPerson::ageChanged, this, &Sample_3_1::on_AgeChanged);
}

Sample_3_1::~Sample_3_1()
{
    delete boy;
    delete girl;
}
void Sample_3_1::on_btnGrowGirl_clicked(){
    this->girl->incAge();
}
void Sample_3_1::on_spinBoxBoy_valueChanged(int value)
{
    boy->setAge(value);
}
void Sample_3_1::on_spinBoxGirl_valueChanged(int value)
{
    girl->setAge(value);
}
void Sample_3_1::on_AgeChanged(unsigned value)
{
    QString text = "";
    QPerson* pPerson = qobject_cast<QPerson*>(sender());
    QString qName = pPerson->property("name").toString();
    QString qSex = pPerson->property("sex").toString();
    unsigned age = pPerson->property("age").toUInt();
    ui.TextEdit->appendPlainText(qName + "," + qSex  + QString::asprintf(QString::fromLocal8Bit(",年龄=%u").toUtf8(), age));
}
void Sample_3_1::on_btnMetaData_clicked()
{
    emit ui.btnClear->click();
    const QMetaObject * metaObj = boy->metaObject();
   ui.TextEdit->appendPlainText(QString::fromLocal8Bit("========元对象信息========"));
   for (int i = metaObj->propertyOffset(); i < metaObj->propertyCount(); i++) {
       QMetaProperty pro = metaObj->property(i);
       ui.TextEdit->appendPlainText(QString::QString(QString::fromLocal8Bit("类型:%1,名称:%2")).arg(pro.typeName()).arg(pro.name()));
   }
   ui.TextEdit->appendPlainText(QString::fromLocal8Bit("类信息"));
   for (int i = metaObj->classInfoOffset(); i < metaObj->classInfoCount(); i++) {
       QMetaClassInfo cls = metaObj->classInfo(i);
       ui.TextEdit->appendPlainText(QString::QString(QString::fromLocal8Bit("名称:%1,值:%2")).arg(cls.name()).arg(cls.value()));
   }

}
void Sample_3_1::on_btnGrowBoy_clicked() {
     this->boy->incAge();
}