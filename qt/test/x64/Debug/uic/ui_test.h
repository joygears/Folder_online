/********************************************************************************
** Form generated from reading UI file 'test.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TEST_H
#define UI_TEST_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_testClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *testClass)
    {
        if (testClass->objectName().isEmpty())
            testClass->setObjectName(QString::fromUtf8("testClass"));
        testClass->resize(600, 400);
        menuBar = new QMenuBar(testClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        testClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(testClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        testClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(testClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        testClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(testClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        testClass->setStatusBar(statusBar);

        retranslateUi(testClass);

        QMetaObject::connectSlotsByName(testClass);
    } // setupUi

    void retranslateUi(QMainWindow *testClass)
    {
        testClass->setWindowTitle(QCoreApplication::translate("testClass", "test", nullptr));
    } // retranslateUi

};

namespace Ui {
    class testClass: public Ui_testClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TEST_H
