/********************************************************************************
** Form generated from reading UI file 'BDownloader.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_BDOWNLOADER_H
#define UI_BDOWNLOADER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_BDownloaderClass
{
public:
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QWidget *centralWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *BDownloaderClass)
    {
        if (BDownloaderClass->objectName().isEmpty())
            BDownloaderClass->setObjectName(QString::fromUtf8("BDownloaderClass"));
        BDownloaderClass->resize(600, 400);
        menuBar = new QMenuBar(BDownloaderClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        BDownloaderClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(BDownloaderClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        BDownloaderClass->addToolBar(mainToolBar);
        centralWidget = new QWidget(BDownloaderClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        BDownloaderClass->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(BDownloaderClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        BDownloaderClass->setStatusBar(statusBar);

        retranslateUi(BDownloaderClass);

        QMetaObject::connectSlotsByName(BDownloaderClass);
    } // setupUi

    void retranslateUi(QMainWindow *BDownloaderClass)
    {
        BDownloaderClass->setWindowTitle(QCoreApplication::translate("BDownloaderClass", "BDownloader", nullptr));
    } // retranslateUi

};

namespace Ui {
    class BDownloaderClass: public Ui_BDownloaderClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_BDOWNLOADER_H
