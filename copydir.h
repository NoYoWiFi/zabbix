#ifndef COPYDIR_H
#define COPYDIR_H
#include <QObject>
#include <QQmlApplicationEngine>
#include "copydirthread.h"
#include <QThread>
#include <QQmlComponent>

class CopyDir : public QObject
{
    Q_OBJECT

public:
    explicit CopyDir(QObject *parent = nullptr);
    ~CopyDir();

signals:
    void signal_systemVar(StructCopyFileDirectory stru);
    void signal_deployStart();
    void signal_deployFinish();

public slots:
    void slot_button_3Deploy_onClicked();
    void slot_readyReadStandard(QString str);
    void slot_progress(int intCurrentFileCount, int intRemainingFilesCount);
    void slot_allFileCount(int i);
    void slot_deployFinish();

public:
    QQmlApplicationEngine *gp_qmlEngine;
    QObject               *gp_rootObject;
    QThread               *gp_copyDirThread;
    CopyDirThread         *gp_copyDirThreadObj;
    StructCopyFileDirectory gv_stru;
    QString               gv_readyReadStandard;
};

#endif // COPYDIR_H
