/********************************************************************************
** Form generated from reading UI file 'sample_4_2.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_4_2_H
#define UI_SAMPLE_4_2_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_sample_4_2Class
{
public:
    QGridLayout *gridLayout_6;
    QGridLayout *gridLayout;
    QLabel *labelStr1;
    QComboBox *comboBoxStr1;
    QLabel *labelStr2;
    QComboBox *comboBoxStr2;
    QGridLayout *gridLayout_5;
    QGroupBox *groupBox;
    QGridLayout *gridLayout_2;
    QPushButton *btnAppend;
    QPushButton *btnPrepend;
    QPushButton *btnToUpper;
    QPushButton *btnToLower;
    QPushButton *btnLeft;
    QPushButton *btnRight;
    QPushButton *btnSection;
    QPushButton *btnSimple;
    QPushButton *btnTrimmed;
    QGroupBox *groupBox_2;
    QGridLayout *gridLayout_3;
    QPushButton *btnSize;
    QPushButton *btnLastIndexOf;
    QPushButton *btnIndexOf;
    QPushButton *btnCount;
    QGroupBox *groupBox_3;
    QGridLayout *gridLayout_4;
    QPushButton *btnEnds;
    QPushButton *btnIsNull;
    QPushButton *btnStarts;
    QPushButton *btnContains;
    QPushButton *btnIsEmpty;
    QHBoxLayout *horizontalLayout_2;
    QLabel *labelResult;
    QLineEdit *editResult;
    QHBoxLayout *horizontalLayout;
    QCheckBox *checkBox;
    QSpacerItem *horizontalSpacer;
    QLabel *labSpin;
    QSpinBox *spinBox;

    void setupUi(QWidget *sample_4_2Class)
    {
        if (sample_4_2Class->objectName().isEmpty())
            sample_4_2Class->setObjectName(QString::fromUtf8("sample_4_2Class"));
        sample_4_2Class->resize(489, 316);
        gridLayout_6 = new QGridLayout(sample_4_2Class);
        gridLayout_6->setSpacing(6);
        gridLayout_6->setContentsMargins(11, 11, 11, 11);
        gridLayout_6->setObjectName(QString::fromUtf8("gridLayout_6"));
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelStr1 = new QLabel(sample_4_2Class);
        labelStr1->setObjectName(QString::fromUtf8("labelStr1"));
        labelStr1->setMaximumSize(QSize(50, 16777215));

        gridLayout->addWidget(labelStr1, 0, 0, 1, 1);

        comboBoxStr1 = new QComboBox(sample_4_2Class);
        comboBoxStr1->addItem(QString());
        comboBoxStr1->addItem(QString());
        comboBoxStr1->setObjectName(QString::fromUtf8("comboBoxStr1"));
        comboBoxStr1->setEditable(true);

        gridLayout->addWidget(comboBoxStr1, 0, 1, 1, 1);

        labelStr2 = new QLabel(sample_4_2Class);
        labelStr2->setObjectName(QString::fromUtf8("labelStr2"));
        labelStr2->setMaximumSize(QSize(50, 16777215));

        gridLayout->addWidget(labelStr2, 1, 0, 1, 1);

        comboBoxStr2 = new QComboBox(sample_4_2Class);
        comboBoxStr2->addItem(QString());
        comboBoxStr2->setObjectName(QString::fromUtf8("comboBoxStr2"));
        comboBoxStr2->setEditable(true);

        gridLayout->addWidget(comboBoxStr2, 1, 1, 1, 1);


        gridLayout_6->addLayout(gridLayout, 0, 0, 1, 1);

        gridLayout_5 = new QGridLayout();
        gridLayout_5->setSpacing(6);
        gridLayout_5->setObjectName(QString::fromUtf8("gridLayout_5"));
        groupBox = new QGroupBox(sample_4_2Class);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        gridLayout_2 = new QGridLayout(groupBox);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        btnAppend = new QPushButton(groupBox);
        btnAppend->setObjectName(QString::fromUtf8("btnAppend"));

        gridLayout_2->addWidget(btnAppend, 0, 0, 1, 1);

        btnPrepend = new QPushButton(groupBox);
        btnPrepend->setObjectName(QString::fromUtf8("btnPrepend"));

        gridLayout_2->addWidget(btnPrepend, 0, 1, 1, 1);

        btnToUpper = new QPushButton(groupBox);
        btnToUpper->setObjectName(QString::fromUtf8("btnToUpper"));

        gridLayout_2->addWidget(btnToUpper, 1, 0, 1, 1);

        btnToLower = new QPushButton(groupBox);
        btnToLower->setObjectName(QString::fromUtf8("btnToLower"));

        gridLayout_2->addWidget(btnToLower, 1, 1, 1, 1);

        btnLeft = new QPushButton(groupBox);
        btnLeft->setObjectName(QString::fromUtf8("btnLeft"));

        gridLayout_2->addWidget(btnLeft, 2, 0, 1, 1);

        btnRight = new QPushButton(groupBox);
        btnRight->setObjectName(QString::fromUtf8("btnRight"));

        gridLayout_2->addWidget(btnRight, 2, 1, 1, 1);

        btnSection = new QPushButton(groupBox);
        btnSection->setObjectName(QString::fromUtf8("btnSection"));

        gridLayout_2->addWidget(btnSection, 3, 1, 1, 1);

        btnSimple = new QPushButton(groupBox);
        btnSimple->setObjectName(QString::fromUtf8("btnSimple"));

        gridLayout_2->addWidget(btnSimple, 4, 0, 1, 1);

        btnTrimmed = new QPushButton(groupBox);
        btnTrimmed->setObjectName(QString::fromUtf8("btnTrimmed"));

        gridLayout_2->addWidget(btnTrimmed, 4, 1, 1, 1);


        gridLayout_5->addWidget(groupBox, 0, 0, 1, 1);

        groupBox_2 = new QGroupBox(sample_4_2Class);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        gridLayout_3 = new QGridLayout(groupBox_2);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        btnSize = new QPushButton(groupBox_2);
        btnSize->setObjectName(QString::fromUtf8("btnSize"));

        gridLayout_3->addWidget(btnSize, 1, 0, 1, 1);

        btnLastIndexOf = new QPushButton(groupBox_2);
        btnLastIndexOf->setObjectName(QString::fromUtf8("btnLastIndexOf"));

        gridLayout_3->addWidget(btnLastIndexOf, 3, 0, 1, 1);

        btnIndexOf = new QPushButton(groupBox_2);
        btnIndexOf->setObjectName(QString::fromUtf8("btnIndexOf"));

        gridLayout_3->addWidget(btnIndexOf, 2, 0, 1, 1);

        btnCount = new QPushButton(groupBox_2);
        btnCount->setObjectName(QString::fromUtf8("btnCount"));

        gridLayout_3->addWidget(btnCount, 0, 0, 1, 1);


        gridLayout_5->addWidget(groupBox_2, 0, 1, 1, 1);

        groupBox_3 = new QGroupBox(sample_4_2Class);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        gridLayout_4 = new QGridLayout(groupBox_3);
        gridLayout_4->setSpacing(6);
        gridLayout_4->setContentsMargins(11, 11, 11, 11);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        btnEnds = new QPushButton(groupBox_3);
        btnEnds->setObjectName(QString::fromUtf8("btnEnds"));

        gridLayout_4->addWidget(btnEnds, 0, 0, 1, 1);

        btnIsNull = new QPushButton(groupBox_3);
        btnIsNull->setObjectName(QString::fromUtf8("btnIsNull"));

        gridLayout_4->addWidget(btnIsNull, 0, 1, 1, 1);

        btnStarts = new QPushButton(groupBox_3);
        btnStarts->setObjectName(QString::fromUtf8("btnStarts"));

        gridLayout_4->addWidget(btnStarts, 1, 0, 1, 1);

        btnContains = new QPushButton(groupBox_3);
        btnContains->setObjectName(QString::fromUtf8("btnContains"));
        btnContains->setCheckable(false);

        gridLayout_4->addWidget(btnContains, 2, 0, 1, 1);

        btnIsEmpty = new QPushButton(groupBox_3);
        btnIsEmpty->setObjectName(QString::fromUtf8("btnIsEmpty"));

        gridLayout_4->addWidget(btnIsEmpty, 2, 1, 1, 1);


        gridLayout_5->addWidget(groupBox_3, 0, 2, 1, 1);


        gridLayout_6->addLayout(gridLayout_5, 1, 0, 1, 1);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        labelResult = new QLabel(sample_4_2Class);
        labelResult->setObjectName(QString::fromUtf8("labelResult"));
        labelResult->setMinimumSize(QSize(39, 0));

        horizontalLayout_2->addWidget(labelResult);

        editResult = new QLineEdit(sample_4_2Class);
        editResult->setObjectName(QString::fromUtf8("editResult"));

        horizontalLayout_2->addWidget(editResult);


        gridLayout_6->addLayout(horizontalLayout_2, 2, 0, 1, 1);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        checkBox = new QCheckBox(sample_4_2Class);
        checkBox->setObjectName(QString::fromUtf8("checkBox"));

        horizontalLayout->addWidget(checkBox);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        labSpin = new QLabel(sample_4_2Class);
        labSpin->setObjectName(QString::fromUtf8("labSpin"));

        horizontalLayout->addWidget(labSpin);

        spinBox = new QSpinBox(sample_4_2Class);
        spinBox->setObjectName(QString::fromUtf8("spinBox"));
        spinBox->setMinimumSize(QSize(132, 0));

        horizontalLayout->addWidget(spinBox);


        gridLayout_6->addLayout(horizontalLayout, 3, 0, 1, 1);


        retranslateUi(sample_4_2Class);

        QMetaObject::connectSlotsByName(sample_4_2Class);
    } // setupUi

    void retranslateUi(QWidget *sample_4_2Class)
    {
        sample_4_2Class->setWindowTitle(QCoreApplication::translate("sample_4_2Class", "sample_4_2", nullptr));
        labelStr1->setText(QCoreApplication::translate("sample_4_2Class", "str1", nullptr));
        comboBoxStr1->setItemText(0, QCoreApplication::translate("sample_4_2Class", "g:\\Qt5Book\\QT5.9Study", nullptr));
        comboBoxStr1->setItemText(1, QCoreApplication::translate("sample_4_2Class", "D:\\sourcetree\\hitPaw-video-download", nullptr));

        comboBoxStr1->setCurrentText(QCoreApplication::translate("sample_4_2Class", "g:\\Qt5Book\\QT5.9Study", nullptr));
        labelStr2->setText(QCoreApplication::translate("sample_4_2Class", "str2", nullptr));
        comboBoxStr2->setItemText(0, QCoreApplication::translate("sample_4_2Class", "\\", nullptr));

        comboBoxStr2->setCurrentText(QCoreApplication::translate("sample_4_2Class", "\\", nullptr));
        groupBox->setTitle(QCoreApplication::translate("sample_4_2Class", "\345\255\227\347\254\246\344\270\262", nullptr));
        btnAppend->setText(QCoreApplication::translate("sample_4_2Class", "Append", nullptr));
        btnPrepend->setText(QCoreApplication::translate("sample_4_2Class", "Prepend", nullptr));
        btnToUpper->setText(QCoreApplication::translate("sample_4_2Class", "toUpper", nullptr));
        btnToLower->setText(QCoreApplication::translate("sample_4_2Class", "toLower", nullptr));
        btnLeft->setText(QCoreApplication::translate("sample_4_2Class", "left", nullptr));
        btnRight->setText(QCoreApplication::translate("sample_4_2Class", "right", nullptr));
        btnSection->setText(QCoreApplication::translate("sample_4_2Class", "section", nullptr));
        btnSimple->setText(QCoreApplication::translate("sample_4_2Class", "simplified", nullptr));
        btnTrimmed->setText(QCoreApplication::translate("sample_4_2Class", "trimmed", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("sample_4_2Class", "\346\225\260\345\255\227", nullptr));
        btnSize->setText(QCoreApplication::translate("sample_4_2Class", "size", nullptr));
        btnLastIndexOf->setText(QCoreApplication::translate("sample_4_2Class", "lastIndexOf", nullptr));
        btnIndexOf->setText(QCoreApplication::translate("sample_4_2Class", "indexOf", nullptr));
        btnCount->setText(QCoreApplication::translate("sample_4_2Class", "count", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("sample_4_2Class", "\351\200\273\350\276\221\345\210\244\346\226\255", nullptr));
        btnEnds->setText(QCoreApplication::translate("sample_4_2Class", "endsWith", nullptr));
        btnIsNull->setText(QCoreApplication::translate("sample_4_2Class", "startsWith", nullptr));
        btnStarts->setText(QCoreApplication::translate("sample_4_2Class", "contains", nullptr));
        btnContains->setText(QCoreApplication::translate("sample_4_2Class", "isNull", nullptr));
        btnIsEmpty->setText(QCoreApplication::translate("sample_4_2Class", "isEmpty", nullptr));
        labelResult->setText(QCoreApplication::translate("sample_4_2Class", "\347\273\223\346\236\234", nullptr));
        editResult->setText(QCoreApplication::translate("sample_4_2Class", "g:\\Qt5Book\\QT5.9Study", nullptr));
        checkBox->setText(QCoreApplication::translate("sample_4_2Class", "CheckBox", nullptr));
        labSpin->setText(QCoreApplication::translate("sample_4_2Class", "LabSpin", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sample_4_2Class: public Ui_sample_4_2Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_4_2_H
