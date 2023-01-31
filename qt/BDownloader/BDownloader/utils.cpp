// Created by voidzero <vooidzero.github@qq.com>

#include "utils.h"
#include <QPainter>
#include <QHelpEvent>

void ElidedTextLabel::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    QPainter painter(this);
    if (this->color.isValid()) {
        auto pen = painter.pen();
        pen.setColor(this->color);
        painter.setPen(pen);
    }
    auto fm = fontMetrics();
    auto elidedText = fm.elidedText(text(), elideMode, width());
    painter.drawText(rect(), static_cast<int>(alignment()), elidedText);
}

bool ElidedTextLabel::event(QEvent *e)
{
    if (e->type() == QEvent::ToolTip) {
        auto helpEvent = static_cast<QHelpEvent*>(e);
        auto displayedText = fontMetrics().elidedText(text(), Qt::ElideRight, width());
        if (helpEvent->x() <= fontMetrics().horizontalAdvance(displayedText)) {
            return QLabel::event(e);
        } else {
            return true;
        }
    } else {
        return QLabel::event(e);
    }
}

QSize ElidedTextLabel::minimumSizeHint() const
{
    if (hintWidth == 0) {
        return QLabel::minimumSizeHint();
    } else {
        return QSize(hintWidth, QLabel::minimumSizeHint().height());
    }
}

QSize ElidedTextLabel::sizeHint() const
{
    if (hintWidth == 0) {
        return QLabel::minimumSizeHint();
    } else {
        return QSize(hintWidth, QLabel::minimumSizeHint().height());
    }
}

ElidedTextLabel::ElidedTextLabel(QWidget *parent)
    : QLabel(parent) {}

ElidedTextLabel::ElidedTextLabel(const QString &text, QWidget *parent)
    : QLabel(text, parent)
{
    setToolTip(text);
}

void ElidedTextLabel::setElideMode(Qt::TextElideMode mode)
{
    elideMode = mode;
}

void ElidedTextLabel::setHintWidthToString(const QString &sample)
{
    hintWidth = fontMetrics().horizontalAdvance(sample);
}

void ElidedTextLabel::setFixedWidthToString(const QString &sample)
{
    setFixedWidth(fontMetrics().horizontalAdvance(sample));
}

void ElidedTextLabel::clear()
{
    this->color = QColor();
    QLabel::clear();
}

void ElidedTextLabel::setText(const QString &str, const QColor &color)
{
    QLabel::setText(str);
    this->color = color;
    setToolTip(str);
}

void ElidedTextLabel::setErrText(const QString &str)
{
    QLabel::setText(str);
    this->color = Qt::red;
    setToolTip(str);
}



