/****************************************************************************
** Meta object code from reading C++ file 'GmicProcessor.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/GmicProcessor.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'GmicProcessor.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__GmicProcessor_t {
    QByteArrayData data[19];
    char stringdata0[388];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__GmicProcessor_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__GmicProcessor_t qt_meta_stringdata_GmicQt__GmicProcessor = {
    {
QT_MOC_LITERAL(0, 0, 21), // "GmicQt::GmicProcessor"
QT_MOC_LITERAL(1, 22, 20), // "previewCommandFailed"
QT_MOC_LITERAL(2, 43, 0), // ""
QT_MOC_LITERAL(3, 44, 12), // "errorMessage"
QT_MOC_LITERAL(4, 57, 25), // "fullImageProcessingFailed"
QT_MOC_LITERAL(5, 83, 21), // "previewImageAvailable"
QT_MOC_LITERAL(6, 105, 18), // "guiDynamismRunDone"
QT_MOC_LITERAL(7, 124, 23), // "fullImageProcessingDone"
QT_MOC_LITERAL(8, 148, 20), // "noMoreUnfinishedJobs"
QT_MOC_LITERAL(9, 169, 23), // "aboutToSendImagesToHost"
QT_MOC_LITERAL(10, 193, 6), // "cancel"
QT_MOC_LITERAL(11, 200, 33), // "detachAllUnfinishedAbortedThr..."
QT_MOC_LITERAL(12, 234, 19), // "terminateAllThreads"
QT_MOC_LITERAL(13, 254, 23), // "onPreviewThreadFinished"
QT_MOC_LITERAL(14, 278, 21), // "onApplyThreadFinished"
QT_MOC_LITERAL(15, 300, 27), // "onGUIDynamismThreadFinished"
QT_MOC_LITERAL(16, 328, 23), // "onAbortedThreadFinished"
QT_MOC_LITERAL(17, 352, 17), // "showWaitingCursor"
QT_MOC_LITERAL(18, 370, 17) // "hideWaitingCursor"

    },
    "GmicQt::GmicProcessor\0previewCommandFailed\0"
    "\0errorMessage\0fullImageProcessingFailed\0"
    "previewImageAvailable\0guiDynamismRunDone\0"
    "fullImageProcessingDone\0noMoreUnfinishedJobs\0"
    "aboutToSendImagesToHost\0cancel\0"
    "detachAllUnfinishedAbortedThreads\0"
    "terminateAllThreads\0onPreviewThreadFinished\0"
    "onApplyThreadFinished\0onGUIDynamismThreadFinished\0"
    "onAbortedThreadFinished\0showWaitingCursor\0"
    "hideWaitingCursor"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__GmicProcessor[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      16,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       7,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   94,    2, 0x06 /* Public */,
       4,    1,   97,    2, 0x06 /* Public */,
       5,    0,  100,    2, 0x06 /* Public */,
       6,    0,  101,    2, 0x06 /* Public */,
       7,    0,  102,    2, 0x06 /* Public */,
       8,    0,  103,    2, 0x06 /* Public */,
       9,    0,  104,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      10,    0,  105,    2, 0x0a /* Public */,
      11,    0,  106,    2, 0x0a /* Public */,
      12,    0,  107,    2, 0x0a /* Public */,
      13,    0,  108,    2, 0x08 /* Private */,
      14,    0,  109,    2, 0x08 /* Private */,
      15,    0,  110,    2, 0x08 /* Private */,
      16,    0,  111,    2, 0x08 /* Private */,
      17,    0,  112,    2, 0x08 /* Private */,
      18,    0,  113,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void GmicQt::GmicProcessor::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<GmicProcessor *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->previewCommandFailed((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->fullImageProcessingFailed((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 2: _t->previewImageAvailable(); break;
        case 3: _t->guiDynamismRunDone(); break;
        case 4: _t->fullImageProcessingDone(); break;
        case 5: _t->noMoreUnfinishedJobs(); break;
        case 6: _t->aboutToSendImagesToHost(); break;
        case 7: _t->cancel(); break;
        case 8: _t->detachAllUnfinishedAbortedThreads(); break;
        case 9: _t->terminateAllThreads(); break;
        case 10: _t->onPreviewThreadFinished(); break;
        case 11: _t->onApplyThreadFinished(); break;
        case 12: _t->onGUIDynamismThreadFinished(); break;
        case 13: _t->onAbortedThreadFinished(); break;
        case 14: _t->showWaitingCursor(); break;
        case 15: _t->hideWaitingCursor(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (GmicProcessor::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::previewCommandFailed)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::fullImageProcessingFailed)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::previewImageAvailable)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::guiDynamismRunDone)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::fullImageProcessingDone)) {
                *result = 4;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::noMoreUnfinishedJobs)) {
                *result = 5;
                return;
            }
        }
        {
            using _t = void (GmicProcessor::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&GmicProcessor::aboutToSendImagesToHost)) {
                *result = 6;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::GmicProcessor::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__GmicProcessor.data,
    qt_meta_data_GmicQt__GmicProcessor,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::GmicProcessor::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::GmicProcessor::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__GmicProcessor.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int GmicQt::GmicProcessor::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 16)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 16;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 16)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 16;
    }
    return _id;
}

// SIGNAL 0
void GmicQt::GmicProcessor::previewCommandFailed(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void GmicQt::GmicProcessor::fullImageProcessingFailed(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void GmicQt::GmicProcessor::previewImageAvailable()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void GmicQt::GmicProcessor::guiDynamismRunDone()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}

// SIGNAL 4
void GmicQt::GmicProcessor::fullImageProcessingDone()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}

// SIGNAL 5
void GmicQt::GmicProcessor::noMoreUnfinishedJobs()
{
    QMetaObject::activate(this, &staticMetaObject, 5, nullptr);
}

// SIGNAL 6
void GmicQt::GmicProcessor::aboutToSendImagesToHost()
{
    QMetaObject::activate(this, &staticMetaObject, 6, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
