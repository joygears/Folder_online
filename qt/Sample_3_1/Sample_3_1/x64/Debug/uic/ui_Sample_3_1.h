/********************************************************************************
** Form generated from reading UI file 'Sample_3_1.ui'
**
** Created by: Qt User Interface Compiler version 5.12.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_3_1_H
#define UI_SAMPLE_3_1_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPlainTextEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Sample_3_1Class
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout_2;
    QGridLayout *gridLayout;
    QLabel *labelBoy;
    QSpinBox *spinBoxBoy;
    QPushButton *btnGrowBoy;
    QPushButton *btnMetaData;
    QLabel *labelGirl;
    QSpinBox *spinBoxGirl;
    QPushButton *btnGrowGirl;
    QPushButton *btnClear;
    QPlainTextEdit *TextEdit;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *Sample_3_1Class)
    {
        if (Sample_3_1Class->objectName().isEmpty())
            Sample_3_1Class->setObjectName(QString::fromUtf8("Sample_3_1Class"));
        Sample_3_1Class->resize(600, 400);
        centralWidget = new QWidget(Sample_3_1Class);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout_2 = new QGridLayout(centralWidget);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelBoy = new QLabel(centralWidget);
        labelBoy->setObjectName(QString::fromUtf8("labelBoy"));

        gridLayout->addWidget(labelBoy, 0, 0, 1, 1);

        spinBoxBoy = new QSpinBox(centralWidget);
        spinBoxBoy->setObjectName(QString::fromUtf8("spinBoxBoy"));

        gridLayout->addWidget(spinBoxBoy, 0, 1, 1, 1);

        btnGrowBoy = new QPushButton(centralWidget);
        btnGrowBoy->setObjectName(QString::fromUtf8("btnGrowBoy"));

        gridLayout->addWidget(btnGrowBoy, 0, 2, 1, 1);

        btnMetaData = new QPushButton(centralWidget);
        btnMetaData->setObjectName(QString::fromUtf8("btnMetaData"));

        gridLayout->addWidget(btnMetaData, 0, 3, 1, 1);

        labelGirl = new QLabel(centralWidget);
        labelGirl->setObjectName(QString::fromUtf8("labelGirl"));

        gridLayout->addWidget(labelGirl, 1, 0, 1, 1);

        spinBoxGirl = new QSpinBox(centralWidget);
        spinBoxGirl->setObjectName(QString::fromUtf8("spinBoxGirl"));

        gridLayout->addWidget(spinBoxGirl, 1, 1, 1, 1);

        btnGrowGirl = new QPushButton(centralWidget);
        btnGrowGirl->setObjectName(QString::fromUtf8("btnGrowGirl"));

        gridLayout->addWidget(btnGrowGirl, 1, 2, 1, 1);

        btnClear = new QPushButton(centralWidget);
        btnClear->setObjectName(QString::fromUtf8("btnClear"));

        gridLayout->addWidget(btnClear, 1, 3, 1, 1);


        gridLayout_2->addLayout(gridLayout, 0, 0, 1, 1);

        TextEdit = new QPlainTextEdit(centralWidget);
        TextEdit->setObjectName(QString::fromUtf8("TextEdit"));

        gridLayout_2->addWidget(TextEdit, 1, 0, 1, 1);

        Sample_3_1Class->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(Sample_3_1Class);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 600, 23));
        Sample_3_1Class->setMenuBar(menuBar);
        mainToolBar = new QToolBar(Sample_3_1Class);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        Sample_3_1Class->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(Sample_3_1Class);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        Sample_3_1Class->setStatusBar(statusBar);

        retranslateUi(Sample_3_1Class);
        QObject::connect(btnClear, SIGNAL(clicked()), TextEdit, SLOT(clear()));

        QMetaObject::connectSlotsByName(Sample_3_1Class);
    } // setupUi

    void retranslateUi(QMainWindow *Sample_3_1Class)
    {
        Sample_3_1Class->setWindowTitle(QApplication::translate("Sample_3_1Class", "Sample_3_1", nullptr));
        labelBoy->setText(QApplication::translate("Sample_3_1Class", "\350\256\276\347\275\256\347\224\267\347\224\237\345\271\264\351\276\204\357\274\232", nullptr));
        btnGrowBoy->setText(QApplication::translate("Sample_3_1Class", "boy\351\225\277\345\244\247\344\270\200\345\262\201", nullptr));
        btnMetaData->setText(QApplication::translate("Sample_3_1Class", "\347\261\273\347\232\204\345\205\203\345\257\271\350\261\241\344\277\241\346\201\257", nullptr));
        labelGirl->setText(QApplication::translate("Sample_3_1Class", "\350\256\276\347\275\256\345\245\263\347\224\237\345\271\264\351\276\204\357\274\232", nullptr));
        btnGrowGirl->setText(QApplication::translate("Sample_3_1Class", "girl\351\225\277\345\244\247\344\270\200\345\262\201", nullptr));
        btnClear->setText(QApplication::translate("Sample_3_1Class", "\346\270\205\347\251\272\346\226\207\346\234\254\346\241\206", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Sample_3_1Class: public Ui_Sample_3_1Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_3_1_H
