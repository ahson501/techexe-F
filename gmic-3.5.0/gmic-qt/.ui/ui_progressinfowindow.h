/********************************************************************************
** Form generated from reading UI file 'progressinfowindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PROGRESSINFOWINDOW_H
#define UI_PROGRESSINFOWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ProgressInfoWindow
{
public:
    QWidget *centralwidget;
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
    QStatusBar *statusbar;

    void setupUi(QMainWindow *ProgressInfoWindow)
    {
        if (ProgressInfoWindow->objectName().isEmpty())
            ProgressInfoWindow->setObjectName(QString::fromUtf8("ProgressInfoWindow"));
        ProgressInfoWindow->resize(438, 166);
        centralwidget = new QWidget(ProgressInfoWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        frame = new QFrame(centralwidget);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        horizontalLayout = new QHBoxLayout(frame);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        label = new QLabel(frame);
        label->setObjectName(QString::fromUtf8("label"));
        label->setAlignment(Qt::AlignCenter);

        horizontalLayout->addWidget(label);


        verticalLayout->addWidget(frame);

        progressBar = new QProgressBar(centralwidget);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setValue(24);

        verticalLayout->addWidget(progressBar);

        info = new QLabel(centralwidget);
        info->setObjectName(QString::fromUtf8("info"));

        verticalLayout->addWidget(info);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        pbCancel = new QPushButton(centralwidget);
        pbCancel->setObjectName(QString::fromUtf8("pbCancel"));

        horizontalLayout_2->addWidget(pbCancel);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);


        verticalLayout->addLayout(horizontalLayout_2);

        ProgressInfoWindow->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(ProgressInfoWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        ProgressInfoWindow->setStatusBar(statusbar);

        retranslateUi(ProgressInfoWindow);

        QMetaObject::connectSlotsByName(ProgressInfoWindow);
    } // setupUi

    void retranslateUi(QMainWindow *ProgressInfoWindow)
    {
        ProgressInfoWindow->setWindowTitle(QCoreApplication::translate("ProgressInfoWindow", "MainWindow", nullptr));
        label->setText(QCoreApplication::translate("ProgressInfoWindow", "TextLabel", nullptr));
        info->setText(QCoreApplication::translate("ProgressInfoWindow", "TextLabel", nullptr));
        pbCancel->setText(QCoreApplication::translate("ProgressInfoWindow", "Cancel", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ProgressInfoWindow: public Ui_ProgressInfoWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PROGRESSINFOWINDOW_H
