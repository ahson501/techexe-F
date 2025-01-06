/********************************************************************************
** Form generated from reading UI file 'inoutpanel.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_INOUTPANEL_H
#define UI_INOUTPANEL_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_InOutPanel
{
public:
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QLabel *topLabel;
    QToolButton *tbReset;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QGridLayout *gridLayout;
    QLabel *labelInputLayers;
    QComboBox *outputMode;
    QLabel *labelOutputMode;
    QComboBox *inputLayers;
    QWidget *widget;

    void setupUi(QWidget *InOutPanel)
    {
        if (InOutPanel->objectName().isEmpty())
            InOutPanel->setObjectName(QString::fromUtf8("InOutPanel"));
        InOutPanel->resize(463, 290);
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(InOutPanel->sizePolicy().hasHeightForWidth());
        InOutPanel->setSizePolicy(sizePolicy);
        InOutPanel->setWindowTitle(QString::fromUtf8("GroupBox"));
        verticalLayout = new QVBoxLayout(InOutPanel);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        topLabel = new QLabel(InOutPanel);
        topLabel->setObjectName(QString::fromUtf8("topLabel"));

        horizontalLayout->addWidget(topLabel);

        tbReset = new QToolButton(InOutPanel);
        tbReset->setObjectName(QString::fromUtf8("tbReset"));

        horizontalLayout->addWidget(tbReset);


        verticalLayout->addLayout(horizontalLayout);

        scrollArea = new QScrollArea(InOutPanel);
        scrollArea->setObjectName(QString::fromUtf8("scrollArea"));
        sizePolicy.setHeightForWidth(scrollArea->sizePolicy().hasHeightForWidth());
        scrollArea->setSizePolicy(sizePolicy);
        scrollArea->setFrameShape(QFrame::NoFrame);
        scrollArea->setSizeAdjustPolicy(QAbstractScrollArea::AdjustIgnored);
        scrollArea->setWidgetResizable(true);
        scrollArea->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName(QString::fromUtf8("scrollAreaWidgetContents"));
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 463, 142));
        gridLayout = new QGridLayout(scrollAreaWidgetContents);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelInputLayers = new QLabel(scrollAreaWidgetContents);
        labelInputLayers->setObjectName(QString::fromUtf8("labelInputLayers"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(labelInputLayers->sizePolicy().hasHeightForWidth());
        labelInputLayers->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(labelInputLayers, 0, 0, 1, 1);

        outputMode = new QComboBox(scrollAreaWidgetContents);
        outputMode->setObjectName(QString::fromUtf8("outputMode"));
        QSizePolicy sizePolicy2(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(1);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(outputMode->sizePolicy().hasHeightForWidth());
        outputMode->setSizePolicy(sizePolicy2);

        gridLayout->addWidget(outputMode, 1, 1, 1, 1);

        labelOutputMode = new QLabel(scrollAreaWidgetContents);
        labelOutputMode->setObjectName(QString::fromUtf8("labelOutputMode"));
        sizePolicy1.setHeightForWidth(labelOutputMode->sizePolicy().hasHeightForWidth());
        labelOutputMode->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(labelOutputMode, 1, 0, 1, 1);

        inputLayers = new QComboBox(scrollAreaWidgetContents);
        inputLayers->setObjectName(QString::fromUtf8("inputLayers"));
        sizePolicy2.setHeightForWidth(inputLayers->sizePolicy().hasHeightForWidth());
        inputLayers->setSizePolicy(sizePolicy2);

        gridLayout->addWidget(inputLayers, 0, 1, 1, 1);

        widget = new QWidget(scrollAreaWidgetContents);
        widget->setObjectName(QString::fromUtf8("widget"));

        gridLayout->addWidget(widget, 2, 0, 1, 2);

        scrollArea->setWidget(scrollAreaWidgetContents);

        verticalLayout->addWidget(scrollArea);


        retranslateUi(InOutPanel);

        QMetaObject::connectSlotsByName(InOutPanel);
    } // setupUi

    void retranslateUi(QWidget *InOutPanel)
    {
        topLabel->setText(QCoreApplication::translate("InOutPanel", "Input / Output", nullptr));
        tbReset->setText(QCoreApplication::translate("InOutPanel", "...", nullptr));
        labelInputLayers->setText(QCoreApplication::translate("InOutPanel", "Input layers", nullptr));
        labelOutputMode->setText(QCoreApplication::translate("InOutPanel", "Output mode", nullptr));
        (void)InOutPanel;
    } // retranslateUi

};

namespace Ui {
    class InOutPanel: public Ui_InOutPanel {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_INOUTPANEL_H
