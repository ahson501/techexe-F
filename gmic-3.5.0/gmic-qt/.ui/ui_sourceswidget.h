/********************************************************************************
** Form generated from reading UI file 'sourceswidget.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SOURCESWIDGET_H
#define UI_SOURCESWIDGET_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_SourcesWidget
{
public:
    QVBoxLayout *verticalLayout_2;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label;
    QLineEdit *leURL;
    QToolButton *tbNew;
    QToolButton *tbOpen;
    QHBoxLayout *horizontalLayout;
    QListWidget *list;
    QVBoxLayout *verticalLayout;
    QToolButton *tbUp;
    QToolButton *tbDown;
    QSpacerItem *verticalSpacer_2;
    QToolButton *tbReset;
    QToolButton *tbTrash;
    QSpacerItem *verticalSpacer;
    QHBoxLayout *horizontalLayout_4;
    QLabel *labelVariables;
    QFrame *line;
    QHBoxLayout *horizontalLayout_3;
    QLabel *label_2;
    QComboBox *cbOfficialFilters;
    QSpacerItem *horizontalSpacer;

    void setupUi(QWidget *SourcesWidget)
    {
        if (SourcesWidget->objectName().isEmpty())
            SourcesWidget->setObjectName(QString::fromUtf8("SourcesWidget"));
        SourcesWidget->resize(694, 524);
        verticalLayout_2 = new QVBoxLayout(SourcesWidget);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label = new QLabel(SourcesWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout_2->addWidget(label);

        leURL = new QLineEdit(SourcesWidget);
        leURL->setObjectName(QString::fromUtf8("leURL"));

        horizontalLayout_2->addWidget(leURL);

        tbNew = new QToolButton(SourcesWidget);
        tbNew->setObjectName(QString::fromUtf8("tbNew"));

        horizontalLayout_2->addWidget(tbNew);

        tbOpen = new QToolButton(SourcesWidget);
        tbOpen->setObjectName(QString::fromUtf8("tbOpen"));

        horizontalLayout_2->addWidget(tbOpen);


        verticalLayout_2->addLayout(horizontalLayout_2);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        list = new QListWidget(SourcesWidget);
        list->setObjectName(QString::fromUtf8("list"));

        horizontalLayout->addWidget(list);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        tbUp = new QToolButton(SourcesWidget);
        tbUp->setObjectName(QString::fromUtf8("tbUp"));

        verticalLayout->addWidget(tbUp);

        tbDown = new QToolButton(SourcesWidget);
        tbDown->setObjectName(QString::fromUtf8("tbDown"));

        verticalLayout->addWidget(tbDown);

        verticalSpacer_2 = new QSpacerItem(10, 35, QSizePolicy::Minimum, QSizePolicy::Fixed);

        verticalLayout->addItem(verticalSpacer_2);

        tbReset = new QToolButton(SourcesWidget);
        tbReset->setObjectName(QString::fromUtf8("tbReset"));

        verticalLayout->addWidget(tbReset);

        tbTrash = new QToolButton(SourcesWidget);
        tbTrash->setObjectName(QString::fromUtf8("tbTrash"));

        verticalLayout->addWidget(tbTrash);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);


        horizontalLayout->addLayout(verticalLayout);


        verticalLayout_2->addLayout(horizontalLayout);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        labelVariables = new QLabel(SourcesWidget);
        labelVariables->setObjectName(QString::fromUtf8("labelVariables"));

        horizontalLayout_4->addWidget(labelVariables);


        verticalLayout_2->addLayout(horizontalLayout_4);

        line = new QFrame(SourcesWidget);
        line->setObjectName(QString::fromUtf8("line"));
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);

        verticalLayout_2->addWidget(line);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        label_2 = new QLabel(SourcesWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        horizontalLayout_3->addWidget(label_2);

        cbOfficialFilters = new QComboBox(SourcesWidget);
        cbOfficialFilters->setObjectName(QString::fromUtf8("cbOfficialFilters"));

        horizontalLayout_3->addWidget(cbOfficialFilters);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer);


        verticalLayout_2->addLayout(horizontalLayout_3);


        retranslateUi(SourcesWidget);

        QMetaObject::connectSlotsByName(SourcesWidget);
    } // setupUi

    void retranslateUi(QWidget *SourcesWidget)
    {
        SourcesWidget->setWindowTitle(QCoreApplication::translate("SourcesWidget", "Form", nullptr));
        label->setText(QCoreApplication::translate("SourcesWidget", "File / URL", nullptr));
        tbNew->setText(QCoreApplication::translate("SourcesWidget", "Add new", nullptr));
        tbOpen->setText(QCoreApplication::translate("SourcesWidget", "...", nullptr));
        tbUp->setText(QCoreApplication::translate("SourcesWidget", "...", nullptr));
        tbDown->setText(QCoreApplication::translate("SourcesWidget", "...", nullptr));
        tbReset->setText(QCoreApplication::translate("SourcesWidget", "...", nullptr));
        tbTrash->setText(QCoreApplication::translate("SourcesWidget", "...", nullptr));
        labelVariables->setText(QCoreApplication::translate("SourcesWidget", "Macros: $HOME $VERSION", nullptr));
        label_2->setText(QCoreApplication::translate("SourcesWidget", "Official filters:", nullptr));
    } // retranslateUi

};

namespace Ui {
    class SourcesWidget: public Ui_SourcesWidget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SOURCESWIDGET_H
