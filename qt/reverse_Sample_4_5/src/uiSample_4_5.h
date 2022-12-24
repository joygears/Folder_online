#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QGroupBox>
#include <QGridLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QDateEdit>
#include <QDateTimeEdit>

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
			
			gridLayout->addWidget(btnSetTime,1,4,1,1);
			
			label_3 = new QLabel(this->groupBox,Qt::Widget);
			label_3->setObjectName(QString::fromUtf8("label_3"));
			
			gridLayout->addWidget(label_3,2,0,1,1);
			
			lineEditDate = new QLineEdit(groupBox);
			lineEditDate->setObjectName(QString::fromUtf8("lineEditDate"));
			
			gridLayout->addWidget(lineEditDate,2,3,1,1);
			
			btnSetDate = new QPushButton(groupBox);
			btnSetDate->setObjectName(QString::fromUtf8("btnSetDate"));
			
			gridLayout->addWidget(lineEditDate,2,4,1,1);
			
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
			
			gridLayout->addWidget(dateTimeEdit,3,4,1,1);
			
			btnGetTime = new QPushButton(this->groupBox);
			btnGetTime->setObjectName(QString::fromUtf8("btnGetTime"));
			
			gridLayout->addWidget(dateTimeEdit,0,0,1,3);
			
			//0000000140002B57
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
		QPushButton * btnGetTime; //58
};