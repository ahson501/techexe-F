/****************************************************************************
** Meta object code from reading C++ file 'HeadlessProcessor.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/HeadlessProcessor.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'HeadlessProcessor.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__HeadlessProcessor_t {
    QByteArrayData data[13];
    char stringdata0[175];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__HeadlessProcessor_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__HeadlessProcessor_t qt_meta_stringdata_GmicQt__HeadlessProcessor = {
    {
QT_MOC_LITERAL(0, 0, 25), // "GmicQt::HeadlessProcessor"
QT_MOC_LITERAL(1, 26, 24), // "progressWindowShouldShow"
QT_MOC_LITERAL(2, 51, 0), // ""
QT_MOC_LITERAL(3, 52, 4), // "done"
QT_MOC_LITERAL(4, 57, 12), // "errorMessage"
QT_MOC_LITERAL(5, 70, 11), // "progression"
QT_MOC_LITERAL(6, 82, 8), // "progress"
QT_MOC_LITERAL(7, 91, 8), // "duration"
QT_MOC_LITERAL(8, 100, 6), // "memory"
QT_MOC_LITERAL(9, 107, 15), // "startProcessing"
QT_MOC_LITERAL(10, 123, 23), // "sendProgressInformation"
QT_MOC_LITERAL(11, 147, 20), // "onProcessingFinished"
QT_MOC_LITERAL(12, 168, 6) // "cancel"

    },
    "GmicQt::HeadlessProcessor\0"
    "progressWindowShouldShow\0\0done\0"
    "errorMessage\0progression\0progress\0"
    "duration\0memory\0startProcessing\0"
    "sendProgressInformation\0onProcessingFinished\0"
    "cancel"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__HeadlessProcessor[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   49,    2, 0x06 /* Public */,
       3,    1,   50,    2, 0x06 /* Public */,
       5,    3,   53,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       9,    0,   60,    2, 0x0a /* Public */,
      10,    0,   61,    2, 0x0a /* Public */,
      11,    0,   62,    2, 0x0a /* Public */,
      12,    0,   63,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    4,
    QMetaType::Void, QMetaType::Float, QMetaType::Int, QMetaType::ULong,    6,    7,    8,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void GmicQt::HeadlessProcessor::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<HeadlessProcessor *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->progressWindowShouldShow(); break;
        case 1: _t->done((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 2: _t->progression((*reinterpret_cast< float(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< ulong(*)>(_a[3]))); break;
        case 3: _t->startProcessing(); break;
        case 4: _t->sendProgressInformation(); break;
        case 5: _t->onProcessingFinished(); break;
        case 6: _t->cancel(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (HeadlessProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&HeadlessProcessor::progressWindowShouldShow)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (HeadlessProcessor::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&HeadlessProcessor::done)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (HeadlessProcessor::*)(float , int , unsigned long );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&HeadlessProcessor::progression)) {
                *result = 2;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::HeadlessProcessor::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__HeadlessProcessor.data,
    qt_meta_data_GmicQt__HeadlessProcessor,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::HeadlessProcessor::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::HeadlessProcessor::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__HeadlessProcessor.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int GmicQt::HeadlessProcessor::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
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
void GmicQt::HeadlessProcessor::progressWindowShouldShow()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void GmicQt::HeadlessProcessor::done(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void GmicQt::HeadlessProcessor::progression(float _t1, int _t2, unsigned long _t3)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t3))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
