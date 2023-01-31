/****************************************************************************
** Meta object code from reading C++ file 'TaskTable.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../../TaskTable.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'TaskTable.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_TaskTableWidget_t {
    QByteArrayData data[6];
    char stringdata0[99];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_TaskTableWidget_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_TaskTableWidget_t qt_meta_stringdata_TaskTableWidget = {
    {
QT_MOC_LITERAL(0, 0, 15), // "TaskTableWidget"
QT_MOC_LITERAL(1, 16, 17), // "onCellTaskStopped"
QT_MOC_LITERAL(2, 34, 0), // ""
QT_MOC_LITERAL(3, 35, 18), // "onCellTaskFinished"
QT_MOC_LITERAL(4, 54, 21), // "onCellStartBtnClicked"
QT_MOC_LITERAL(5, 76, 22) // "onCellRemoveBtnClicked"

    },
    "TaskTableWidget\0onCellTaskStopped\0\0"
    "onCellTaskFinished\0onCellStartBtnClicked\0"
    "onCellRemoveBtnClicked"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_TaskTableWidget[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       4,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   34,    2, 0x08 /* Private */,
       3,    0,   35,    2, 0x08 /* Private */,
       4,    0,   36,    2, 0x08 /* Private */,
       5,    0,   37,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void TaskTableWidget::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<TaskTableWidget *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->onCellTaskStopped(); break;
        case 1: _t->onCellTaskFinished(); break;
        case 2: _t->onCellStartBtnClicked(); break;
        case 3: _t->onCellRemoveBtnClicked(); break;
        default: ;
        }
    }
    Q_UNUSED(_a);
}

QT_INIT_METAOBJECT const QMetaObject TaskTableWidget::staticMetaObject = { {
    QMetaObject::SuperData::link<QTableWidget::staticMetaObject>(),
    qt_meta_stringdata_TaskTableWidget.data,
    qt_meta_data_TaskTableWidget,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *TaskTableWidget::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *TaskTableWidget::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_TaskTableWidget.stringdata0))
        return static_cast<void*>(this);
    return QTableWidget::qt_metacast(_clname);
}

int TaskTableWidget::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QTableWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 4)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 4;
    }
    return _id;
}
struct qt_meta_stringdata_TaskCellWidget_t {
    QByteArrayData data[10];
    char stringdata0[121];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_TaskCellWidget_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_TaskCellWidget_t qt_meta_stringdata_TaskCellWidget = {
    {
QT_MOC_LITERAL(0, 0, 14), // "TaskCellWidget"
QT_MOC_LITERAL(1, 15, 15), // "downloadStopped"
QT_MOC_LITERAL(2, 31, 0), // ""
QT_MOC_LITERAL(3, 32, 16), // "downloadFinished"
QT_MOC_LITERAL(4, 49, 15), // "startBtnClicked"
QT_MOC_LITERAL(5, 65, 16), // "removeBtnClicked"
QT_MOC_LITERAL(6, 82, 15), // "onErrorOccurred"
QT_MOC_LITERAL(7, 98, 6), // "errStr"
QT_MOC_LITERAL(8, 105, 10), // "onFinished"
QT_MOC_LITERAL(9, 116, 4) // "open"

    },
    "TaskCellWidget\0downloadStopped\0\0"
    "downloadFinished\0startBtnClicked\0"
    "removeBtnClicked\0onErrorOccurred\0"
    "errStr\0onFinished\0open"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_TaskCellWidget[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   49,    2, 0x06 /* Public */,
       3,    0,   50,    2, 0x06 /* Public */,
       4,    0,   51,    2, 0x06 /* Public */,
       5,    0,   52,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       6,    1,   53,    2, 0x08 /* Private */,
       8,    0,   56,    2, 0x08 /* Private */,
       9,    0,   57,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::QString,    7,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void TaskCellWidget::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<TaskCellWidget *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->downloadStopped(); break;
        case 1: _t->downloadFinished(); break;
        case 2: _t->startBtnClicked(); break;
        case 3: _t->removeBtnClicked(); break;
        case 4: _t->onErrorOccurred((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 5: _t->onFinished(); break;
        case 6: _t->open(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (TaskCellWidget::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TaskCellWidget::downloadStopped)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (TaskCellWidget::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TaskCellWidget::downloadFinished)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (TaskCellWidget::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TaskCellWidget::startBtnClicked)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (TaskCellWidget::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TaskCellWidget::removeBtnClicked)) {
                *result = 3;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject TaskCellWidget::staticMetaObject = { {
    QMetaObject::SuperData::link<QWidget::staticMetaObject>(),
    qt_meta_stringdata_TaskCellWidget.data,
    qt_meta_data_TaskCellWidget,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *TaskCellWidget::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *TaskCellWidget::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_TaskCellWidget.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int TaskCellWidget::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 7)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 7;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 7)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 7;
    }
    return _id;
}

// SIGNAL 0
void TaskCellWidget::downloadStopped()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void TaskCellWidget::downloadFinished()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void TaskCellWidget::startBtnClicked()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void TaskCellWidget::removeBtnClicked()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
