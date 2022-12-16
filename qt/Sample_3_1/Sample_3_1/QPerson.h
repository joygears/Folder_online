#pragma once

#include <QObject>

class QPerson  : public QObject
{
	Q_OBJECT
	Q_CLASSINFO("author","CZL")
	Q_CLASSINFO("company","Tenorshare")
	Q_CLASSINFO("version","1.0")
	Q_PROPERTY(unsigned age READ age WRITE setAge NOTIFY ageChanged)
	Q_PROPERTY(QString name MEMBER m_name)
	Q_PROPERTY(int  score MEMBER m_socre)
public:
	QPerson(QObject *parent);
	QPerson(QString name, QObject* parent=nullptr);
	~QPerson();
	unsigned age();
	void setAge(unsigned value);
	void incAge();

signals:
	void ageChanged(unsigned value);
private:
	unsigned m_age = 10;
	QString m_name;
	unsigned m_socre = 79;
};
