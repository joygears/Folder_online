/********************************************************************************
** Form generated from reading UI file 'sample_4_4.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_4_4_H
#define UI_SAMPLE_4_4_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDial>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLCDNumber>
#include <QtWidgets/QLabel>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QScrollBar>
#include <QtWidgets/QSlider>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_sample_4_4Class
{
public:
    QGridLayout *gridLayout_2;
    QGridLayout *gridLayout_3;
    QGroupBox *groupBox;
    QGridLayout *gridLayout;
    QLabel *label;
    QSlider *sliderRed;
    QTextEdit *editColor;
    QLabel *label_2;
    QSlider *sliderGreen;
    QLabel *label_3;
    QSlider *sliderBlue;
    QLabel *label_4;
    QSlider *sliderAlpha;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout;
    QSlider *sliderH;
    QScrollBar *scrollH;
    QProgressBar *progressH;
    QGroupBox *groupBox_4;
    QHBoxLayout *horizontalLayout_2;
    QDial *dial;
    QLCDNumber *lcdNumber;
    QGroupBox *groupBox_5;
    QVBoxLayout *verticalLayout_2;
    QRadioButton *radioDec;
    QRadioButton *radioBin;
    QRadioButton *radioOct;
    QRadioButton *radioHex;
    QVBoxLayout *verticalLayout_4;
    QGroupBox *groupBox_3;
    QGridLayout *gridLayout_4;
    QSlider *sliderV;
    QScrollBar *scrollV;
    QProgressBar *progressV;
    QSpacerItem *verticalSpacer_3;
    QPushButton *btnClose;
    QSpacerItem *verticalSpacer_4;

    void setupUi(QWidget *sample_4_4Class)
    {
        if (sample_4_4Class->objectName().isEmpty())
            sample_4_4Class->setObjectName(QString::fromUtf8("sample_4_4Class"));
        sample_4_4Class->resize(545, 424);
        gridLayout_2 = new QGridLayout(sample_4_4Class);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_3 = new QGridLayout();
        gridLayout_3->setSpacing(6);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        groupBox = new QGroupBox(sample_4_4Class);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        gridLayout = new QGridLayout(groupBox);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        label = new QLabel(groupBox);
        label->setObjectName(QString::fromUtf8("label"));
        label->setMaximumSize(QSize(100, 16777215));

        gridLayout->addWidget(label, 0, 0, 1, 1);

        sliderRed = new QSlider(groupBox);
        sliderRed->setObjectName(QString::fromUtf8("sliderRed"));
        sliderRed->setMaximum(255);
        sliderRed->setOrientation(Qt::Horizontal);

        gridLayout->addWidget(sliderRed, 0, 1, 1, 1);

        editColor = new QTextEdit(groupBox);
        editColor->setObjectName(QString::fromUtf8("editColor"));
        editColor->setMaximumSize(QSize(100, 16777215));
        QPalette palette;
        QBrush brush(QColor(170, 255, 0, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Base, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush);
        QBrush brush1(QColor(240, 240, 240, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush1);
        editColor->setPalette(palette);

        gridLayout->addWidget(editColor, 0, 2, 4, 1);

        label_2 = new QLabel(groupBox);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout->addWidget(label_2, 1, 0, 1, 1);

        sliderGreen = new QSlider(groupBox);
        sliderGreen->setObjectName(QString::fromUtf8("sliderGreen"));
        sliderGreen->setMaximum(255);
        sliderGreen->setOrientation(Qt::Horizontal);

        gridLayout->addWidget(sliderGreen, 1, 1, 1, 1);

        label_3 = new QLabel(groupBox);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        gridLayout->addWidget(label_3, 2, 0, 1, 1);

        sliderBlue = new QSlider(groupBox);
        sliderBlue->setObjectName(QString::fromUtf8("sliderBlue"));
        sliderBlue->setMaximum(255);
        sliderBlue->setOrientation(Qt::Horizontal);

        gridLayout->addWidget(sliderBlue, 2, 1, 1, 1);

        label_4 = new QLabel(groupBox);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        gridLayout->addWidget(label_4, 3, 0, 1, 1);

        sliderAlpha = new QSlider(groupBox);
        sliderAlpha->setObjectName(QString::fromUtf8("sliderAlpha"));
        sliderAlpha->setMaximum(255);
        sliderAlpha->setOrientation(Qt::Horizontal);

        gridLayout->addWidget(sliderAlpha, 3, 1, 1, 1);


        gridLayout_3->addWidget(groupBox, 0, 0, 1, 1);

        groupBox_2 = new QGroupBox(sample_4_4Class);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        verticalLayout = new QVBoxLayout(groupBox_2);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        sliderH = new QSlider(groupBox_2);
        sliderH->setObjectName(QString::fromUtf8("sliderH"));
        sliderH->setOrientation(Qt::Horizontal);
        sliderH->setTickPosition(QSlider::TicksAbove);

        verticalLayout->addWidget(sliderH);

        scrollH = new QScrollBar(groupBox_2);
        scrollH->setObjectName(QString::fromUtf8("scrollH"));
        scrollH->setOrientation(Qt::Horizontal);

        verticalLayout->addWidget(scrollH);

        progressH = new QProgressBar(groupBox_2);
        progressH->setObjectName(QString::fromUtf8("progressH"));
        progressH->setValue(24);

        verticalLayout->addWidget(progressH);


        gridLayout_3->addWidget(groupBox_2, 1, 0, 1, 1);

        groupBox_4 = new QGroupBox(sample_4_4Class);
        groupBox_4->setObjectName(QString::fromUtf8("groupBox_4"));
        horizontalLayout_2 = new QHBoxLayout(groupBox_4);
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        dial = new QDial(groupBox_4);
        dial->setObjectName(QString::fromUtf8("dial"));
        dial->setMaximum(255);
        dial->setWrapping(false);
        dial->setNotchesVisible(true);

        horizontalLayout_2->addWidget(dial);

        lcdNumber = new QLCDNumber(groupBox_4);
        lcdNumber->setObjectName(QString::fromUtf8("lcdNumber"));
        lcdNumber->setDigitCount(5);

        horizontalLayout_2->addWidget(lcdNumber);

        groupBox_5 = new QGroupBox(groupBox_4);
        groupBox_5->setObjectName(QString::fromUtf8("groupBox_5"));
        verticalLayout_2 = new QVBoxLayout(groupBox_5);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        radioDec = new QRadioButton(groupBox_5);
        radioDec->setObjectName(QString::fromUtf8("radioDec"));

        verticalLayout_2->addWidget(radioDec);

        radioBin = new QRadioButton(groupBox_5);
        radioBin->setObjectName(QString::fromUtf8("radioBin"));

        verticalLayout_2->addWidget(radioBin);

        radioOct = new QRadioButton(groupBox_5);
        radioOct->setObjectName(QString::fromUtf8("radioOct"));

        verticalLayout_2->addWidget(radioOct);

        radioHex = new QRadioButton(groupBox_5);
        radioHex->setObjectName(QString::fromUtf8("radioHex"));

        verticalLayout_2->addWidget(radioHex);


        horizontalLayout_2->addWidget(groupBox_5);


        gridLayout_3->addWidget(groupBox_4, 2, 0, 1, 1);


        gridLayout_2->addLayout(gridLayout_3, 0, 0, 1, 1);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setSpacing(6);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        groupBox_3 = new QGroupBox(sample_4_4Class);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        gridLayout_4 = new QGridLayout(groupBox_3);
        gridLayout_4->setSpacing(6);
        gridLayout_4->setContentsMargins(11, 11, 11, 11);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        sliderV = new QSlider(groupBox_3);
        sliderV->setObjectName(QString::fromUtf8("sliderV"));
        sliderV->setMinimumSize(QSize(0, 200));
        sliderV->setOrientation(Qt::Vertical);
        sliderV->setTickPosition(QSlider::TicksAbove);

        gridLayout_4->addWidget(sliderV, 0, 0, 1, 1);

        scrollV = new QScrollBar(groupBox_3);
        scrollV->setObjectName(QString::fromUtf8("scrollV"));
        scrollV->setSliderPosition(0);
        scrollV->setTracking(true);
        scrollV->setOrientation(Qt::Vertical);
        scrollV->setInvertedAppearance(true);

        gridLayout_4->addWidget(scrollV, 0, 1, 1, 1);

        progressV = new QProgressBar(groupBox_3);
        progressV->setObjectName(QString::fromUtf8("progressV"));
        progressV->setLayoutDirection(Qt::LeftToRight);
        progressV->setValue(24);
        progressV->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
        progressV->setOrientation(Qt::Vertical);
        progressV->setInvertedAppearance(false);
        progressV->setTextDirection(QProgressBar::TopToBottom);

        gridLayout_4->addWidget(progressV, 0, 2, 1, 1);


        verticalLayout_4->addWidget(groupBox_3);

        verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_4->addItem(verticalSpacer_3);

        btnClose = new QPushButton(sample_4_4Class);
        btnClose->setObjectName(QString::fromUtf8("btnClose"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/images/images/wsl.ico"), QSize(), QIcon::Normal, QIcon::Off);
        btnClose->setIcon(icon);

        verticalLayout_4->addWidget(btnClose);

        verticalSpacer_4 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_4->addItem(verticalSpacer_4);


        gridLayout_2->addLayout(verticalLayout_4, 0, 1, 1, 1);


        retranslateUi(sample_4_4Class);
        QObject::connect(btnClose, SIGNAL(clicked()), sample_4_4Class, SLOT(close()));
        QObject::connect(sliderH, SIGNAL(valueChanged(int)), scrollH, SLOT(setValue(int)));
        QObject::connect(sliderH, SIGNAL(valueChanged(int)), progressH, SLOT(setValue(int)));
        QObject::connect(sliderV, SIGNAL(valueChanged(int)), scrollV, SLOT(setValue(int)));
        QObject::connect(sliderV, SIGNAL(valueChanged(int)), progressV, SLOT(setValue(int)));
        QObject::connect(dial, SIGNAL(valueChanged(int)), lcdNumber, SLOT(display(int)));
        QObject::connect(radioDec, SIGNAL(clicked()), lcdNumber, SLOT(setDecMode()));
        QObject::connect(radioHex, SIGNAL(clicked()), lcdNumber, SLOT(setHexMode()));
        QObject::connect(radioBin, SIGNAL(clicked()), lcdNumber, SLOT(setBinMode()));
        QObject::connect(radioOct, SIGNAL(clicked()), lcdNumber, SLOT(setOctMode()));

        QMetaObject::connectSlotsByName(sample_4_4Class);
    } // setupUi

    void retranslateUi(QWidget *sample_4_4Class)
    {
        sample_4_4Class->setWindowTitle(QCoreApplication::translate("sample_4_4Class", "sample_4_4", nullptr));
        groupBox->setTitle(QCoreApplication::translate("sample_4_4Class", "Slider\345\222\214QColor", nullptr));
        label->setText(QCoreApplication::translate("sample_4_4Class", "Red", nullptr));
        label_2->setText(QCoreApplication::translate("sample_4_4Class", "Green", nullptr));
        label_3->setText(QCoreApplication::translate("sample_4_4Class", "Blue", nullptr));
        label_4->setText(QCoreApplication::translate("sample_4_4Class", "Alpha", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("sample_4_4Class", "\346\260\264\345\271\263", nullptr));
        groupBox_4->setTitle(QCoreApplication::translate("sample_4_4Class", "Dial\345\222\214LCDNumber", nullptr));
        groupBox_5->setTitle(QCoreApplication::translate("sample_4_4Class", "LCD\346\230\276\347\244\272\350\277\233\345\210\266", nullptr));
        radioDec->setText(QCoreApplication::translate("sample_4_4Class", "\345\215\201\350\277\233\345\210\266", nullptr));
        radioBin->setText(QCoreApplication::translate("sample_4_4Class", "\344\272\214\350\277\233\345\210\266", nullptr));
        radioOct->setText(QCoreApplication::translate("sample_4_4Class", "\345\205\253\350\277\233\345\210\266", nullptr));
        radioHex->setText(QCoreApplication::translate("sample_4_4Class", "\345\215\201\345\205\255\350\277\233\345\210\266", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("sample_4_4Class", "\345\236\202\347\233\264", nullptr));
        btnClose->setText(QCoreApplication::translate("sample_4_4Class", "\351\200\200\345\207\272", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sample_4_4Class: public Ui_sample_4_4Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_4_4_H
