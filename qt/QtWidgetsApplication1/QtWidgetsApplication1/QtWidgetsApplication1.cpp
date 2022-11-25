#include "QtWidgetsApplication1.h"
#include <QPushButton>
#include <QMessageBox>
QtWidgetsApplication1::QtWidgetsApplication1(QWidget *parent)
    : QWidget(parent)
{
    
    ui.setupUi(this);
    connect(ui.centerBtn, &QPushButton::clicked, [this]() {

        QMessageBox::StandardButton result = QMessageBox::information(this, "Title", "text");

        });
}

QtWidgetsApplication1::~QtWidgetsApplication1()
{}
