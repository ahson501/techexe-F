/********************************************************************************
** Form generated from reading UI file 'SearchFieldWidget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SEARCHFIELDWIDGET_H
#define UI_SEARCHFIELDWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_SearchFieldWidget
{
public:
    QHBoxLayout *horizontalLayout_2;

    void setupUi(QWidget *SearchFieldWidget)
    {
        if (SearchFieldWidget->objectName().isEmpty())
            SearchFieldWidget->setObjectName(QString::fromUtf8("SearchFieldWidget"));
        SearchFieldWidget->resize(400, 300);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(SearchFieldWidget->sizePolicy().hasHeightForWidth());
        SearchFieldWidget->setSizePolicy(sizePolicy);
        horizontalLayout_2 = new QHBoxLayout(SearchFieldWidget);
        horizontalLayout_2->setSpacing(2);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);

        retranslateUi(SearchFieldWidget);

        QMetaObject::connectSlotsByName(SearchFieldWidget);
    } // setupUi

    void retranslateUi(QWidget *SearchFieldWidget)
    {
        SearchFieldWidget->setWindowTitle(QCoreApplication::translate("SearchFieldWidget", "Frame", nullptr));
    } // retranslateUi

};

namespace Ui {
    class SearchFieldWidget: public Ui_SearchFieldWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SEARCHFIELDWIDGET_H
