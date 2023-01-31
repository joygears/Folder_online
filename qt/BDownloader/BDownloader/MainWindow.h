#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_BDownloader.h"
#include <QVBoxLayout>
#include <QToolButton>
#include <QLineEdit>
#include "utils.h"


class QLabel;
class QLineEdit;
class QPushButton;
class QToolButton;
class QNetworkReply;

class ElidedTextLabel;
class TaskTableWidget;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
private:
    void startGetUserInfo();
private slots:
    void downloadButtonClicked();
    void getUserInfoFinished();
    void ufaceButtonClicked();
private:
    Ui::BDownloaderClass ui;
    
    bool hasGotUInfo = false;
    bool hasGotUFace = false;
    QNetworkReply* uinfoReply = nullptr;
    QString ufaceUrl;

    QToolButton* ufaceButton;
    ElidedTextLabel* unameLabel;
    QLineEdit* urlLineEdit;
    TaskTableWidget* taskTable;

};
