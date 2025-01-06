/********************************************************************************
** Form generated from reading UI file 'filtersview.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FILTERSVIEW_H
#define UI_FILTERSVIEW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "FilterSelector/FiltersView/TreeView.h"

QT_BEGIN_NAMESPACE

class Ui_FiltersView
{
public:
    QVBoxLayout *verticalLayout;
    GmicQt::TreeView *treeView;

    void setupUi(QWidget *FiltersView)
    {
        if (FiltersView->objectName().isEmpty())
            FiltersView->setObjectName(QString::fromUtf8("FiltersView"));
        FiltersView->resize(428, 458);
        verticalLayout = new QVBoxLayout(FiltersView);
        verticalLayout->setSpacing(0);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        treeView = new GmicQt::TreeView(FiltersView);
        treeView->setObjectName(QString::fromUtf8("treeView"));

        verticalLayout->addWidget(treeView);


        retranslateUi(FiltersView);

        QMetaObject::connectSlotsByName(FiltersView);
    } // setupUi

    void retranslateUi(QWidget *FiltersView)
    {
        FiltersView->setWindowTitle(QCoreApplication::translate("FiltersView", "Form", nullptr));
    } // retranslateUi

};

namespace Ui {
    class FiltersView: public Ui_FiltersView {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FILTERSVIEW_H
