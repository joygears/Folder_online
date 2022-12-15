/****************************************************************************
** Meta object code from reading C++ file 'sample_2_4.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.12.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../sample_2_4.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'sample_2_4.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.12.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_sample_2_4_t {
    QByteArrayData data[13];
    char stringdata0[214];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_sample_2_4_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_sample_2_4_t qt_meta_stringdata_sample_2_4 = {
    {
QT_MOC_LITERAL(0, 0, 10), // "sample_2_4"
QT_MOC_LITERAL(1, 11, 20), // "on_actBold_triggered"
QT_MOC_LITERAL(2, 32, 0), // ""
QT_MOC_LITERAL(3, 33, 7), // "checked"
QT_MOC_LITERAL(4, 41, 22), // "on_actItalic_triggered"
QT_MOC_LITERAL(5, 64, 25), // "on_actUnderline_triggered"
QT_MOC_LITERAL(6, 90, 25), // "on_textEdit_copyAvailable"
QT_MOC_LITERAL(7, 116, 8), // "copyable"
QT_MOC_LITERAL(8, 125, 28), // "on_textEdit_selectionChanged"
QT_MOC_LITERAL(9, 154, 28), // "on_spinFontSize_valueChanged"
QT_MOC_LITERAL(10, 183, 8), // "fontSize"
QT_MOC_LITERAL(11, 192, 16), // "ChangeFontFamily"
QT_MOC_LITERAL(12, 209, 4) // "font"

    },
    "sample_2_4\0on_actBold_triggered\0\0"
    "checked\0on_actItalic_triggered\0"
    "on_actUnderline_triggered\0"
    "on_textEdit_copyAvailable\0copyable\0"
    "on_textEdit_selectionChanged\0"
    "on_spinFontSize_valueChanged\0fontSize\0"
    "ChangeFontFamily\0font"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_sample_2_4[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   49,    2, 0x08 /* Private */,
       4,    1,   52,    2, 0x08 /* Private */,
       5,    1,   55,    2, 0x08 /* Private */,
       6,    1,   58,    2, 0x08 /* Private */,
       8,    0,   61,    2, 0x08 /* Private */,
       9,    1,   62,    2, 0x08 /* Private */,
      11,    1,   65,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void, QMetaType::Bool,    3,
    QMetaType::Void, QMetaType::Bool,    3,
    QMetaType::Void, QMetaType::Bool,    3,
    QMetaType::Void, QMetaType::Bool,    7,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,   10,
    QMetaType::Void, QMetaType::QFont,   12,

       0        // eod
};

void sample_2_4::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<sample_2_4 *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->on_actBold_triggered((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 1: _t->on_actItalic_triggered((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: _t->on_actUnderline_triggered((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 3: _t->on_textEdit_copyAvailable((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 4: _t->on_textEdit_selectionChanged(); break;
        case 5: _t->on_spinFontSize_valueChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 6: _t->ChangeFontFamily((*reinterpret_cast< const QFont(*)>(_a[1]))); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject sample_2_4::staticMetaObject = { {
    &QMainWindow::staticMetaObject,
    qt_meta_stringdata_sample_2_4.data,
    qt_meta_data_sample_2_4,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *sample_2_4::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *sample_2_4::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_sample_2_4.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int sample_2_4::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
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
QT_WARNING_POP
QT_END_MOC_NAMESPACE
