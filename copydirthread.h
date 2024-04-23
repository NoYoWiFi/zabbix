#ifndef COPYDIRTHREAD_H
#define COPYDIRTHREAD_H

#include <QObject>
#include <QMutex>
#include "localMethod/localStruct.h"
#include <QDir>

class CopyDirThread : public QObject
{
    Q_OBJECT

public:
    CopyDirThread(QObject *parent = nullptr);
    ~CopyDirThread();

signals:
    void signal_readyReadStandard(QString str);
    void signal_allFileCount(int i);
    void signal_progress(int val,int filec);
    void signal_deployFinish();
    void signal_errorBreak();

public slots:
    void   slot_onCopyDirClose();
    void   slot_systemVar(StructCopyFileDirectory stru);
    void   slot_deployStart();
    void   slot_button_4Cancel_onClicked();
    void   slot_errorBreak();

public:
    int             gm_getFileCount(QString frompath);
    struct          StructCopyFileDirectory copyFileDirectory();
    struct          StructCopyFileDirectory copyFile();

private:
    bool            gv_isStop;
    QMutex          gv_stopMutex;

private:
    StructCopyFileDirectory gv_stru;
};

#endif // COPYDIRTHREAD_H
