#include "MainWindow.h"
#include "Network.h"
#include "Settings.h"
#include <QPushButton>
#include "TaskTable.h"
#include "AboutWidget.h"
#include "MyTabWidget.h"
#include <QTimer>
#include <QtNetwork>

static constexpr int GetUserInfoRetryInterval = 10000; // ms
static constexpr int GetUserInfoTimeout = 10000; // ms

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
   // ui.setupUi(this);
#ifdef APP_VERSION
    QApplication::setApplicationVersion(APP_VERSION);
#endif
    Network::accessManager()->setCookieJar(Settings::inst()->getCookieJar());
    setWindowTitle("B23Downloader");
    setCentralWidget(new QWidget);
    auto mainLayout = new QVBoxLayout(centralWidget());
    auto topLayout = new QHBoxLayout;

    // set up user info widgets
    ufaceButton = new QToolButton;
    ufaceButton->setText(QString::fromLocal8Bit("µÇÂ¼"));
    ufaceButton->setFixedSize(32, 32);
    ufaceButton->setIconSize(QSize(32, 32));
    ufaceButton->setCursor(Qt::PointingHandCursor);
    auto loginTextFont = font();
    loginTextFont.setBold(true);
    loginTextFont.setPointSize(font().pointSize() + 1);
    ufaceButton->setFont(loginTextFont);
    ufaceButton->setPopupMode(QToolButton::InstantPopup);
    ufaceButton->setStyleSheet(R"(
        QToolButton {
            color: #00a1d6;
            background-color: white;
            border: none;
        }
        QToolButton::menu-indicator { image: none; }
    )");
    connect(ufaceButton, &QToolButton::clicked, this, &MainWindow::ufaceButtonClicked);
    unameLabel = new ElidedTextLabel;
    unameLabel->setHintWidthToString(QString::fromLocal8Bit("Íí°²Âê¿¨°Í¿¨£¡¤ä¤µ¤·¤¤‰ôÒŠ¤Æ¤Í"));
    topLayout->addWidget(ufaceButton);
    topLayout->addWidget(unameLabel, 1);
    
    // set up download url lineEdit
    auto downloadUrlLayout = new QHBoxLayout;
    downloadUrlLayout->setSpacing(0);
    urlLineEdit = new QLineEdit;
    urlLineEdit->setFixedHeight(32);
    urlLineEdit->setClearButtonEnabled(true);
    urlLineEdit->setPlaceholderText(QString::fromLocal8Bit("bilibili Ö±²¥/ÊÓÆµ/Âþ»­ URL"));

    auto downloadButton = new QPushButton;
    downloadButton->setToolTip(QString::fromLocal8Bit("ÏÂÔØ"));
    downloadButton->setFixedSize(QSize(32, 32));
    downloadButton->setIconSize(QSize(28, 28));
    downloadButton->setIcon(QIcon(":/icons/download.svg"));
    downloadButton->setCursor(Qt::PointingHandCursor);
    downloadButton->setStyleSheet(
        "QPushButton{border:1px solid gray; border-left:0px; background-color:white;}"
        "QPushButton:hover{background-color:rgb(229,229,229);}"
        "QPushButton:pressed{background-color:rgb(204,204,204);}"
    );
    connect(urlLineEdit, &QLineEdit::returnPressed, this, &MainWindow::downloadButtonClicked);
    connect(downloadButton, &QPushButton::clicked, this, &MainWindow::downloadButtonClicked);

    downloadUrlLayout->addWidget(urlLineEdit, 1);
    downloadUrlLayout->addWidget(downloadButton);
    topLayout->addLayout(downloadUrlLayout, 2);
    mainLayout->addLayout(topLayout);

    taskTable = new TaskTableWidget;
    QTimer::singleShot(0, this, [this] { taskTable->load(); });
    auto tabs = new MyTabWidget;
    tabs->addTab(taskTable, QIcon(":/icons/download.svg"), QString::fromLocal8Bit("ÕýÔÚÏÂÔØ"));
    tabs->addTab(new AboutWidget, QIcon(":/icons/about.svg"), QString::fromLocal8Bit("¹ØÓÚ"));
    mainLayout->addWidget(tabs);

    setStyleSheet("QMainWindow{background-color:white;}QTableWidget{border:none;}");
    setMinimumSize(650, 360);
    QTimer::singleShot(0, this, [this] { resize(minimumSize()); });
    
    urlLineEdit->setFocus();
    startGetUserInfo();
}

MainWindow::~MainWindow()
{

}

void MainWindow::startGetUserInfo()
{
    if (!Settings::inst()->hasCookies()) {
        return;
    }
    if (hasGotUInfo || uinfoReply != nullptr) {
        return;
    }
    unameLabel->setText("µÇÂ¼ÖÐ...", Qt::gray);
    auto rqst = Network::Bili::Request(QUrl("https://api.bilibili.com/nav"));
    rqst.setTransferTimeout(GetUserInfoTimeout);
    uinfoReply = Network::accessManager()->get(rqst);;
    connect(uinfoReply, &QNetworkReply::finished, this, &MainWindow::getUserInfoFinished);
}

// login
void MainWindow::ufaceButtonClicked()
{
    auto settings = Settings::inst();
    if (hasGotUInfo) {
        return;
    }
    
}
void MainWindow::downloadButtonClicked()
{
    auto trimmed = urlLineEdit->text().trimmed();
    if (trimmed.isEmpty()) {
        urlLineEdit->clear();
        return;
    }

   
}

void MainWindow::getUserInfoFinished()
{
    auto reply = uinfoReply;
    uinfoReply->deleteLater();
    uinfoReply = nullptr;

    if (reply->error() == QNetworkReply::OperationCanceledError) {
        unameLabel->setErrText("ÍøÂçÇëÇó³¬Ê±");
        QTimer::singleShot(GetUserInfoRetryInterval, this, &MainWindow::startGetUserInfo);
        return;
    }

    //const auto [json, errorString] = Network::Bili::parseReply(reply, "data");

    //if (!json.empty() && !errorString.isNull()) {
    //    // cookies is wrong, or expired?
    //    unameLabel->clear();
    //    Settings::inst()->removeCookies();
    //}
    //else if (!errorString.isNull()) {
    //    unameLabel->setErrText(errorString);
    //    QTimer::singleShot(GetUserInfoRetryInterval, this, &MainWindow::startGetUserInfo);
    //}
    //else {
    //    // success
    //    hasGotUInfo = true;
    //    auto data = json["data"];
    //    auto uname = data["uname"].toString();
    //    ufaceUrl = data["face"].toString() + "@64w_64h.png";
    //    if (data["vipStatus"].toInt()) {
    //        unameLabel->setText(uname, B23Style::Pink);
    //    }
    //    else {
    //        unameLabel->setText(uname);
    //    }

    //    auto logoutAction = new QAction(QIcon(":/icons/logout.svg"), "ÍË³ö");
    //    ufaceButton->addAction(logoutAction);
    //    ufaceButton->setIcon(QIcon(":/icons/akkarin.png"));
    //    connect(logoutAction, &QAction::triggered, this, &MainWindow::logoutActionTriggered);

    //    startGetUFace();
    //}
}