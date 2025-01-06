/********************************************************************************
** Form generated from reading UI file 'headlessprogressdialog.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_HEADLESSPROGRESSDIALOG_H
#define UI_HEADLESSPROGRESSDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_HeadlessProgressDialog
{
public:
    QVBoxLayout *verticalLayout;
    QFrame *frame;
    QHBoxLayout *horizontalLayout;
    QLabel *label;
    QProgressBar *progressBar;
    QLabel *info;
    QHBoxLayout *horizontalLayout_2;
    QSpacerItem *horizontalSpacer;
    QPushButton *pbCancel;
    QSpacerItem *horizontalSpacer_2;

    void setupUi(QDialog *HeadlessProgressDialog)
    {
        if (HeadlessProgressDialog->objectName().isEmpty())
            HeadlessProgressDialog->setObjectName(QString::fromUtf8("HeadlessProgressDialog"));
        HeadlessProgressDialog->resize(432, 218);
        verticalLayout = new QVBoxLayout(HeadlessProgressDialog);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        frame = new QFrame(HeadlessProgressDialog);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        horizontalLayout = new QHBoxLayout(frame);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        label = new QLabel(frame);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);


        verticalLayout->addWidget(frame);

        progressBar = new QProgressBar(HeadlessProgressDialog);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setValue(24);

        verticalLayout->addWidget(progressBar);

        info = new QLabel(HeadlessProgressDialog);
        info->setObjectName(QString::fromUtf8("info"));

        verticalLayout->addWidget(info);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        pbCancel = new QPushButton(HeadlessProgressDialog);
        pbCancel->setObjectName(QString::fromUtf8("pbCancel"));

        horizontalLayout_2->addWidget(pbCancel);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);


        verticalLayout->addLayout(horizontalLayout_2);


        retranslateUi(HeadlessProgressDialog);

        QMetaObject::connectSlotsByName(HeadlessProgressDialog);
    } // setupUi

    void retranslateUi(QDialog *HeadlessProgressDialog)
    {
        HeadlessProgressDialog->setWindowTitle(QCoreApplication::translate("HeadlessProgressDialog", "Dialog", nullptr));
        label->setText(QString());
        info->setText(QString());
        pbCancel->setText(QCoreApplication::translate("HeadlessProgressDialog", "Cancel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class HeadlessProgressDialog: public Ui_HeadlessProgressDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_HEADLESSPROGRESSDIALOG_H
