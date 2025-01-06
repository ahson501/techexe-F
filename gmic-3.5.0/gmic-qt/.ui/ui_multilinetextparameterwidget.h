/********************************************************************************
** Form generated from reading UI file 'multilinetextparameterwidget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MULTILINETEXTPARAMETERWIDGET_H
#define UI_MULTILINETEXTPARAMETERWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MultilineTextParameterWidget
{
public:
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QLabel *label;
    QPushButton *pbUpdate;
    QTextEdit *textEdit;

    void setupUi(QWidget *MultilineTextParameterWidget)
    {
        if (MultilineTextParameterWidget->objectName().isEmpty())
            MultilineTextParameterWidget->setObjectName(QString::fromUtf8("MultilineTextParameterWidget"));
        MultilineTextParameterWidget->resize(403, 210);
        verticalLayout = new QVBoxLayout(MultilineTextParameterWidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        label = new QLabel(MultilineTextParameterWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        pbUpdate = new QPushButton(MultilineTextParameterWidget);
        pbUpdate->setObjectName(QString::fromUtf8("pbUpdate"));

        horizontalLayout->addWidget(pbUpdate);


        verticalLayout->addLayout(horizontalLayout);

        textEdit = new QTextEdit(MultilineTextParameterWidget);
        textEdit->setObjectName(QString::fromUtf8("textEdit"));

        verticalLayout->addWidget(textEdit);


        retranslateUi(MultilineTextParameterWidget);

        QMetaObject::connectSlotsByName(MultilineTextParameterWidget);
    } // setupUi

    void retranslateUi(QWidget *MultilineTextParameterWidget)
    {
        MultilineTextParameterWidget->setWindowTitle(QCoreApplication::translate("MultilineTextParameterWidget", "Form", nullptr));
        label->setText(QString());
        pbUpdate->setText(QCoreApplication::translate("MultilineTextParameterWidget", "Update", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MultilineTextParameterWidget: public Ui_MultilineTextParameterWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MULTILINETEXTPARAMETERWIDGET_H
