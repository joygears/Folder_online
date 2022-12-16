#include "QPerson.h"

QPerson::QPerson(QObject *parent)
	: QObject(parent)
{
	

}
QPerson::QPerson(QString name, QObject* parent) {
	m_name = name;
}
QPerson::~QPerson()
{


}

unsigned QPerson::age()
{
	return m_age;
}

void QPerson::setAge(unsigned value)
{
	m_age = value;
	emit ageChanged(m_age);
}

void QPerson::incAge()
{
	m_age++;
	emit ageChanged(m_age);
}
