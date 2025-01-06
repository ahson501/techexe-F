/********************************************************************************
** Form generated from reading UI file 'progressinfowidget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PROGRESSINFOWIDGET_H
#define UI_PROGRESSINFOWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ProgressInfoWidget
{
public:
    QHBoxLayout *horizontalLayout;
    QProgressBar *progressBar;
    QToolButton *tbCancel;
    QLabel *label;

    void setupUi(QWidget *ProgressInfoWidget)
    {
        if (ProgressInfoWidget->objectName().isEmpty())
            ProgressInfoWidget->setObjectName(QString::fromUtf8("ProgressInfoWidget"));
        ProgressInfoWidget->resize(296, 25);
        horizontalLayout = new QHBoxLayout(ProgressInfoWidget);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        progressBar = new QProgressBar(ProgressInfoWidget);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setValue(24);
        progressBar->setInvertedAppearance(false);

        horizontalLayout->addWidget(progressBar);

        tbCancel = new QToolButton(ProgressInfoWidget);
        tbCancel->setObjectName(QString::fromUtf8("tbCancel"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(tbCancel->sizePolicy().hasHeightForWidth());
        tbCancel->setSizePolicy(sizePolicy);

        horizontalLayout->addWidget(tbCancel);

        label = new QLabel(ProgressInfoWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);


        retranslateUi(ProgressInfoWidget);

        QMetaObject::connectSlotsByName(ProgressInfoWidget);
    } // setupUi

    void retranslateUi(QWidget *ProgressInfoWidget)
    {
        ProgressInfoWidget->setWindowTitle(QCoreApplication::translate("ProgressInfoWidget", "Form", nullptr));
        tbCancel->setText(QCoreApplication::translate("ProgressInfoWidget", "Abort", nullptr));
        label->setText(QCoreApplication::translate("ProgressInfoWidget", "TextLabel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ProgressInfoWidget: public Ui_ProgressInfoWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PROGRESSINFOWIDGET_H
