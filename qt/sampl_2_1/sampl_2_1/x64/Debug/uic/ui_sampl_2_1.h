/********************************************************************************
** Form generated from reading UI file 'sampl_2_1.ui'
**
** Created by: Qt User Interface Compiler version 5.12.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPL_2_1_H
#define UI_SAMPL_2_1_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_sampl_2_1Class
{
public:
    QLabel *labelDemo;
    QPushButton *btnClose;

    void setupUi(QDialog *sampl_2_1Class)
    {
        if (sampl_2_1Class->objectName().isEmpty())
            sampl_2_1Class->setObjectName(QString::fromUtf8("sampl_2_1Class"));
        sampl_2_1Class->resize(600, 400);
        labelDemo = new QLabel(sampl_2_1Class);
        labelDemo->setObjectName(QString::fromUtf8("labelDemo"));
        labelDemo->setGeometry(QRect(210, 130, 151, 61));
        QFont font;
        font.setFamily(QString::fromUtf8("Arial"));
        font.setPointSize(20);
        labelDemo->setFont(font);
        btnClose = new QPushButton(sampl_2_1Class);
        btnClose->setObjectName(QString::fromUtf8("btnClose"));
        btnClose->setGeometry(QRect(360, 240, 75, 23));

        retranslateUi(sampl_2_1Class);
        QObject::connect(btnClose, SIGNAL(clicked()), sampl_2_1Class, SLOT(close()));

        QMetaObject::connectSlotsByName(sampl_2_1Class);
    } // setupUi

    void retranslateUi(QDialog *sampl_2_1Class)
    {
        sampl_2_1Class->setWindowTitle(QApplication::translate("sampl_2_1Class", "sampl_2_1", nullptr));
        labelDemo->setText(QApplication::translate("sampl_2_1Class", "hello world!", nullptr));
        btnClose->setText(QApplication::translate("sampl_2_1Class", "close", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sampl_2_1Class: public Ui_sampl_2_1Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPL_2_1_H
