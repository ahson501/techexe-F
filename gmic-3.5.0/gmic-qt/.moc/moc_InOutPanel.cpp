/****************************************************************************
** Meta object code from reading C++ file 'InOutPanel.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/Widgets/InOutPanel.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'InOutPanel.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__InOutPanel_t {
    QByteArrayData data[8];
    char stringdata0[122];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__InOutPanel_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__InOutPanel_t qt_meta_stringdata_GmicQt__InOutPanel = {
    {
QT_MOC_LITERAL(0, 0, 18), // "GmicQt::InOutPanel"
QT_MOC_LITERAL(1, 19, 16), // "inputModeChanged"
QT_MOC_LITERAL(2, 36, 0), // ""
QT_MOC_LITERAL(3, 37, 9), // "InputMode"
QT_MOC_LITERAL(4, 47, 19), // "onInputModeSelected"
QT_MOC_LITERAL(5, 67, 20), // "onOutputModeSelected"
QT_MOC_LITERAL(6, 88, 20), // "onResetButtonClicked"
QT_MOC_LITERAL(7, 109, 12) // "setDarkTheme"

    },
    "GmicQt::InOutPanel\0inputModeChanged\0"
    "\0InputMode\0onInputModeSelected\0"
    "onOutputModeSelected\0onResetButtonClicked\0"
    "setDarkTheme"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__InOutPanel[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       5,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   39,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       4,    1,   42,    2, 0x0a /* Public */,
       5,    1,   45,    2, 0x0a /* Public */,
       6,    0,   48,    2, 0x0a /* Public */,
       7,    0,   49,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void, 0x80000000 | 3,    2,

 // slots: parameters
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void GmicQt::InOutPanel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<InOutPanel *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->inputModeChanged((*reinterpret_cast< InputMode(*)>(_a[1]))); break;
        case 1: _t->onInputModeSelected((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 2: _t->onOutputModeSelected((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->onResetButtonClicked(); break;
        case 4: _t->setDarkTheme(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (InOutPanel::*)(InputMode );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&InOutPanel::inputModeChanged)) {
                *result = 0;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::InOutPanel::staticMetaObject = { {
    QMetaObject::SuperData::link<QWidget::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__InOutPanel.data,
    qt_meta_data_GmicQt__InOutPanel,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::InOutPanel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::InOutPanel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__InOutPanel.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int GmicQt::InOutPanel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 5)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 5;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 5)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 5;
    }
    return _id;
}

// SIGNAL 0
void GmicQt::InOutPanel::inputModeChanged(InputMode _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
