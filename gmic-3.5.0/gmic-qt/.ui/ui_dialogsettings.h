/********************************************************************************
** Form generated from reading UI file 'dialogsettings.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DIALOGSETTINGS_H
#define UI_DIALOGSETTINGS_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "ClickableLabel.h"
#include "SourcesWidget.h"
#include "Widgets/LanguageSelectionWidget.h"

QT_BEGIN_NAMESPACE

class Ui_DialogSettings
{
public:
    QVBoxLayout *verticalLayout_2;
    QTabWidget *tabWidget;
    QWidget *interface;
    QGridLayout *gridLayout;
    QGroupBox *groupBox_2;
    QGridLayout *gridLayout_2;
    QCheckBox *cbShowLogos;
    QVBoxLayout *verticalLayout;
    GmicQt::ClickableLabel *labelPreviewLeft;
    QRadioButton *rbLeftPreview;
    QVBoxLayout *verticalLayout_4;
    GmicQt::ClickableLabel *labelPreviewRight;
    QRadioButton *rbRightPreview;
    QFrame *line;
    QGroupBox *groupBox_3;
    QVBoxLayout *verticalLayout_3;
    QRadioButton *rbDefaultTheme;
    QRadioButton *rbDarkTheme;
    QLabel *label;
    QGroupBox *groupBox_5;
    QVBoxLayout *verticalLayout_7;
    GmicQt::LanguageSelectionWidget *languageSelector;
    QHBoxLayout *horizontalLayout_4;
    QGroupBox *groupBox_6;
    QGridLayout *gridLayout_4;
    QLabel *label_2;
    QSpinBox *sbPreviewTimeout;
    QCheckBox *cbPreviewZoom;
    QLabel *label_3;
    QGroupBox *groupBox_4;
    QVBoxLayout *verticalLayout_6;
    QCheckBox *cbNativeColorDialogs;
    QCheckBox *cbNativeFileDialogs;
    QCheckBox *cbHighDPI;
    QLabel *labelHighDPI;
    GmicQt::SourcesWidget *sources;
    QWidget *other;
    QGridLayout *gridLayout_3;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout_2;
    QComboBox *cbUpdatePeriodicity;
    QPushButton *pbUpdate;
    QSpacerItem *horizontalSpacer_2;
    QGroupBox *groupBox_7;
    QVBoxLayout *verticalLayout_8;
    QComboBox *outputMessages;
    QCheckBox *cbNotifyFailedUpdate;
    QSpacerItem *verticalSpacer;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QPushButton *pbOk;

    void setupUi(QDialog *DialogSettings)
    {
        if (DialogSettings->objectName().isEmpty())
            DialogSettings->setObjectName(QString::fromUtf8("DialogSettings"));
        DialogSettings->resize(553, 496);
        verticalLayout_2 = new QVBoxLayout(DialogSettings);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        tabWidget = new QTabWidget(DialogSettings);
        tabWidget->setObjectName(QString::fromUtf8("tabWidget"));
        interface = new QWidget();
        interface->setObjectName(QString::fromUtf8("interface"));
        gridLayout = new QGridLayout(interface);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        groupBox_2 = new QGroupBox(interface);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        gridLayout_2 = new QGridLayout(groupBox_2);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        cbShowLogos = new QCheckBox(groupBox_2);
        cbShowLogos->setObjectName(QString::fromUtf8("cbShowLogos"));

        gridLayout_2->addWidget(cbShowLogos, 2, 0, 1, 2);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        labelPreviewLeft = new GmicQt::ClickableLabel(groupBox_2);
        labelPreviewLeft->setObjectName(QString::fromUtf8("labelPreviewLeft"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(labelPreviewLeft->sizePolicy().hasHeightForWidth());
        labelPreviewLeft->setSizePolicy(sizePolicy);
        labelPreviewLeft->setPixmap(QPixmap(QString::fromUtf8(":/images/preview_left.png")));
        labelPreviewLeft->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        verticalLayout->addWidget(labelPreviewLeft);

        rbLeftPreview = new QRadioButton(groupBox_2);
        rbLeftPreview->setObjectName(QString::fromUtf8("rbLeftPreview"));

        verticalLayout->addWidget(rbLeftPreview);


        gridLayout_2->addLayout(verticalLayout, 0, 0, 1, 1);

        verticalLayout_4 = new QVBoxLayout();
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        labelPreviewRight = new GmicQt::ClickableLabel(groupBox_2);
        labelPreviewRight->setObjectName(QString::fromUtf8("labelPreviewRight"));
        sizePolicy.setHeightForWidth(labelPreviewRight->sizePolicy().hasHeightForWidth());
        labelPreviewRight->setSizePolicy(sizePolicy);
        labelPreviewRight->setPixmap(QPixmap(QString::fromUtf8(":/images/preview_right.png")));
        labelPreviewRight->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        verticalLayout_4->addWidget(labelPreviewRight);

        rbRightPreview = new QRadioButton(groupBox_2);
        rbRightPreview->setObjectName(QString::fromUtf8("rbRightPreview"));

        verticalLayout_4->addWidget(rbRightPreview);


        gridLayout_2->addLayout(verticalLayout_4, 0, 1, 1, 1);

        line = new QFrame(groupBox_2);
        line->setObjectName(QString::fromUtf8("line"));
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);

        gridLayout_2->addWidget(line, 1, 0, 1, 2);


        gridLayout->addWidget(groupBox_2, 0, 0, 2, 1);

        groupBox_3 = new QGroupBox(interface);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        verticalLayout_3 = new QVBoxLayout(groupBox_3);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        rbDefaultTheme = new QRadioButton(groupBox_3);
        rbDefaultTheme->setObjectName(QString::fromUtf8("rbDefaultTheme"));

        verticalLayout_3->addWidget(rbDefaultTheme);

        rbDarkTheme = new QRadioButton(groupBox_3);
        rbDarkTheme->setObjectName(QString::fromUtf8("rbDarkTheme"));

        verticalLayout_3->addWidget(rbDarkTheme);

        label = new QLabel(groupBox_3);
        label->setObjectName(QString::fromUtf8("label"));
        sizePolicy.setHeightForWidth(label->sizePolicy().hasHeightForWidth());
        label->setSizePolicy(sizePolicy);

        verticalLayout_3->addWidget(label);


        gridLayout->addWidget(groupBox_3, 0, 1, 1, 1);

        groupBox_5 = new QGroupBox(interface);
        groupBox_5->setObjectName(QString::fromUtf8("groupBox_5"));
        verticalLayout_7 = new QVBoxLayout(groupBox_5);
        verticalLayout_7->setObjectName(QString::fromUtf8("verticalLayout_7"));
        languageSelector = new GmicQt::LanguageSelectionWidget(groupBox_5);
        languageSelector->setObjectName(QString::fromUtf8("languageSelector"));

        verticalLayout_7->addWidget(languageSelector);


        gridLayout->addWidget(groupBox_5, 1, 1, 1, 1);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        groupBox_6 = new QGroupBox(interface);
        groupBox_6->setObjectName(QString::fromUtf8("groupBox_6"));
        gridLayout_4 = new QGridLayout(groupBox_6);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        label_2 = new QLabel(groupBox_6);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout_4->addWidget(label_2, 0, 0, 1, 1);

        sbPreviewTimeout = new QSpinBox(groupBox_6);
        sbPreviewTimeout->setObjectName(QString::fromUtf8("sbPreviewTimeout"));

        gridLayout_4->addWidget(sbPreviewTimeout, 0, 1, 1, 1);

        cbPreviewZoom = new QCheckBox(groupBox_6);
        cbPreviewZoom->setObjectName(QString::fromUtf8("cbPreviewZoom"));

        gridLayout_4->addWidget(cbPreviewZoom, 1, 0, 1, 2);

        label_3 = new QLabel(groupBox_6);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        gridLayout_4->addWidget(label_3, 2, 0, 1, 2);


        horizontalLayout_4->addWidget(groupBox_6);

        groupBox_4 = new QGroupBox(interface);
        groupBox_4->setObjectName(QString::fromUtf8("groupBox_4"));
        verticalLayout_6 = new QVBoxLayout(groupBox_4);
        verticalLayout_6->setObjectName(QString::fromUtf8("verticalLayout_6"));
        cbNativeColorDialogs = new QCheckBox(groupBox_4);
        cbNativeColorDialogs->setObjectName(QString::fromUtf8("cbNativeColorDialogs"));

        verticalLayout_6->addWidget(cbNativeColorDialogs);

        cbNativeFileDialogs = new QCheckBox(groupBox_4);
        cbNativeFileDialogs->setObjectName(QString::fromUtf8("cbNativeFileDialogs"));

        verticalLayout_6->addWidget(cbNativeFileDialogs);

        cbHighDPI = new QCheckBox(groupBox_4);
        cbHighDPI->setObjectName(QString::fromUtf8("cbHighDPI"));

        verticalLayout_6->addWidget(cbHighDPI);

        labelHighDPI = new QLabel(groupBox_4);
        labelHighDPI->setObjectName(QString::fromUtf8("labelHighDPI"));
        labelHighDPI->setAlignment(Qt::AlignRight|Qt::AlignTop|Qt::AlignTrailing);

        verticalLayout_6->addWidget(labelHighDPI);


        horizontalLayout_4->addWidget(groupBox_4);


        gridLayout->addLayout(horizontalLayout_4, 2, 0, 1, 2);

        tabWidget->addTab(interface, QString());
        sources = new GmicQt::SourcesWidget();
        sources->setObjectName(QString::fromUtf8("sources"));
        tabWidget->addTab(sources, QString());
        other = new QWidget();
        other->setObjectName(QString::fromUtf8("other"));
        gridLayout_3 = new QGridLayout(other);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        groupBox = new QGroupBox(other);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        horizontalLayout_2 = new QHBoxLayout(groupBox);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        cbUpdatePeriodicity = new QComboBox(groupBox);
        cbUpdatePeriodicity->setObjectName(QString::fromUtf8("cbUpdatePeriodicity"));

        horizontalLayout_2->addWidget(cbUpdatePeriodicity);

        pbUpdate = new QPushButton(groupBox);
        pbUpdate->setObjectName(QString::fromUtf8("pbUpdate"));

        horizontalLayout_2->addWidget(pbUpdate);


        gridLayout_3->addWidget(groupBox, 0, 0, 1, 1);

        horizontalSpacer_2 = new QSpacerItem(227, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_2, 0, 1, 1, 1);

        groupBox_7 = new QGroupBox(other);
        groupBox_7->setObjectName(QString::fromUtf8("groupBox_7"));
        verticalLayout_8 = new QVBoxLayout(groupBox_7);
        verticalLayout_8->setObjectName(QString::fromUtf8("verticalLayout_8"));
        outputMessages = new QComboBox(groupBox_7);
        outputMessages->setObjectName(QString::fromUtf8("outputMessages"));

        verticalLayout_8->addWidget(outputMessages);

        cbNotifyFailedUpdate = new QCheckBox(groupBox_7);
        cbNotifyFailedUpdate->setObjectName(QString::fromUtf8("cbNotifyFailedUpdate"));

        verticalLayout_8->addWidget(cbNotifyFailedUpdate);


        gridLayout_3->addWidget(groupBox_7, 1, 0, 1, 1);

        verticalSpacer = new QSpacerItem(20, 122, QSizePolicy::Minimum, QSizePolicy::Expanding);

        gridLayout_3->addItem(verticalSpacer, 2, 0, 1, 1);

        tabWidget->addTab(other, QString());

        verticalLayout_2->addWidget(tabWidget);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        pbOk = new QPushButton(DialogSettings);
        pbOk->setObjectName(QString::fromUtf8("pbOk"));

        horizontalLayout->addWidget(pbOk);


        verticalLayout_2->addLayout(horizontalLayout);


        retranslateUi(DialogSettings);

        tabWidget->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(DialogSettings);
    } // setupUi

    void retranslateUi(QDialog *DialogSettings)
    {
        DialogSettings->setWindowTitle(QCoreApplication::translate("DialogSettings", "Dialog", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("DialogSettings", "Layout", nullptr));
        cbShowLogos->setText(QCoreApplication::translate("DialogSettings", "Show institution logos", nullptr));
        labelPreviewLeft->setText(QString());
        rbLeftPreview->setText(QCoreApplication::translate("DialogSettings", "Preview on the &left", nullptr));
        labelPreviewRight->setText(QString());
        rbRightPreview->setText(QCoreApplication::translate("DialogSettings", "Pre&view on right side", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("DialogSettings", "Theme", nullptr));
        rbDefaultTheme->setText(QCoreApplication::translate("DialogSettings", "&Default", nullptr));
        rbDarkTheme->setText(QCoreApplication::translate("DialogSettings", "Dar&k", nullptr));
        label->setText(QCoreApplication::translate("DialogSettings", "<i>(Restart needed)</I>", nullptr));
        groupBox_5->setTitle(QCoreApplication::translate("DialogSettings", "Language", nullptr));
        groupBox_6->setTitle(QCoreApplication::translate("DialogSettings", "Preview", nullptr));
        label_2->setText(QCoreApplication::translate("DialogSettings", "Timeout (seconds)", nullptr));
        cbPreviewZoom->setText(QCoreApplication::translate("DialogSettings", "Always enable preview zooming", nullptr));
        label_3->setText(QCoreApplication::translate("DialogSettings", "<html><head/><body><p><span style=\" font-style:italic;\">(Warning: preview may be inaccurate<br/>if checked.)</span></p></body></html>", nullptr));
        groupBox_4->setTitle(QCoreApplication::translate("DialogSettings", "Misc", nullptr));
        cbNativeColorDialogs->setText(QCoreApplication::translate("DialogSettings", "&Use native color dialog", nullptr));
        cbNativeFileDialogs->setText(QCoreApplication::translate("DialogSettings", "Use native file dialog", nullptr));
        cbHighDPI->setText(QCoreApplication::translate("DialogSettings", "&Enable High-DPI support", nullptr));
        labelHighDPI->setText(QCoreApplication::translate("DialogSettings", "<i>(Restart needed)</i>", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(interface), QCoreApplication::translate("DialogSettings", "Interface", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(sources), QCoreApplication::translate("DialogSettings", "Filter sources", nullptr));
        groupBox->setTitle(QCoreApplication::translate("DialogSettings", "Internet updates", nullptr));
        pbUpdate->setText(QCoreApplication::translate("DialogSettings", "Update now", nullptr));
        groupBox_7->setTitle(QCoreApplication::translate("DialogSettings", "Output messages", nullptr));
        cbNotifyFailedUpdate->setText(QCoreApplication::translate("DialogSettings", "Notify when scheduled update fails", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(other), QCoreApplication::translate("DialogSettings", "Other", nullptr));
        pbOk->setText(QCoreApplication::translate("DialogSettings", "&Ok", nullptr));
    } // retranslateUi

};

namespace Ui {
    class DialogSettings: public Ui_DialogSettings {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DIALOGSETTINGS_H
