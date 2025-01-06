/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "FilterParameters/FilterParametersWidget.h"
#include "FilterSelector/FiltersView/FiltersView.h"
#include "Widgets/InOutPanel.h"
#include "Widgets/PreviewWidget.h"
#include "Widgets/ProgressInfoWidget.h"
#include "Widgets/SearchFieldWidget.h"
#include "Widgets/ZoomLevelSelector.h"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout_3;
    QSplitter *splitter;
    QFrame *filtersFrame;
    QVBoxLayout *verticalLayout_2;
    GmicQt::SearchFieldWidget *searchField;
    GmicQt::FiltersView *filtersView;
    QWidget *widget_2;
    QHBoxLayout *horizontalLayout_8;
    QToolButton *tbAddFave;
    QToolButton *tbRemoveFave;
    QToolButton *tbRenameFave;
    QSpacerItem *horizontalSpacer;
    QToolButton *tbTags;
    QToolButton *tbSelectionMode;
    QToolButton *tbExpandCollapse;
    QWidget *widget;
    QHBoxLayout *horizontalLayout_7;
    QToolButton *tbUpdateFilters;
    QCheckBox *cbInternetUpdate;
    QFrame *parametersPanel;
    QVBoxLayout *verticalLayout_5;
    QSplitter *verticalSplitter;
    QWidget *vSplitterTopWidget;
    QVBoxLayout *verticalLayout_4;
    QHBoxLayout *horizontalLayout_6;
    QLabel *filterName;
    QToolButton *tbCopyCommand;
    QToolButton *tbRandomizeParameters;
    QToolButton *tbResetParameters;
    QScrollArea *scrollAreaParameters;
    QWidget *scrollAreaWidgetContents_2;
    QVBoxLayout *verticalLayout_6;
    GmicQt::FilterParametersWidget *filterParams;
    QSpacerItem *verticalSpacer;
    QFrame *vSplitterLine;
    GmicQt::InOutPanel *inOutSelector;
    QWidget *previewPanel;
    QVBoxLayout *verticalLayout;
    QFrame *previewFrame;
    QVBoxLayout *verticalLayout_7;
    GmicQt::PreviewWidget *previewWidget;
    QHBoxLayout *horizontalLayout_2;
    QCheckBox *cbPreview;
    QComboBox *cbPreviewType;
    QSpacerItem *horizontalSpacer_2;
    GmicQt::ZoomLevelSelector *zoomLevelSelector;
    QWidget *belowPreviewWidget;
    QHBoxLayout *horizontalLayout_5;
    QWidget *belowPreviewPadding;
    QLabel *logosLabel;
    QHBoxLayout *horizontalLayout;
    QPushButton *pbSettings;
    GmicQt::ProgressInfoWidget *progressInfoWidget;
    QLabel *messageLabel;
    QLabel *rightMessageLabel;
    QPushButton *pbFullscreen;
    QPushButton *pbClose;
    QPushButton *pbCancel;
    QPushButton *pbApply;
    QPushButton *pbOk;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1143, 639);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout_3 = new QVBoxLayout(centralwidget);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        splitter = new QSplitter(centralwidget);
        splitter->setObjectName(QString::fromUtf8("splitter"));
        splitter->setOrientation(Qt::Orientation::Horizontal);
        filtersFrame = new QFrame(splitter);
        filtersFrame->setObjectName(QString::fromUtf8("filtersFrame"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(filtersFrame->sizePolicy().hasHeightForWidth());
        filtersFrame->setSizePolicy(sizePolicy);
        filtersFrame->setFrameShape(QFrame::Shape::NoFrame);
        filtersFrame->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_2 = new QVBoxLayout(filtersFrame);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout_2->setContentsMargins(0, -1, 0, -1);
        searchField = new GmicQt::SearchFieldWidget(filtersFrame);
        searchField->setObjectName(QString::fromUtf8("searchField"));
        searchField->setFocusPolicy(Qt::FocusPolicy::StrongFocus);

        verticalLayout_2->addWidget(searchField);

        filtersView = new GmicQt::FiltersView(filtersFrame);
        filtersView->setObjectName(QString::fromUtf8("filtersView"));

        verticalLayout_2->addWidget(filtersView);

        widget_2 = new QWidget(filtersFrame);
        widget_2->setObjectName(QString::fromUtf8("widget_2"));
        horizontalLayout_8 = new QHBoxLayout(widget_2);
        horizontalLayout_8->setObjectName(QString::fromUtf8("horizontalLayout_8"));
        horizontalLayout_8->setContentsMargins(-1, 0, -1, 0);
        tbAddFave = new QToolButton(widget_2);
        tbAddFave->setObjectName(QString::fromUtf8("tbAddFave"));
        QSizePolicy sizePolicy1(QSizePolicy::Fixed, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(tbAddFave->sizePolicy().hasHeightForWidth());
        tbAddFave->setSizePolicy(sizePolicy1);

        horizontalLayout_8->addWidget(tbAddFave);

        tbRemoveFave = new QToolButton(widget_2);
        tbRemoveFave->setObjectName(QString::fromUtf8("tbRemoveFave"));
        sizePolicy1.setHeightForWidth(tbRemoveFave->sizePolicy().hasHeightForWidth());
        tbRemoveFave->setSizePolicy(sizePolicy1);

        horizontalLayout_8->addWidget(tbRemoveFave);

        tbRenameFave = new QToolButton(widget_2);
        tbRenameFave->setObjectName(QString::fromUtf8("tbRenameFave"));
        sizePolicy1.setHeightForWidth(tbRenameFave->sizePolicy().hasHeightForWidth());
        tbRenameFave->setSizePolicy(sizePolicy1);

        horizontalLayout_8->addWidget(tbRenameFave);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_8->addItem(horizontalSpacer);

        tbTags = new QToolButton(widget_2);
        tbTags->setObjectName(QString::fromUtf8("tbTags"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icons/color-wheel.png"), QSize(), QIcon::Normal, QIcon::Off);
        tbTags->setIcon(icon);

        horizontalLayout_8->addWidget(tbTags);

        tbSelectionMode = new QToolButton(widget_2);
        tbSelectionMode->setObjectName(QString::fromUtf8("tbSelectionMode"));

        horizontalLayout_8->addWidget(tbSelectionMode);

        tbExpandCollapse = new QToolButton(widget_2);
        tbExpandCollapse->setObjectName(QString::fromUtf8("tbExpandCollapse"));
        sizePolicy1.setHeightForWidth(tbExpandCollapse->sizePolicy().hasHeightForWidth());
        tbExpandCollapse->setSizePolicy(sizePolicy1);

        horizontalLayout_8->addWidget(tbExpandCollapse);


        verticalLayout_2->addWidget(widget_2);

        widget = new QWidget(filtersFrame);
        widget->setObjectName(QString::fromUtf8("widget"));
        horizontalLayout_7 = new QHBoxLayout(widget);
        horizontalLayout_7->setObjectName(QString::fromUtf8("horizontalLayout_7"));
        horizontalLayout_7->setContentsMargins(-1, 0, -1, 0);
        tbUpdateFilters = new QToolButton(widget);
        tbUpdateFilters->setObjectName(QString::fromUtf8("tbUpdateFilters"));
        sizePolicy1.setHeightForWidth(tbUpdateFilters->sizePolicy().hasHeightForWidth());
        tbUpdateFilters->setSizePolicy(sizePolicy1);

        horizontalLayout_7->addWidget(tbUpdateFilters);

        cbInternetUpdate = new QCheckBox(widget);
        cbInternetUpdate->setObjectName(QString::fromUtf8("cbInternetUpdate"));

        horizontalLayout_7->addWidget(cbInternetUpdate);


        verticalLayout_2->addWidget(widget);

        verticalLayout_2->setStretch(1, 1);
        splitter->addWidget(filtersFrame);
        parametersPanel = new QFrame(splitter);
        parametersPanel->setObjectName(QString::fromUtf8("parametersPanel"));
        QSizePolicy sizePolicy2(QSizePolicy::MinimumExpanding, QSizePolicy::Preferred);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(parametersPanel->sizePolicy().hasHeightForWidth());
        parametersPanel->setSizePolicy(sizePolicy2);
        parametersPanel->setFrameShape(QFrame::Shape::NoFrame);
        parametersPanel->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_5 = new QVBoxLayout(parametersPanel);
        verticalLayout_5->setObjectName(QString::fromUtf8("verticalLayout_5"));
        verticalSplitter = new QSplitter(parametersPanel);
        verticalSplitter->setObjectName(QString::fromUtf8("verticalSplitter"));
        verticalSplitter->setOrientation(Qt::Orientation::Vertical);
        verticalSplitter->setHandleWidth(6);
        vSplitterTopWidget = new QWidget(verticalSplitter);
        vSplitterTopWidget->setObjectName(QString::fromUtf8("vSplitterTopWidget"));
        vSplitterTopWidget->setMinimumSize(QSize(0, 150));
        verticalLayout_4 = new QVBoxLayout(vSplitterTopWidget);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        verticalLayout_4->setContentsMargins(0, 0, 0, 0);
        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setObjectName(QString::fromUtf8("horizontalLayout_6"));
        filterName = new QLabel(vSplitterTopWidget);
        filterName->setObjectName(QString::fromUtf8("filterName"));
        QSizePolicy sizePolicy3(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy3.setHorizontalStretch(0);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(filterName->sizePolicy().hasHeightForWidth());
        filterName->setSizePolicy(sizePolicy3);

        horizontalLayout_6->addWidget(filterName);

        tbCopyCommand = new QToolButton(vSplitterTopWidget);
        tbCopyCommand->setObjectName(QString::fromUtf8("tbCopyCommand"));

        horizontalLayout_6->addWidget(tbCopyCommand);

        tbRandomizeParameters = new QToolButton(vSplitterTopWidget);
        tbRandomizeParameters->setObjectName(QString::fromUtf8("tbRandomizeParameters"));

        horizontalLayout_6->addWidget(tbRandomizeParameters);

        tbResetParameters = new QToolButton(vSplitterTopWidget);
        tbResetParameters->setObjectName(QString::fromUtf8("tbResetParameters"));

        horizontalLayout_6->addWidget(tbResetParameters);


        verticalLayout_4->addLayout(horizontalLayout_6);

        scrollAreaParameters = new QScrollArea(vSplitterTopWidget);
        scrollAreaParameters->setObjectName(QString::fromUtf8("scrollAreaParameters"));
        QSizePolicy sizePolicy4(QSizePolicy::Preferred, QSizePolicy::Expanding);
        sizePolicy4.setHorizontalStretch(0);
        sizePolicy4.setVerticalStretch(0);
        sizePolicy4.setHeightForWidth(scrollAreaParameters->sizePolicy().hasHeightForWidth());
        scrollAreaParameters->setSizePolicy(sizePolicy4);
        scrollAreaParameters->setFrameShape(QFrame::Shape::NoFrame);
        scrollAreaParameters->setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy::ScrollBarAsNeeded);
        scrollAreaParameters->setSizeAdjustPolicy(QAbstractScrollArea::SizeAdjustPolicy::AdjustToContents);
        scrollAreaParameters->setWidgetResizable(true);
        scrollAreaWidgetContents_2 = new QWidget();
        scrollAreaWidgetContents_2->setObjectName(QString::fromUtf8("scrollAreaWidgetContents_2"));
        scrollAreaWidgetContents_2->setGeometry(QRect(0, 0, 227, 397));
        verticalLayout_6 = new QVBoxLayout(scrollAreaWidgetContents_2);
        verticalLayout_6->setObjectName(QString::fromUtf8("verticalLayout_6"));
        filterParams = new GmicQt::FilterParametersWidget(scrollAreaWidgetContents_2);
        filterParams->setObjectName(QString::fromUtf8("filterParams"));
        sizePolicy.setHeightForWidth(filterParams->sizePolicy().hasHeightForWidth());
        filterParams->setSizePolicy(sizePolicy);
        filterParams->setFocusPolicy(Qt::FocusPolicy::NoFocus);

        verticalLayout_6->addWidget(filterParams);

        scrollAreaParameters->setWidget(scrollAreaWidgetContents_2);

        verticalLayout_4->addWidget(scrollAreaParameters);

        verticalSpacer = new QSpacerItem(20, 9, QSizePolicy::Policy::Fixed, QSizePolicy::Minimum);

        verticalLayout_4->addItem(verticalSpacer);

        vSplitterLine = new QFrame(vSplitterTopWidget);
        vSplitterLine->setObjectName(QString::fromUtf8("vSplitterLine"));
        vSplitterLine->setFrameShape(QFrame::HLine);
        vSplitterLine->setFrameShadow(QFrame::Sunken);

        verticalLayout_4->addWidget(vSplitterLine);

        verticalSplitter->addWidget(vSplitterTopWidget);
        inOutSelector = new GmicQt::InOutPanel(verticalSplitter);
        inOutSelector->setObjectName(QString::fromUtf8("inOutSelector"));
        sizePolicy.setHeightForWidth(inOutSelector->sizePolicy().hasHeightForWidth());
        inOutSelector->setSizePolicy(sizePolicy);
        inOutSelector->setAutoFillBackground(false);
        verticalSplitter->addWidget(inOutSelector);

        verticalLayout_5->addWidget(verticalSplitter);

        splitter->addWidget(parametersPanel);
        previewPanel = new QWidget(splitter);
        previewPanel->setObjectName(QString::fromUtf8("previewPanel"));
        verticalLayout = new QVBoxLayout(previewPanel);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        previewFrame = new QFrame(previewPanel);
        previewFrame->setObjectName(QString::fromUtf8("previewFrame"));
        previewFrame->setFrameShape(QFrame::Shape::StyledPanel);
        previewFrame->setFrameShadow(QFrame::Shadow::Raised);
        verticalLayout_7 = new QVBoxLayout(previewFrame);
        verticalLayout_7->setSpacing(2);
        verticalLayout_7->setObjectName(QString::fromUtf8("verticalLayout_7"));
        verticalLayout_7->setContentsMargins(2, 2, 2, 2);
        previewWidget = new GmicQt::PreviewWidget(previewFrame);
        previewWidget->setObjectName(QString::fromUtf8("previewWidget"));
        previewWidget->setFocusPolicy(Qt::FocusPolicy::StrongFocus);

        verticalLayout_7->addWidget(previewWidget);


        verticalLayout->addWidget(previewFrame);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        cbPreview = new QCheckBox(previewPanel);
        cbPreview->setObjectName(QString::fromUtf8("cbPreview"));

        horizontalLayout_2->addWidget(cbPreview);

        cbPreviewType = new QComboBox(previewPanel);
        cbPreviewType->setObjectName(QString::fromUtf8("cbPreviewType"));

        horizontalLayout_2->addWidget(cbPreviewType);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);

        zoomLevelSelector = new GmicQt::ZoomLevelSelector(previewPanel);
        zoomLevelSelector->setObjectName(QString::fromUtf8("zoomLevelSelector"));
        zoomLevelSelector->setMinimumSize(QSize(40, 0));

        horizontalLayout_2->addWidget(zoomLevelSelector);


        verticalLayout->addLayout(horizontalLayout_2);

        belowPreviewWidget = new QWidget(previewPanel);
        belowPreviewWidget->setObjectName(QString::fromUtf8("belowPreviewWidget"));
        horizontalLayout_5 = new QHBoxLayout(belowPreviewWidget);
        horizontalLayout_5->setObjectName(QString::fromUtf8("horizontalLayout_5"));
        horizontalLayout_5->setContentsMargins(0, 0, 0, 0);
        belowPreviewPadding = new QWidget(belowPreviewWidget);
        belowPreviewPadding->setObjectName(QString::fromUtf8("belowPreviewPadding"));
        QSizePolicy sizePolicy5(QSizePolicy::Expanding, QSizePolicy::Preferred);
        sizePolicy5.setHorizontalStretch(0);
        sizePolicy5.setVerticalStretch(0);
        sizePolicy5.setHeightForWidth(belowPreviewPadding->sizePolicy().hasHeightForWidth());
        belowPreviewPadding->setSizePolicy(sizePolicy5);

        horizontalLayout_5->addWidget(belowPreviewPadding);

        logosLabel = new QLabel(belowPreviewWidget);
        logosLabel->setObjectName(QString::fromUtf8("logosLabel"));
        sizePolicy.setHeightForWidth(logosLabel->sizePolicy().hasHeightForWidth());
        logosLabel->setSizePolicy(sizePolicy);
        logosLabel->setPixmap(QPixmap(QString::fromUtf8(":/resources/gimp_logos.png")));
        logosLabel->setAlignment(Qt::AlignmentFlag::AlignCenter);

        horizontalLayout_5->addWidget(logosLabel);

        horizontalLayout_5->setStretch(0, 1);

        verticalLayout->addWidget(belowPreviewWidget);

        verticalLayout->setStretch(0, 1);
        splitter->addWidget(previewPanel);

        verticalLayout_3->addWidget(splitter);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        pbSettings = new QPushButton(centralwidget);
        pbSettings->setObjectName(QString::fromUtf8("pbSettings"));
        QSizePolicy sizePolicy6(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy6.setHorizontalStretch(0);
        sizePolicy6.setVerticalStretch(0);
        sizePolicy6.setHeightForWidth(pbSettings->sizePolicy().hasHeightForWidth());
        pbSettings->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbSettings);

        progressInfoWidget = new GmicQt::ProgressInfoWidget(centralwidget);
        progressInfoWidget->setObjectName(QString::fromUtf8("progressInfoWidget"));

        horizontalLayout->addWidget(progressInfoWidget);

        messageLabel = new QLabel(centralwidget);
        messageLabel->setObjectName(QString::fromUtf8("messageLabel"));
        sizePolicy.setHeightForWidth(messageLabel->sizePolicy().hasHeightForWidth());
        messageLabel->setSizePolicy(sizePolicy);

        horizontalLayout->addWidget(messageLabel);

        rightMessageLabel = new QLabel(centralwidget);
        rightMessageLabel->setObjectName(QString::fromUtf8("rightMessageLabel"));

        horizontalLayout->addWidget(rightMessageLabel);

        pbFullscreen = new QPushButton(centralwidget);
        pbFullscreen->setObjectName(QString::fromUtf8("pbFullscreen"));
        sizePolicy6.setHeightForWidth(pbFullscreen->sizePolicy().hasHeightForWidth());
        pbFullscreen->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbFullscreen);

        pbClose = new QPushButton(centralwidget);
        pbClose->setObjectName(QString::fromUtf8("pbClose"));
        sizePolicy6.setHeightForWidth(pbClose->sizePolicy().hasHeightForWidth());
        pbClose->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbClose);

        pbCancel = new QPushButton(centralwidget);
        pbCancel->setObjectName(QString::fromUtf8("pbCancel"));
        sizePolicy6.setHeightForWidth(pbCancel->sizePolicy().hasHeightForWidth());
        pbCancel->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbCancel);

        pbApply = new QPushButton(centralwidget);
        pbApply->setObjectName(QString::fromUtf8("pbApply"));
        sizePolicy6.setHeightForWidth(pbApply->sizePolicy().hasHeightForWidth());
        pbApply->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbApply);

        pbOk = new QPushButton(centralwidget);
        pbOk->setObjectName(QString::fromUtf8("pbOk"));
        sizePolicy6.setHeightForWidth(pbOk->sizePolicy().hasHeightForWidth());
        pbOk->setSizePolicy(sizePolicy6);

        horizontalLayout->addWidget(pbOk);

        horizontalLayout->setStretch(1, 1);

        verticalLayout_3->addLayout(horizontalLayout);

        verticalLayout_3->setStretch(0, 1);
        MainWindow->setCentralWidget(centralwidget);
        QWidget::setTabOrder(previewWidget, cbPreview);
        QWidget::setTabOrder(cbPreview, pbCancel);
        QWidget::setTabOrder(pbCancel, pbApply);
        QWidget::setTabOrder(pbApply, pbOk);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        centralwidget->setWindowTitle(QCoreApplication::translate("MainWindow", "Form", nullptr));
        tbAddFave->setText(QString());
        tbRemoveFave->setText(QString());
        tbRenameFave->setText(QString());
        tbTags->setText(QString());
        tbSelectionMode->setText(QString());
        tbExpandCollapse->setText(QString());
        tbUpdateFilters->setText(QString());
#if QT_CONFIG(tooltip)
        cbInternetUpdate->setToolTip(QCoreApplication::translate("MainWindow", "<html><head/><body><p>Download filter definitions from remote sources</p></body></html>", nullptr));
#endif // QT_CONFIG(tooltip)
        cbInternetUpdate->setText(QCoreApplication::translate("MainWindow", "Internet", nullptr));
        filterName->setText(QString());
        tbCopyCommand->setText(QCoreApplication::translate("MainWindow", "...", nullptr));
        tbRandomizeParameters->setText(QCoreApplication::translate("MainWindow", "...", nullptr));
        tbResetParameters->setText(QCoreApplication::translate("MainWindow", "...", nullptr));
#if QT_CONFIG(tooltip)
        cbPreview->setToolTip(QCoreApplication::translate("MainWindow", "<html><head/><body><p>Enable/disable preview<br/>(Ctrl+P)<br/>(right click on preview image for instant swapping)</p></body></html>", nullptr));
#endif // QT_CONFIG(tooltip)
        cbPreview->setText(QCoreApplication::translate("MainWindow", "Preview", nullptr));
#if QT_CONFIG(tooltip)
        cbPreviewType->setToolTip(QCoreApplication::translate("MainWindow", "Preview type (Ctrl+Shift+P)", nullptr));
#endif // QT_CONFIG(tooltip)
        logosLabel->setText(QString());
        pbSettings->setText(QCoreApplication::translate("MainWindow", "&Settings...", nullptr));
        messageLabel->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        rightMessageLabel->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        pbFullscreen->setText(QCoreApplication::translate("MainWindow", "&Fullscreen", nullptr));
        pbClose->setText(QCoreApplication::translate("MainWindow", "&Close", nullptr));
        pbCancel->setText(QCoreApplication::translate("MainWindow", "&Cancel", nullptr));
        pbApply->setText(QCoreApplication::translate("MainWindow", "&Apply", nullptr));
        pbOk->setText(QCoreApplication::translate("MainWindow", "&OK", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
