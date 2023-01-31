/********************************************************************************
** Form generated from reading UI file 'uiFit.ui'
**
** Created by: Qt User Interface Compiler version 5.15.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_UIFIT_H
#define UI_UIFIT_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_uiFitClass
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QToolButton *toolButton;
    QSpacerItem *horizontalSpacer;
    QHBoxLayout *horizontalLayout;
    QLineEdit *lineEdit;
    QPushButton *pushButton_2;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *uiFitClass)
    {
        if (uiFitClass->objectName().isEmpty())
            uiFitClass->setObjectName(QString::fromUtf8("uiFitClass"));
        uiFitClass->resize(402, 543);
        centralWidget = new QWidget(uiFitClass);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        toolButton = new QToolButton(centralWidget);
        toolButton->setObjectName(QString::fromUtf8("toolButton"));
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(toolButton->sizePolicy().hasHeightForWidth());
        toolButton->setSizePolicy(sizePolicy);
        toolButton->setMinimumSize(QSize(32, 32));
        toolButton->setMaximumSize(QSize(32, 32));
        toolButton->setBaseSize(QSize(0, 0));
        QFont font;
        font.setPointSize(10);
        font.setBold(true);
        font.setWeight(75);
        toolButton->setFont(font);
        toolButton->setCursor(QCursor(Qt::PointingHandCursor));
        toolButton->setStyleSheet(QString::fromUtf8(" QToolButton {\n"
"            color: #00a1d6;\n"
"            background-color: white;\n"
"            border: none;\n"
"        }\n"
"        QToolButton::menu-indicator { image: none; }"));
        toolButton->setIconSize(QSize(32, 32));
        toolButton->setPopupMode(QToolButton::InstantPopup);

        horizontalLayout_2->addWidget(toolButton);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(0);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        lineEdit = new QLineEdit(centralWidget);
        lineEdit->setObjectName(QString::fromUtf8("lineEdit"));
        lineEdit->setMinimumSize(QSize(0, 32));
        lineEdit->setClearButtonEnabled(true);

        horizontalLayout->addWidget(lineEdit);

        pushButton_2 = new QPushButton(centralWidget);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setMinimumSize(QSize(32, 32));
        pushButton_2->setStyleSheet(QString::fromUtf8("QPushButton{border:1px solid gray; border-left:0px; background-color:white;}\n"
"QPushButton:hover{background-color:rgb(229,229,229);}\n"
"QPushButton:pressed{background-color:rgb(204,204,204);}"));

        horizontalLayout->addWidget(pushButton_2);


        horizontalLayout_2->addLayout(horizontalLayout);


        verticalLayout->addLayout(horizontalLayout_2);

        uiFitClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(uiFitClass);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 402, 23));
        uiFitClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(uiFitClass);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        uiFitClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(uiFitClass);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        uiFitClass->setStatusBar(statusBar);

        retranslateUi(uiFitClass);

        QMetaObject::connectSlotsByName(uiFitClass);
    } // setupUi

    void retranslateUi(QMainWindow *uiFitClass)
    {
        uiFitClass->setWindowTitle(QCoreApplication::translate("uiFitClass", "uiFit", nullptr));
        toolButton->setText(QCoreApplication::translate("uiFitClass", "\347\231\273\345\275\225", nullptr));
#if QT_CONFIG(tooltip)
        lineEdit->setToolTip(QCoreApplication::translate("uiFitClass", "\344\270\213\350\275\275", nullptr));
#endif // QT_CONFIG(tooltip)
        lineEdit->setPlaceholderText(QCoreApplication::translate("uiFitClass", "bilibili \347\233\264\346\222\255/\350\247\206\351\242\221/\346\274\253\347\224\273 URL", nullptr));
        pushButton_2->setText(QCoreApplication::translate("uiFitClass", "\344\270\213\350\275\275", nullptr));
    } // retranslateUi

};

namespace Ui {
    class uiFitClass: public Ui_uiFitClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_UIFIT_H
