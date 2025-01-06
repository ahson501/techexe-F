/********************************************************************************
** Form generated from reading UI file 'zoomlevelselector.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ZOOMLEVELSELECTOR_H
#define UI_ZOOMLEVELSELECTOR_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ZoomLevelSelector
{
public:
    QHBoxLayout *horizontalLayout;
    QLabel *labelWarning;
    QToolButton *tbZoomOut;
    QComboBox *comboBox;
    QToolButton *tbZoomIn;
    QToolButton *tbZoomReset;

    void setupUi(QWidget *ZoomLevelSelector)
    {
        if (ZoomLevelSelector->objectName().isEmpty())
            ZoomLevelSelector->setObjectName(QString::fromUtf8("ZoomLevelSelector"));
        ZoomLevelSelector->resize(170, 39);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(ZoomLevelSelector->sizePolicy().hasHeightForWidth());
        ZoomLevelSelector->setSizePolicy(sizePolicy);
        horizontalLayout = new QHBoxLayout(ZoomLevelSelector);
        horizontalLayout->setSpacing(0);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        labelWarning = new QLabel(ZoomLevelSelector);
        labelWarning->setObjectName(QString::fromUtf8("labelWarning"));
        labelWarning->setPixmap(QPixmap(QString::fromUtf8(":/images/warning.png")));

        horizontalLayout->addWidget(labelWarning);

        tbZoomOut = new QToolButton(ZoomLevelSelector);
        tbZoomOut->setObjectName(QString::fromUtf8("tbZoomOut"));
        QSizePolicy sizePolicy1(QSizePolicy::Fixed, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(tbZoomOut->sizePolicy().hasHeightForWidth());
        tbZoomOut->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(tbZoomOut);

        comboBox = new QComboBox(ZoomLevelSelector);
        comboBox->setObjectName(QString::fromUtf8("comboBox"));
        comboBox->setSizeAdjustPolicy(QComboBox::AdjustToContents);

        horizontalLayout->addWidget(comboBox);

        tbZoomIn = new QToolButton(ZoomLevelSelector);
        tbZoomIn->setObjectName(QString::fromUtf8("tbZoomIn"));
        sizePolicy1.setHeightForWidth(tbZoomIn->sizePolicy().hasHeightForWidth());
        tbZoomIn->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(tbZoomIn);

        tbZoomReset = new QToolButton(ZoomLevelSelector);
        tbZoomReset->setObjectName(QString::fromUtf8("tbZoomReset"));
        sizePolicy1.setHeightForWidth(tbZoomReset->sizePolicy().hasHeightForWidth());
        tbZoomReset->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(tbZoomReset);


        retranslateUi(ZoomLevelSelector);

        QMetaObject::connectSlotsByName(ZoomLevelSelector);
    } // setupUi

    void retranslateUi(QWidget *ZoomLevelSelector)
    {
        ZoomLevelSelector->setWindowTitle(QCoreApplication::translate("ZoomLevelSelector", "Form", nullptr));
        labelWarning->setText(QString());
        tbZoomOut->setText(QString());
        tbZoomIn->setText(QString());
        tbZoomReset->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class ZoomLevelSelector: public Ui_ZoomLevelSelector {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ZOOMLEVELSELECTOR_H
