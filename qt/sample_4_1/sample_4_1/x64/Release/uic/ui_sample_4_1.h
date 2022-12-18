/********************************************************************************
** Form generated from reading UI file 'sample_4_1.ui'
**
** Created by: Qt User Interface Compiler version 5.12.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_4_1_H
#define UI_SAMPLE_4_1_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_sample_4_1Class
{
public:
    QGridLayout *gridLayout_3;
    QGridLayout *gridLayout;
    QLabel *labelNum;
    QLineEdit *EditNum;
    QLabel *labelSingalPrice;
    QLineEdit *EditSinglePrice;
    QPushButton *btnCal;
    QLabel *labelGlobalPrice;
    QLineEdit *EditGlobalPrice;
    QSpacerItem *verticalSpacer;
    QGridLayout *gridLayout_2;
    QLabel *labelTenHex;
    QLineEdit *EditTenHex;
    QPushButton *btnTenHex;
    QLabel *labelTwoHex;
    QLineEdit *EditTwoHex;
    QPushButton *btnTwoHex;
    QLabel *labelHex;
    QLineEdit *EditHex;
    QPushButton *btnHex;

    void setupUi(QWidget *sample_4_1Class)
    {
        if (sample_4_1Class->objectName().isEmpty())
            sample_4_1Class->setObjectName(QString::fromUtf8("sample_4_1Class"));
        sample_4_1Class->resize(384, 170);
        gridLayout_3 = new QGridLayout(sample_4_1Class);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelNum = new QLabel(sample_4_1Class);
        labelNum->setObjectName(QString::fromUtf8("labelNum"));

        gridLayout->addWidget(labelNum, 0, 0, 1, 1);

        EditNum = new QLineEdit(sample_4_1Class);
        EditNum->setObjectName(QString::fromUtf8("EditNum"));

        gridLayout->addWidget(EditNum, 0, 1, 1, 1);

        labelSingalPrice = new QLabel(sample_4_1Class);
        labelSingalPrice->setObjectName(QString::fromUtf8("labelSingalPrice"));

        gridLayout->addWidget(labelSingalPrice, 0, 2, 1, 1);

        EditSinglePrice = new QLineEdit(sample_4_1Class);
        EditSinglePrice->setObjectName(QString::fromUtf8("EditSinglePrice"));

        gridLayout->addWidget(EditSinglePrice, 0, 3, 1, 1);

        btnCal = new QPushButton(sample_4_1Class);
        btnCal->setObjectName(QString::fromUtf8("btnCal"));
        btnCal->setEnabled(true);

        gridLayout->addWidget(btnCal, 1, 1, 1, 1);

        labelGlobalPrice = new QLabel(sample_4_1Class);
        labelGlobalPrice->setObjectName(QString::fromUtf8("labelGlobalPrice"));

        gridLayout->addWidget(labelGlobalPrice, 1, 2, 1, 1);

        EditGlobalPrice = new QLineEdit(sample_4_1Class);
        EditGlobalPrice->setObjectName(QString::fromUtf8("EditGlobalPrice"));

        gridLayout->addWidget(EditGlobalPrice, 1, 3, 1, 1);


        gridLayout_3->addLayout(gridLayout, 0, 0, 1, 1);

        verticalSpacer = new QSpacerItem(20, 1, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_3->addItem(verticalSpacer, 1, 0, 1, 1);

        gridLayout_2 = new QGridLayout();
        gridLayout_2->setSpacing(6);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        labelTenHex = new QLabel(sample_4_1Class);
        labelTenHex->setObjectName(QString::fromUtf8("labelTenHex"));

        gridLayout_2->addWidget(labelTenHex, 0, 0, 1, 1);

        EditTenHex = new QLineEdit(sample_4_1Class);
        EditTenHex->setObjectName(QString::fromUtf8("EditTenHex"));

        gridLayout_2->addWidget(EditTenHex, 0, 1, 1, 1);

        btnTenHex = new QPushButton(sample_4_1Class);
        btnTenHex->setObjectName(QString::fromUtf8("btnTenHex"));

        gridLayout_2->addWidget(btnTenHex, 0, 2, 1, 1);

        labelTwoHex = new QLabel(sample_4_1Class);
        labelTwoHex->setObjectName(QString::fromUtf8("labelTwoHex"));

        gridLayout_2->addWidget(labelTwoHex, 1, 0, 1, 1);

        EditTwoHex = new QLineEdit(sample_4_1Class);
        EditTwoHex->setObjectName(QString::fromUtf8("EditTwoHex"));

        gridLayout_2->addWidget(EditTwoHex, 1, 1, 1, 1);

        btnTwoHex = new QPushButton(sample_4_1Class);
        btnTwoHex->setObjectName(QString::fromUtf8("btnTwoHex"));

        gridLayout_2->addWidget(btnTwoHex, 1, 2, 1, 1);

        labelHex = new QLabel(sample_4_1Class);
        labelHex->setObjectName(QString::fromUtf8("labelHex"));

        gridLayout_2->addWidget(labelHex, 2, 0, 1, 1);

        EditHex = new QLineEdit(sample_4_1Class);
        EditHex->setObjectName(QString::fromUtf8("EditHex"));

        gridLayout_2->addWidget(EditHex, 2, 1, 1, 1);

        btnHex = new QPushButton(sample_4_1Class);
        btnHex->setObjectName(QString::fromUtf8("btnHex"));

        gridLayout_2->addWidget(btnHex, 2, 2, 1, 1);


        gridLayout_3->addLayout(gridLayout_2, 2, 0, 1, 1);


        retranslateUi(sample_4_1Class);

        QMetaObject::connectSlotsByName(sample_4_1Class);
    } // setupUi

    void retranslateUi(QWidget *sample_4_1Class)
    {
        sample_4_1Class->setWindowTitle(QApplication::translate("sample_4_1Class", "\345\255\227\347\254\246\344\270\262\347\232\204\350\276\223\345\205\245\344\270\216\350\276\223\345\207\272", nullptr));
        labelNum->setText(QApplication::translate("sample_4_1Class", "\346\225\260\351\207\217\357\274\232", nullptr));
        EditNum->setText(QApplication::translate("sample_4_1Class", "5", nullptr));
        labelSingalPrice->setText(QApplication::translate("sample_4_1Class", "\345\215\225\344\273\267\357\274\232", nullptr));
        EditSinglePrice->setText(QApplication::translate("sample_4_1Class", "7.2", nullptr));
        btnCal->setText(QApplication::translate("sample_4_1Class", "\350\256\241\347\256\227\346\200\273\344\273\267", nullptr));
        labelGlobalPrice->setText(QApplication::translate("sample_4_1Class", "\346\200\273\344\273\267\357\274\232", nullptr));
        labelTenHex->setText(QApplication::translate("sample_4_1Class", "\345\215\201\350\277\233\345\210\266\357\274\232", nullptr));
        EditTenHex->setText(QApplication::translate("sample_4_1Class", "15", nullptr));
        btnTenHex->setText(QApplication::translate("sample_4_1Class", "\350\275\254\346\215\242\346\210\220\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
        labelTwoHex->setText(QApplication::translate("sample_4_1Class", "\344\272\214\350\277\233\345\210\266\357\274\232", nullptr));
        EditTwoHex->setText(QApplication::translate("sample_4_1Class", "100", nullptr));
        btnTwoHex->setText(QApplication::translate("sample_4_1Class", "\350\275\254\346\215\242\346\210\220\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
        labelHex->setText(QApplication::translate("sample_4_1Class", "\345\215\201\345\205\255\350\277\233\345\210\266\357\274\232", nullptr));
        EditHex->setText(QApplication::translate("sample_4_1Class", "F", nullptr));
        btnHex->setText(QApplication::translate("sample_4_1Class", "\350\275\254\346\215\242\346\210\220\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sample_4_1Class: public Ui_sample_4_1Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_4_1_H
