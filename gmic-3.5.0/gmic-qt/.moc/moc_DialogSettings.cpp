/****************************************************************************
** Meta object code from reading C++ file 'DialogSettings.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/DialogSettings.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'DialogSettings.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__DialogSettings_t {
    QByteArrayData data[20];
    char stringdata0[335];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__DialogSettings_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__DialogSettings_t qt_meta_stringdata_GmicQt__DialogSettings = {
    {
QT_MOC_LITERAL(0, 0, 22), // "GmicQt::DialogSettings"
QT_MOC_LITERAL(1, 23, 25), // "onRadioLeftPreviewToggled"
QT_MOC_LITERAL(2, 49, 0), // ""
QT_MOC_LITERAL(3, 50, 18), // "onDarkThemeToggled"
QT_MOC_LITERAL(4, 69, 2), // "on"
QT_MOC_LITERAL(5, 72, 15), // "onUpdateClicked"
QT_MOC_LITERAL(6, 88, 4), // "onOk"
QT_MOC_LITERAL(7, 93, 18), // "enableUpdateButton"
QT_MOC_LITERAL(8, 112, 26), // "onUpdatePeriodicityChanged"
QT_MOC_LITERAL(9, 139, 1), // "i"
QT_MOC_LITERAL(10, 141, 21), // "onColorDialogsToggled"
QT_MOC_LITERAL(11, 163, 20), // "onFileDialogsToggled"
QT_MOC_LITERAL(12, 184, 4), // "done"
QT_MOC_LITERAL(13, 189, 1), // "r"
QT_MOC_LITERAL(14, 191, 21), // "onVisibleLogosToggled"
QT_MOC_LITERAL(15, 213, 22), // "onPreviewTimeoutChange"
QT_MOC_LITERAL(16, 236, 26), // "onOutputMessageModeChanged"
QT_MOC_LITERAL(17, 263, 20), // "onPreviewZoomToggled"
QT_MOC_LITERAL(18, 284, 33), // "onNotifyStartupUpdateFailedTo..."
QT_MOC_LITERAL(19, 318, 16) // "onHighDPIToggled"

    },
    "GmicQt::DialogSettings\0onRadioLeftPreviewToggled\0"
    "\0onDarkThemeToggled\0on\0onUpdateClicked\0"
    "onOk\0enableUpdateButton\0"
    "onUpdatePeriodicityChanged\0i\0"
    "onColorDialogsToggled\0onFileDialogsToggled\0"
    "done\0r\0onVisibleLogosToggled\0"
    "onPreviewTimeoutChange\0"
    "onOutputMessageModeChanged\0"
    "onPreviewZoomToggled\0"
    "onNotifyStartupUpdateFailedToggle\0"
    "onHighDPIToggled"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__DialogSettings[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      15,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    1,   89,    2, 0x0a /* Public */,
       3,    1,   92,    2, 0x0a /* Public */,
       5,    0,   95,    2, 0x0a /* Public */,
       6,    0,   96,    2, 0x0a /* Public */,
       7,    0,   97,    2, 0x0a /* Public */,
       8,    1,   98,    2, 0x0a /* Public */,
      10,    1,  101,    2, 0x0a /* Public */,
      11,    1,  104,    2, 0x0a /* Public */,
      12,    1,  107,    2, 0x0a /* Public */,
      14,    1,  110,    2, 0x0a /* Public */,
      15,    1,  113,    2, 0x0a /* Public */,
      16,    1,  116,    2, 0x0a /* Public */,
      17,    1,  119,    2, 0x0a /* Public */,
      18,    1,  122,    2, 0x0a /* Public */,
      19,    1,  125,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    4,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    9,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Int,   13,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Bool,    2,

       0        // eod
};

void GmicQt::DialogSettings::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<DialogSettings *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->onRadioLeftPreviewToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 1: _t->onDarkThemeToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: _t->onUpdateClicked(); break;
        case 3: _t->onOk(); break;
        case 4: _t->enableUpdateButton(); break;
        case 5: _t->onUpdatePeriodicityChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 6: _t->onColorDialogsToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 7: _t->onFileDialogsToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 8: _t->done((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: _t->onVisibleLogosToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 10: _t->onPreviewTimeoutChange((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 11: _t->onOutputMessageModeChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 12: _t->onPreviewZoomToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 13: _t->onNotifyStartupUpdateFailedToggle((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 14: _t->onHighDPIToggled((*reinterpret_cast< bool(*)>(_a[1]))); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::DialogSettings::staticMetaObject = { {
    QMetaObject::SuperData::link<QDialog::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__DialogSettings.data,
    qt_meta_data_GmicQt__DialogSettings,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::DialogSettings::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::DialogSettings::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__DialogSettings.stringdata0))
        return static_cast<void*>(this);
    return QDialog::qt_metacast(_clname);
}

int GmicQt::DialogSettings::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 15)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 15;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 15)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 15;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
