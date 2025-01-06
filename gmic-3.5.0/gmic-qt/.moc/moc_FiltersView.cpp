/****************************************************************************
** Meta object code from reading C++ file 'FiltersView.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/FilterSelector/FiltersView/FiltersView.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'FiltersView.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_GmicQt__FiltersView_t {
    QByteArrayData data[29];
    char stringdata0[412];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GmicQt__FiltersView_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GmicQt__FiltersView_t qt_meta_stringdata_GmicQt__FiltersView = {
    {
QT_MOC_LITERAL(0, 0, 19), // "GmicQt::FiltersView"
QT_MOC_LITERAL(1, 20, 14), // "filterSelected"
QT_MOC_LITERAL(2, 35, 0), // ""
QT_MOC_LITERAL(3, 36, 4), // "hash"
QT_MOC_LITERAL(4, 41, 11), // "faveRenamed"
QT_MOC_LITERAL(5, 53, 7), // "newName"
QT_MOC_LITERAL(6, 61, 20), // "faveRemovalRequested"
QT_MOC_LITERAL(7, 82, 21), // "faveAdditionRequested"
QT_MOC_LITERAL(8, 104, 10), // "tagToggled"
QT_MOC_LITERAL(9, 115, 6), // "iColor"
QT_MOC_LITERAL(10, 122, 20), // "editSelectedFaveName"
QT_MOC_LITERAL(11, 143, 9), // "expandAll"
QT_MOC_LITERAL(12, 153, 11), // "collapseAll"
QT_MOC_LITERAL(13, 165, 16), // "expandFaveFolder"
QT_MOC_LITERAL(14, 182, 19), // "onCustomContextMenu"
QT_MOC_LITERAL(15, 202, 5), // "point"
QT_MOC_LITERAL(16, 208, 20), // "onRenameFaveFinished"
QT_MOC_LITERAL(17, 229, 8), // "QWidget*"
QT_MOC_LITERAL(18, 238, 6), // "editor"
QT_MOC_LITERAL(19, 245, 31), // "onReturnKeyPressedInFiltersTree"
QT_MOC_LITERAL(20, 277, 13), // "onItemClicked"
QT_MOC_LITERAL(21, 291, 11), // "QModelIndex"
QT_MOC_LITERAL(22, 303, 5), // "index"
QT_MOC_LITERAL(23, 309, 13), // "onItemChanged"
QT_MOC_LITERAL(24, 323, 14), // "QStandardItem*"
QT_MOC_LITERAL(25, 338, 4), // "item"
QT_MOC_LITERAL(26, 343, 23), // "onContextMenuRemoveFave"
QT_MOC_LITERAL(27, 367, 23), // "onContextMenuRenameFave"
QT_MOC_LITERAL(28, 391, 20) // "onContextMenuAddFave"

    },
    "GmicQt::FiltersView\0filterSelected\0\0"
    "hash\0faveRenamed\0newName\0faveRemovalRequested\0"
    "faveAdditionRequested\0tagToggled\0"
    "iColor\0editSelectedFaveName\0expandAll\0"
    "collapseAll\0expandFaveFolder\0"
    "onCustomContextMenu\0point\0"
    "onRenameFaveFinished\0QWidget*\0editor\0"
    "onReturnKeyPressedInFiltersTree\0"
    "onItemClicked\0QModelIndex\0index\0"
    "onItemChanged\0QStandardItem*\0item\0"
    "onContextMenuRemoveFave\0onContextMenuRenameFave\0"
    "onContextMenuAddFave"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GmicQt__FiltersView[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      17,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       5,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   99,    2, 0x06 /* Public */,
       4,    2,  102,    2, 0x06 /* Public */,
       6,    1,  107,    2, 0x06 /* Public */,
       7,    1,  110,    2, 0x06 /* Public */,
       8,    1,  113,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      10,    0,  116,    2, 0x0a /* Public */,
      11,    0,  117,    2, 0x0a /* Public */,
      12,    0,  118,    2, 0x0a /* Public */,
      13,    0,  119,    2, 0x0a /* Public */,
      14,    1,  120,    2, 0x0a /* Public */,
      16,    1,  123,    2, 0x08 /* Private */,
      19,    0,  126,    2, 0x08 /* Private */,
      20,    1,  127,    2, 0x08 /* Private */,
      23,    1,  130,    2, 0x08 /* Private */,
      26,    0,  133,    2, 0x08 /* Private */,
      27,    0,  134,    2, 0x08 /* Private */,
      28,    0,  135,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QString, QMetaType::QString,    3,    5,
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::Int,    9,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QPoint,   15,
    QMetaType::Void, 0x80000000 | 17,   18,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 21,   22,
    QMetaType::Void, 0x80000000 | 24,   25,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void GmicQt::FiltersView::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<FiltersView *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->filterSelected((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->faveRenamed((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< QString(*)>(_a[2]))); break;
        case 2: _t->faveRemovalRequested((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 3: _t->faveAdditionRequested((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 4: _t->tagToggled((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->editSelectedFaveName(); break;
        case 6: _t->expandAll(); break;
        case 7: _t->collapseAll(); break;
        case 8: _t->expandFaveFolder(); break;
        case 9: _t->onCustomContextMenu((*reinterpret_cast< const QPoint(*)>(_a[1]))); break;
        case 10: _t->onRenameFaveFinished((*reinterpret_cast< QWidget*(*)>(_a[1]))); break;
        case 11: _t->onReturnKeyPressedInFiltersTree(); break;
        case 12: _t->onItemClicked((*reinterpret_cast< QModelIndex(*)>(_a[1]))); break;
        case 13: _t->onItemChanged((*reinterpret_cast< QStandardItem*(*)>(_a[1]))); break;
        case 14: _t->onContextMenuRemoveFave(); break;
        case 15: _t->onContextMenuRenameFave(); break;
        case 16: _t->onContextMenuAddFave(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 10:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QWidget* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (FiltersView::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersView::filterSelected)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (FiltersView::*)(QString , QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersView::faveRenamed)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (FiltersView::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersView::faveRemovalRequested)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (FiltersView::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersView::faveAdditionRequested)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (FiltersView::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FiltersView::tagToggled)) {
                *result = 4;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject GmicQt::FiltersView::staticMetaObject = { {
    QMetaObject::SuperData::link<QWidget::staticMetaObject>(),
    qt_meta_stringdata_GmicQt__FiltersView.data,
    qt_meta_data_GmicQt__FiltersView,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *GmicQt::FiltersView::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GmicQt::FiltersView::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_GmicQt__FiltersView.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int GmicQt::FiltersView::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 17)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 17;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 17)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 17;
    }
    return _id;
}

// SIGNAL 0
void GmicQt::FiltersView::filterSelected(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void GmicQt::FiltersView::faveRenamed(QString _t1, QString _t2)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void GmicQt::FiltersView::faveRemovalRequested(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void GmicQt::FiltersView::faveAdditionRequested(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void GmicQt::FiltersView::tagToggled(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 4, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
