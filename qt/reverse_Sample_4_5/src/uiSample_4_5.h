#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QGridLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QDateEdit>
#include <QDateTimeEdit>
#include <QTimeEdit>
#include <QSpacerItem>
#include <QSpinBox>
#include <QLCDNumber>
#include <QProgressBar>
#include <QBoxLayout>
#include <QCalendarWidget>
#include <QCoreApplication>

class ui_Sample_4_5{
	
	
		
	public:
	
		void setUI(QWidget * pMainWindow){
			int count = pMainWindow->objectName().count();
			if(count == 0){
				pMainWindow->setObjectName(QString::fromUtf8("Sample_4_5Class"));
			}
			pMainWindow->resize(885,400);
			horizontalLayout = new QHBoxLayout(pMainWindow);
			horizontalLayout->setSpacing(6);
			horizontalLayout->setContentsMargins(11,11,11,11);
			horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
			
			verticalLayout_2 = new QVBoxLayout();
			verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
			
			groupBox = new QGroupBox(pMainWindow);
			groupBox->setObjectName(QString::fromUtf8("groupBox"));
			
			gridLayout = new QGridLayout(this->groupBox);
			gridLayout->setSpacing(6);
			gridLayout->setContentsMargins(11,11,11,11);
			gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
			
			btnSetTime = new QPushButton(this->groupBox);
			btnSetTime->setObjectName(QString::fromUtf8("btnSetTime"));
			
			gridLayout->addWidget(btnSetTime,1,4,1,1,0);
			
			label_3 = new QLabel(this->groupBox,Qt::Widget);
			label_3->setObjectName(QString::fromUtf8("label_3"));
			
			gridLayout->addWidget(label_3,2,0,1,1);
			
			lineEditDate = new QLineEdit(groupBox);
			lineEditDate->setObjectName(QString::fromUtf8("lineEditDate"));
			
			gridLayout->addWidget(lineEditDate,2,3,1,1);
			
			btnSetDate = new QPushButton(groupBox);
			btnSetDate->setObjectName(QString::fromUtf8("btnSetDate"));
			
			gridLayout->addWidget(btnSetDate,2,4,1,1);
			
			dateEdit = new QDateEdit(groupBox);
			dateEdit->setObjectName(QString::fromUtf8("dateEdit"));
			dateEdit->setWrapping(false);
			dateEdit->setFrame(true);
			dateEdit->setCorrectionMode(QAbstractSpinBox::CorrectToPreviousValue);
			dateEdit->setCalendarPopup(true);
			dateEdit->setTimeSpec(Qt::LocalTime);
			dateEdit->setDate(QDate(2022,7,14));
			
			gridLayout->addWidget(dateEdit,2,1,1,2);
			
			label = new QLabel(groupBox);
			label->setObjectName(QString::fromUtf8("label"));
			
			gridLayout->addWidget(label,0,3,1,1);
			
			
			dateTimeEdit = new QDateTimeEdit(groupBox);
			dateTimeEdit->setObjectName(QString::fromUtf8("dateTimeEdit"));
			
			gridLayout->addWidget(dateTimeEdit,3,1,1,2);
			
			btnSetDateTime = new QPushButton(this->groupBox);
			btnSetDateTime->setObjectName(QString::fromUtf8("btnSetDateTime"));
			
			gridLayout->addWidget(btnSetDateTime,3,4,1,1);
			
			btnGetTime = new QPushButton(this->groupBox);
			btnGetTime->setObjectName(QString::fromUtf8("btnGetTime"));
			
			gridLayout->addWidget(btnGetTime,0,0,1,3);
			
			label_4 = new QLabel(groupBox,Qt::Widget);
			label_4->setObjectName(QString::fromUtf8("label_4"));
			
			gridLayout->addWidget(label_4,3,0,1,1);
			
			timeEditCurrent = new QTimeEdit(groupBox);
			timeEditCurrent->setObjectName(QString::fromUtf8("timeEditCurrent"));
			timeEditCurrent->setMinimumSize(QSize(64,0));
			timeEditCurrent->setCurrentSection(QDateTimeEdit::HourSection);
			timeEditCurrent->setTime(QTime(15,10,30,0));
			
			gridLayout->addWidget(timeEditCurrent,1,1,1,1);
			
			spacerItem = new QSpacerItem(57,20,QSizePolicy::Expanding,QSizePolicy::Minimum);
			
			gridLayout->addItem(spacerItem,1,2,1,1);
			
			lineEditTime = new QLineEdit(groupBox);
			lineEditTime->setObjectName(QString::fromUtf8("lineEditTime"));
			
			gridLayout->addWidget(lineEditTime,1,3,1,1);
			
			label_2 = new QLabel(groupBox,Qt::Widget);
			label_2->setObjectName(QString::fromUtf8("label_2"));
			
			gridLayout->addWidget(label_2,1,0,1,1);
			
			lineEditDateTime = new QLineEdit(groupBox);
			lineEditDateTime->setObjectName(QString::fromUtf8("lineEditDateTime"));
			
			gridLayout->addWidget(lineEditDateTime,3,3,1,1);
			
			verticalLayout_2->addWidget(groupBox,0,0);
			
			groupBox_2 = new QGroupBox(pMainWindow);
			groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
			
			gridLayout_2 = new QGridLayout(this->groupBox_2);
			gridLayout_2->setSpacing(6);
			gridLayout_2->setContentsMargins(11,11,11,11);
			gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
			
			horizontalLayout_4 = new QHBoxLayout();
			horizontalLayout_4->setSpacing(6);
			horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
			
			btnStart = new QPushButton(groupBox_2);
			btnStart->setObjectName(QString::fromUtf8("btnStart"));
			
			horizontalLayout_4->addWidget(btnStart,0,0);
			
			btnStop = new QPushButton(groupBox_2);
			btnStop->setObjectName(QString::fromUtf8("btnStop"));
			btnStop->setEnabled(false);
			btnStop->setCheckable(false);
			btnStop->setAutoDefault(false);
			btnStop->setFlat(false);
			
			horizontalLayout_4->addWidget(btnStop,0,0);
			
			labelEcilpse = new QLabel(groupBox_2,Qt::Widget);
			labelEcilpse->setObjectName(QString::fromUtf8("labelEcilpse"));
			
			horizontalLayout_4->addWidget(labelEcilpse,0,0);
			gridLayout_2->addLayout(horizontalLayout_4,0,0,1,1,0);
			
			horizontalLayout_3 = new QHBoxLayout();
			horizontalLayout_3->setSpacing(6);
			horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
			
			label_6 = new QLabel(groupBox_2,Qt::Widget);
			label_6->setObjectName(QString::fromUtf8("label_6"));
			
			horizontalLayout_3->addWidget(label_6,0,0);
			
			spinInternal = new QSpinBox(groupBox_2);
			spinInternal->setObjectName(QString::fromUtf8("spinInternal"));
			spinInternal->setMaximum(99999);
			spinInternal->setSingleStep(1000);
			spinInternal->setValue(1000);
			
			horizontalLayout_3->addWidget(spinInternal,0,0);
			
			btnSetInternal = new QPushButton(groupBox_2);
			btnSetInternal->setObjectName(QString::fromUtf8("btnSetInternal"));
			
			horizontalLayout_3->addWidget(btnSetInternal,0,0);
			
			spacerItem_2 = new QSpacerItem(99,17,QSizePolicy::Expanding,QSizePolicy::Minimum);
			
			horizontalLayout_3->addItem(spacerItem_2);
			
			gridLayout_2->addLayout(horizontalLayout_3,1,0,1,1,0);
			
			horizontalLayout_2 = new QHBoxLayout();
			horizontalLayout_2->setSpacing(6);
			horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
			
			lcdHour = new QLCDNumber();
			lcdHour->setObjectName(QString::fromUtf8("lcdHour"));
			lcdHour->setContextMenuPolicy(Qt::DefaultContextMenu);
			lcdHour->setLayoutDirection(Qt::LeftToRight);
			lcdHour->setAutoFillBackground(false);
			lcdHour->setFrameShape(QFrame::Box);
			lcdHour->setFrameShadow(QFrame::Raised);
			lcdHour->setLineWidth(1);
			lcdHour->setMidLineWidth(0);
			lcdHour->setSmallDecimalPoint(false);
			lcdHour->setDigitCount(2);
			lcdHour->setSegmentStyle(QLCDNumber::Flat);
			
			horizontalLayout_2->addWidget(lcdHour,0,0);
			
			lcdMinute = new QLCDNumber();
			lcdMinute->setObjectName(QString::fromUtf8("lcdMinute"));
			lcdMinute->setSmallDecimalPoint(false);
			lcdMinute->setDigitCount(2);
			lcdMinute->setSegmentStyle(QLCDNumber::Flat);
			
			horizontalLayout_2->addWidget(lcdMinute,0,0);
			
			lcdSecond = new QLCDNumber();
			lcdSecond->setObjectName(QString::fromUtf8("lcdSecond"));
			lcdSecond->setDigitCount(2);
			lcdSecond->setSegmentStyle(QLCDNumber::Flat);
			horizontalLayout_2->addWidget(lcdSecond,0,0);
			
			gridLayout_2->addLayout(horizontalLayout_2,2,0,1,1,0);
			
			progressBar = new QProgressBar(groupBox_2);
			progressBar->setObjectName(QString::fromUtf8("progressBar"));
			progressBar->setValue(24);
			gridLayout_2->addWidget(progressBar,3,0,1,1,0);
			
			verticalLayout_2->addWidget(groupBox_2,0,0);
			
			horizontalLayout->addLayout(verticalLayout_2,0);
			
			verticalLayout = new QVBoxLayout();
			verticalLayout->setSpacing(6);
			verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
			
			groupBox_3 = new QGroupBox(pMainWindow);
			groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
			
			gridLayout_3 = new QGridLayout(groupBox_3);
			gridLayout_3->setSpacing(6);
			gridLayout_3->setContentsMargins(11,11,11,11);
			gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
			
			label_7 = new QLabel(groupBox_3,Qt::Widget);
			label_7->setObjectName(QString::fromUtf8("label_7"));
			
			gridLayout_3->addWidget(label_7,0,0,1,1,0);
			
			lineEditSelectedDate = new QLineEdit(groupBox_3);
			lineEditSelectedDate->setObjectName(QString::fromUtf8("lineEditSelectedDate"));
		
			gridLayout_3->addWidget(lineEditSelectedDate,0,1,1,1,0);
		
			calendarWidget = new QCalendarWidget(groupBox_3);
			calendarWidget->setObjectName(QString::fromUtf8("calendarWidget"));
			
			gridLayout_3->addWidget(calendarWidget,1,0,1,2,0);
			verticalLayout->addWidget(groupBox_3,0,0);
			
			spacerItem_3 = new QSpacerItem(20,40,QSizePolicy::Minimum,QSizePolicy::Expanding);
		
			verticalLayout->addItem(spacerItem_3);
		
			btnClose = new QPushButton(pMainWindow);
			btnClose->setObjectName(QString::fromUtf8("btnClose"));
			
			verticalLayout->addWidget(btnClose,0,0);
		
			spacerItem_4 = new QSpacerItem(20,40,QSizePolicy::Minimum,QSizePolicy::Expanding);
			
			verticalLayout->addItem(spacerItem_4);
			
			horizontalLayout->addLayout(verticalLayout,0);
			
			reTranslateUi(pMainWindow);
			
			QObject::connect(btnClose,"2clicked()",pMainWindow,"1close()",Qt::AutoConnection);
			
			QMetaObject::connectSlotsByName(pMainWindow);
		}
		void reTranslateUi(QWidget * pMainWindow){
			
			pMainWindow->setWindowTitle(QCoreApplication::translate("Sample_4_5Class", "Sample_4_5", 0, -1));
			groupBox->setTitle(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("日期时间").toUtf8(), 0, -1));
			btnSetTime->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("设置时间").toUtf8(), 0, -1));
			label_3->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("日 期").toUtf8(), 0, -1));
			btnSetDate->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("设置日期").toUtf8(), 0, -1));
			dateEdit->setDisplayFormat(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("yyyy年M月d日").toUtf8(), 0, -1));
			label->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("字符串显示").toUtf8(), 0, -1));
			dateTimeEdit->setDisplayFormat(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("yyyy-M-d HH:mm:ss").toUtf8(), 0, -1));
			btnSetDateTime->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("设置日期时间").toUtf8(), 0, -1));
			btnGetTime->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("读取当前日期时间").toUtf8(), 0, -1));
			label_4->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("日期时间").toUtf8(), 0, -1));
			timeEditCurrent->setDisplayFormat(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("H:mm:ss").toUtf8(), 0, -1));
			label_2->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("时 间").toUtf8(), 0, -1));
			groupBox_2->setTitle(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("定时器").toUtf8(), 0, -1));
			btnStart->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("开始").toUtf8(), 0, -1));
			btnStop->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("停止").toUtf8(), 0, -1));
			labelEcilpse->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("流逝时间").toUtf8(), 0, -1));
			label_6->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("定时周期").toUtf8(), 0, -1));
			spinInternal->setSuffix(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit(" ms").toUtf8(), 0, -1));
			btnSetInternal->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("设置周期").toUtf8(), 0, -1));
			groupBox_3->setTitle(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("日历选择").toUtf8(), 0, -1));
			label_7->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("选择的日期：").toUtf8(), 0, -1));
			btnClose->setText(QCoreApplication::translate("Sample_4_5Class", QString::fromLocal8Bit("停止").toUtf8(), 0, -1));
			
			
			
		}
	public:
		QHBoxLayout * horizontalLayout; //0
		QVBoxLayout * verticalLayout_2; //8
		QGroupBox * groupBox; //10
		QGridLayout * gridLayout; //18
		QPushButton * btnSetTime; // 20
		QLabel * label_3; // 28
		QLineEdit * lineEditDate; // 30
		QPushButton * btnSetDate; // 38
		QDateEdit * dateEdit;//40
		QLabel * label;// 48
		QDateTimeEdit * dateTimeEdit; //50
		QPushButton * btnSetDateTime; //58
		QPushButton * btnGetTime; //60
		QLabel *label_4; // 68
		QTimeEdit * timeEditCurrent; //70
		QSpacerItem * spacerItem; // 78
		QLineEdit * lineEditTime; // 80
		QLabel * label_2; //88
		QLineEdit * lineEditDateTime; // 90
		QGroupBox * groupBox_2; // 98
		QGridLayout * gridLayout_2; //A0
		QHBoxLayout * horizontalLayout_4; //A8
		QPushButton * btnStart; // B0
		QPushButton * btnStop; // B8
		QLabel * labelEcilpse; // C0
		QHBoxLayout * horizontalLayout_3; // C8
		QLabel * label_6; // D0
		QSpinBox * spinInternal; // D8
		QPushButton * btnSetInternal; //E0
		QSpacerItem * spacerItem_2; // E8
		QHBoxLayout * horizontalLayout_2;// F0
		QLCDNumber * lcdHour;// F8
		QLCDNumber * lcdMinute;//100
		QLCDNumber * lcdSecond; //108
		QProgressBar * progressBar; // 110
		QVBoxLayout * verticalLayout; // 118
		QGroupBox * groupBox_3;//120
		QGridLayout * gridLayout_3;//128
		QLabel  * label_7;//130
		QLineEdit * lineEditSelectedDate; // 138
		QCalendarWidget * calendarWidget;//140
		QSpacerItem * spacerItem_3; // 148
		QPushButton * btnClose;//150
		QSpacerItem * spacerItem_4; // 158
		
		
};