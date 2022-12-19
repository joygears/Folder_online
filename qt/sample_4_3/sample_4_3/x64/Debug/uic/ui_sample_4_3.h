/********************************************************************************
** Form generated from reading UI file 'sample_4_3.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_4_3_H
#define UI_SAMPLE_4_3_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_sample_4_3Class
{
public:
    QGridLayout *gridLayout_3;
    QGridLayout *gridLayout;
    QLabel *label;
    QSpinBox *spinNum;
    QLabel *label_2;
    QDoubleSpinBox *spinSingle;
    QPushButton *btnCal;
    QLabel *label_4;
    QDoubleSpinBox *spinGlobal;
    QGridLayout *gridLayout_2;
    QLabel *label_5;
    QSpinBox *spinDec;
    QPushButton *btnDec;
    QLabel *label_6;
    QSpinBox *spinBin;
    QPushButton *btnBin;
    QLabel *label_7;
    QSpinBox *spinHex;
    QPushButton *btnHex;
    QSpacerItem *verticalSpacer;

    void setupUi(QWidget *sample_4_3Class)
    {
        if (sample_4_3Class->objectName().isEmpty())
            sample_4_3Class->setObjectName(QString::fromUtf8("sample_4_3Class"));
        sample_4_3Class->resize(328, 169);
        gridLayout_3 = new QGridLayout(sample_4_3Class);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        label = new QLabel(sample_4_3Class);
        label->setObjectName(QString::fromUtf8("label"));
        label->setAlignment(Qt::AlignCenter);

        gridLayout->addWidget(label, 0, 0, 1, 1);

        spinNum = new QSpinBox(sample_4_3Class);
        spinNum->setObjectName(QString::fromUtf8("spinNum"));
        spinNum->setMaximum(999999999);
        spinNum->setValue(4);

        gridLayout->addWidget(spinNum, 0, 1, 1, 1);

        label_2 = new QLabel(sample_4_3Class);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setAlignment(Qt::AlignCenter);

        gridLayout->addWidget(label_2, 0, 2, 1, 1);

        spinSingle = new QDoubleSpinBox(sample_4_3Class);
        spinSingle->setObjectName(QString::fromUtf8("spinSingle"));
        spinSingle->setMinimumSize(QSize(100, 0));
        spinSingle->setMaximum(10000000000000000000.000000000000000);
        spinSingle->setValue(12.430000000000000);

        gridLayout->addWidget(spinSingle, 0, 3, 1, 1);

        btnCal = new QPushButton(sample_4_3Class);
        btnCal->setObjectName(QString::fromUtf8("btnCal"));

        gridLayout->addWidget(btnCal, 1, 1, 1, 1);

        label_4 = new QLabel(sample_4_3Class);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setAlignment(Qt::AlignCenter);

        gridLayout->addWidget(label_4, 1, 2, 1, 1);

        spinGlobal = new QDoubleSpinBox(sample_4_3Class);
        spinGlobal->setObjectName(QString::fromUtf8("spinGlobal"));
        spinGlobal->setMaximum(9999999103.989999771118164);

        gridLayout->addWidget(spinGlobal, 1, 3, 1, 1);


        gridLayout_3->addLayout(gridLayout, 0, 0, 1, 1);

        gridLayout_2 = new QGridLayout();
        gridLayout_2->setSpacing(6);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        label_5 = new QLabel(sample_4_3Class);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        gridLayout_2->addWidget(label_5, 0, 0, 1, 1);

        spinDec = new QSpinBox(sample_4_3Class);
        spinDec->setObjectName(QString::fromUtf8("spinDec"));
        spinDec->setMinimumSize(QSize(150, 0));
        spinDec->setMaximum(999999999);
        spinDec->setValue(12);

        gridLayout_2->addWidget(spinDec, 0, 1, 1, 1);

        btnDec = new QPushButton(sample_4_3Class);
        btnDec->setObjectName(QString::fromUtf8("btnDec"));

        gridLayout_2->addWidget(btnDec, 0, 2, 1, 1);

        label_6 = new QLabel(sample_4_3Class);
        label_6->setObjectName(QString::fromUtf8("label_6"));

        gridLayout_2->addWidget(label_6, 1, 0, 1, 1);

        spinBin = new QSpinBox(sample_4_3Class);
        spinBin->setObjectName(QString::fromUtf8("spinBin"));
        spinBin->setMaximum(999999999);
        spinBin->setDisplayIntegerBase(2);

        gridLayout_2->addWidget(spinBin, 1, 1, 1, 1);

        btnBin = new QPushButton(sample_4_3Class);
        btnBin->setObjectName(QString::fromUtf8("btnBin"));

        gridLayout_2->addWidget(btnBin, 1, 2, 1, 1);

        label_7 = new QLabel(sample_4_3Class);
        label_7->setObjectName(QString::fromUtf8("label_7"));

        gridLayout_2->addWidget(label_7, 2, 0, 1, 1);

        spinHex = new QSpinBox(sample_4_3Class);
        spinHex->setObjectName(QString::fromUtf8("spinHex"));
        spinHex->setMaximum(999999999);
        spinHex->setDisplayIntegerBase(16);

        gridLayout_2->addWidget(spinHex, 2, 1, 1, 1);

        btnHex = new QPushButton(sample_4_3Class);
        btnHex->setObjectName(QString::fromUtf8("btnHex"));

        gridLayout_2->addWidget(btnHex, 2, 2, 1, 1);


        gridLayout_3->addLayout(gridLayout_2, 2, 0, 1, 1);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_3->addItem(verticalSpacer, 1, 0, 1, 1);


        retranslateUi(sample_4_3Class);

        QMetaObject::connectSlotsByName(sample_4_3Class);
    } // setupUi

    void retranslateUi(QWidget *sample_4_3Class)
    {
        sample_4_3Class->setWindowTitle(QCoreApplication::translate("sample_4_3Class", "sample_4_3", nullptr));
        label->setText(QCoreApplication::translate("sample_4_3Class", "\346\225\260  \351\207\217", nullptr));
        spinNum->setSuffix(QCoreApplication::translate("sample_4_3Class", " kg", nullptr));
        spinNum->setPrefix(QString());
        label_2->setText(QCoreApplication::translate("sample_4_3Class", "\345\215\225 \344\273\267", nullptr));
        spinSingle->setPrefix(QCoreApplication::translate("sample_4_3Class", "$ ", nullptr));
        btnCal->setText(QCoreApplication::translate("sample_4_3Class", "\350\256\241\347\256\227", nullptr));
        label_4->setText(QCoreApplication::translate("sample_4_3Class", "\346\200\273 \344\273\267", nullptr));
        spinGlobal->setPrefix(QCoreApplication::translate("sample_4_3Class", "$ ", nullptr));
        label_5->setText(QCoreApplication::translate("sample_4_3Class", "\345\215\201\350\277\233\345\210\266", nullptr));
        spinDec->setPrefix(QCoreApplication::translate("sample_4_3Class", "Dec ", nullptr));
        btnDec->setText(QCoreApplication::translate("sample_4_3Class", "\350\275\254\346\215\242\344\270\272\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
        label_6->setText(QCoreApplication::translate("sample_4_3Class", "\344\272\214\350\277\233\345\210\266", nullptr));
        spinBin->setPrefix(QCoreApplication::translate("sample_4_3Class", "Bin ", nullptr));
        btnBin->setText(QCoreApplication::translate("sample_4_3Class", "\350\275\254\346\215\242\344\270\272\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
        label_7->setText(QCoreApplication::translate("sample_4_3Class", "\345\215\201\345\205\255\350\277\233\345\210\266", nullptr));
        spinHex->setPrefix(QCoreApplication::translate("sample_4_3Class", "Hex ", nullptr));
        btnHex->setText(QCoreApplication::translate("sample_4_3Class", "\350\275\254\346\215\242\344\270\272\345\205\266\344\273\226\350\277\233\345\210\266", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sample_4_3Class: public Ui_sample_4_3Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_4_3_H
