/****************************************************************************
** Meta object code from reading C++ file 'FiltersPresenter.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/FilterSelector/FiltersPresenter.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'FiltersPresenter.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__FiltersPresenter_t {
    QByteArrayData data[17];
    char stringdata0[240];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__FiltersPresenter_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__FiltersPresenter_t qt_meta_stringdata_GmicQt__FiltersPresenter = {
    {
QT_MOC_LITERAL(0, 0, 24), // "GmicQt::FiltersPresenter"
QT_MOC_LITERAL(1, 25, 22), // "filterSelectionChanged"
QT_MOC_LITERAL(2, 48, 0), // ""
QT_MOC_LITERAL(3, 49, 21), // "faveAdditionRequested"
QT_MOC_LITERAL(4, 71, 15), // "faveNameChanged"
QT_MOC_LITERAL(5, 87, 19), // "setVisibleTagColors"
QT_MOC_LITERAL(6, 107, 5), // "color"
QT_MOC_LITERAL(7, 113, 18), // "removeSelectedFave"
QT_MOC_LITERAL(8, 132, 20), // "editSelectedFaveName"
QT_MOC_LITERAL(9, 153, 13), // "onFaveRenamed"
QT_MOC_LITERAL(10, 167, 4), // "hash"
QT_MOC_LITERAL(11, 172, 4), // "name"
QT_MOC_LITERAL(12, 177, 19), // "toggleSelectionMode"
QT_MOC_LITERAL(13, 197, 2), // "on"
QT_MOC_LITERAL(14, 200, 15), // "onFilterChanged"
QT_MOC_LITERAL(15, 216, 10), // "removeFave"
QT_MOC_LITERAL(16, 227, 12) // "onTagToggled"

    },
    "GmicQt::FiltersPresenter\0"
    "filterSelectionChanged\0\0faveAdditionRequested\0"
    "faveNameChanged\0setVisibleTagColors\0"
    "color\0removeSelectedFave\0editSelectedFaveName\0"
    "onFaveRenamed\0hash\0name\0toggleSelectionMode\0"
    "on\0onFilterChanged\0removeFave\0"
    "onTagToggled"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__FiltersPresenter[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      11,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   69,    2, 0x06 /* Public */,
       3,    1,   70,    2, 0x06 /* Public */,
       4,    1,   73,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    1,   76,    2, 0x0a /* Public */,
       7,    0,   79,    2, 0x0a /* Public */,
       8,    0,   80,    2, 0x0a /* Public */,
       9,    2,   81,    2, 0x0a /* Public */,
      12,    1,   86,    2, 0x0a /* Public */,
      14,    1,   89,    2, 0x08 /* Private */,
      15,    1,   92,    2, 0x08 /* Private */,
      16,    1,   95,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    2,
    QMetaType::Void, QMetaType::QString,    2,

 // slots: parameters
    QMetaType::Void, QMetaType::UInt,    6,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString, QMetaType::QString,   10,   11,
    QMetaType::Void, QMetaType::Bool,   13,
    QMetaType::Void, QMetaType::QString,   10,
    QMetaType::Void, QMetaType::QString,   10,
    QMetaType::Void, QMetaType::Int,    6,

       0        // eod
};

void GmicQt::FiltersPresenter::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<FiltersPresenter *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->filterSelectionChanged(); break;
        case 1: _t->faveAdditionRequested((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 2: _t->faveNameChanged((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 3: _t->setVisibleTagColors((*reinterpret_cast< uint(*)>(_a[1]))); break;
        case 4: _t->removeSelectedFave(); break;
        case 5: _t->editSelectedFaveName(); break;
        case 6: _t->onFaveRenamed((*reinterpret_cast< const QString(*)>(_a[1])),(*reinterpret_cast< const QString(*)>(_a[2]))); break;
        case 7: _t->toggleSelectionMode((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 8: _t->onFilterChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 9: _t->removeFave((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 10: _t->onTagToggled((*reinterpret_cast< int(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (FiltersPresenter::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersPresenter::filterSelectionChanged)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (FiltersPresenter::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersPresenter::faveAdditionRequested)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (FiltersPresenter::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersPresenter::faveNameChanged)) {
                *result = 2;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::FiltersPresenter::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__FiltersPresenter.data,
    qt_meta_data_GmicQt__FiltersPresenter,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::FiltersPresenter::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::FiltersPresenter::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__FiltersPresenter.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int GmicQt::FiltersPresenter::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 11)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 11;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 11)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 11;
    }
    return _id;
}

// SIGNAL 0
void GmicQt::FiltersPresenter::filterSelectionChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void GmicQt::FiltersPresenter::faveAdditionRequested(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void GmicQt::FiltersPresenter::faveNameChanged(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
