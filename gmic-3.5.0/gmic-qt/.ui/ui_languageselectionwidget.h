/********************************************************************************
** Form generated from reading UI file 'languageselectionwidget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LANGUAGESELECTIONWIDGET_H
#define UI_LANGUAGESELECTIONWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_LanguageSelectionWidget
{
public:
    QVBoxLayout *verticalLayout;
    QLabel *label;
    QComboBox *comboBox;
    QCheckBox *cbTranslateFilters;

    void setupUi(QWidget *LanguageSelectionWidget)
    {
        if (LanguageSelectionWidget->objectName().isEmpty())
            LanguageSelectionWidget->setObjectName(QString::fromUtf8("LanguageSelectionWidget"));
        LanguageSelectionWidget->resize(228, 53);
        verticalLayout = new QVBoxLayout(LanguageSelectionWidget);
        verticalLayout->setSpacing(0);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        label = new QLabel(LanguageSelectionWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setTextFormat(Qt::AutoText);

        verticalLayout->addWidget(label);

        comboBox = new QComboBox(LanguageSelectionWidget);
        comboBox->setObjectName(QString::fromUtf8("comboBox"));

        verticalLayout->addWidget(comboBox);

        cbTranslateFilters = new QCheckBox(LanguageSelectionWidget);
        cbTranslateFilters->setObjectName(QString::fromUtf8("cbTranslateFilters"));

        verticalLayout->addWidget(cbTranslateFilters);


        retranslateUi(LanguageSelectionWidget);

        QMetaObject::connectSlotsByName(LanguageSelectionWidget);
    } // setupUi

    void retranslateUi(QWidget *LanguageSelectionWidget)
    {
        LanguageSelectionWidget->setWindowTitle(QCoreApplication::translate("LanguageSelectionWidget", "Form", nullptr));
        label->setText(QCoreApplication::translate("LanguageSelectionWidget", "<i>(Restart needed)</i>", nullptr));
        cbTranslateFilters->setText(QCoreApplication::translate("LanguageSelectionWidget", "Translate filters (WIP)", nullptr));
    } // retranslateUi

};

namespace Ui {
    class LanguageSelectionWidget: public Ui_LanguageSelectionWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LANGUAGESELECTIONWIDGET_H
