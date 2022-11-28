/********************************************************************************
** Form generated from reading UI file 'tsignal.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TSIGNAL_H
#define UI_TSIGNAL_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_tsignalClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *tsignalClass)
    {
        if (tsignalClass->objectName().isEmpty())
            tsignalClass->setObjectName(QString::fromUtf8("tsignalClass"));
        tsignalClass->resize(600, 400);
        menuBar = new QMenuBar(tsignalClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        tsignalClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(tsignalClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        tsignalClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(tsignalClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        tsignalClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(tsignalClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        tsignalClass->setStatusBar(statusBar);

        retranslateUi(tsignalClass);

        QMetaObject::connectSlotsByName(tsignalClass);
    } // setupUi

    void retranslateUi(QMainWindow *tsignalClass)
    {
        tsignalClass->setWindowTitle(QCoreApplication::translate("tsignalClass", "tsignal", nullptr));
    } // retranslateUi

};

namespace Ui {
    class tsignalClass: public Ui_tsignalClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TSIGNAL_H
