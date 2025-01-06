/****************************************************************************
** Meta object code from reading C++ file 'ProgressInfoWindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/Widgets/ProgressInfoWindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'ProgressInfoWindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__ProgressInfoWindow_t {
    QByteArrayData data[11];
    char stringdata0[126];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__ProgressInfoWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__ProgressInfoWindow_t qt_meta_stringdata_GmicQt__ProgressInfoWindow = {
    {
QT_MOC_LITERAL(0, 0, 26), // "GmicQt::ProgressInfoWindow"
QT_MOC_LITERAL(1, 27, 15), // "onCancelClicked"
QT_MOC_LITERAL(2, 43, 0), // ""
QT_MOC_LITERAL(3, 44, 10), // "onProgress"
QT_MOC_LITERAL(4, 55, 8), // "progress"
QT_MOC_LITERAL(5, 64, 8), // "duration"
QT_MOC_LITERAL(6, 73, 6), // "memory"
QT_MOC_LITERAL(7, 80, 6), // "onInfo"
QT_MOC_LITERAL(8, 87, 4), // "text"
QT_MOC_LITERAL(9, 92, 20), // "onProcessingFinished"
QT_MOC_LITERAL(10, 113, 12) // "errorMessage"

    },
    "GmicQt::ProgressInfoWindow\0onCancelClicked\0"
    "\0onProgress\0progress\0duration\0memory\0"
    "onInfo\0text\0onProcessingFinished\0"
    "errorMessage"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__ProgressInfoWindow[] = {

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
       1,    1,   34,    2, 0x0a /* Public */,
       3,    3,   37,    2, 0x0a /* Public */,
       7,    1,   44,    2, 0x0a /* Public */,
       9,    1,   47,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void, QMetaType::Bool,    2,
    QMetaType::Void, QMetaType::Float, QMetaType::Int, QMetaType::ULong,    4,    5,    6,
    QMetaType::Void, QMetaType::QString,    8,
    QMetaType::Void, QMetaType::QString,   10,

       0        // eod
};

void GmicQt::ProgressInfoWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<ProgressInfoWindow *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->onCancelClicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 1: _t->onProgress((*reinterpret_cast< float(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< ulong(*)>(_a[3]))); break;
        case 2: _t->onInfo((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 3: _t->onProcessingFinished((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::ProgressInfoWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__ProgressInfoWindow.data,
    qt_meta_data_GmicQt__ProgressInfoWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::ProgressInfoWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::ProgressInfoWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__ProgressInfoWindow.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int GmicQt::ProgressInfoWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
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
QT_WARNING_POP
QT_END_MOC_NAMESPACE
