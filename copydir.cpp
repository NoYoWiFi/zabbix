#include "copydir.h"

CopyDir::CopyDir(QObject *parent) : QObject(parent)
  ,gv_readyReadStandard("")
{
    gp_qmlEngine = new QQmlApplicationEngine(this);
    QQmlComponent lv_component(gp_qmlEngine, QUrl(QStringLiteral("qrc:/qmls/main.qml")));
    gp_rootObject = lv_component.create();
    gp_rootObject->setParent(this);
    gp_rootObject->setProperty("visible", true);
    //#![]
    gp_copyDirThread = new QThread(this);
    gp_copyDirThreadObj = new CopyDirThread();
    gp_copyDirThreadObj->moveToThread(gp_copyDirThread);
    QObject::connect(gp_copyDirThread,SIGNAL(finished())
                     ,gp_copyDirThreadObj,SLOT(deleteLater()));
    QObject::connect(gp_rootObject, SIGNAL(signal_button_3Deploy_onClicked()),
                     this, SLOT(slot_button_3Deploy_onClicked()));
    QObject::connect(gp_rootObject, SIGNAL(signal_button_4Cancel_onClicked()),
                     gp_copyDirThreadObj, SLOT(slot_button_4Cancel_onClicked()), Qt::DirectConnection);
    QObject::connect(this,SIGNAL(signal_systemVar(StructCopyFileDirectory))
                     ,gp_copyDirThreadObj,SLOT(slot_systemVar(StructCopyFileDirectory)));
    QObject::connect(this,SIGNAL(signal_deployStart())
                     ,gp_copyDirThreadObj,SLOT(slot_deployStart()));
    QObject::connect(gp_copyDirThreadObj,SIGNAL(signal_progress(int,int))
                     ,this,SLOT(slot_progress(int,int)));
    QObject::connect(gp_copyDirThreadObj, SIGNAL(signal_allFileCount(int)),
                     this,SLOT(slot_allFileCount(int)));
    QObject::connect(gp_rootObject, SIGNAL(signal_onCopyDirClose()),
                     gp_copyDirThreadObj, SLOT(slot_onCopyDirClose()), Qt::DirectConnection);
    QObject::connect(gp_copyDirThreadObj,SIGNAL(signal_deployFinish())
                     ,this,SLOT(slot_deployFinish()));

    QObject::connect(gp_copyDirThreadObj, SIGNAL(signal_readyReadStandard(QString)),
                     this, SLOT(slot_readyReadStandard(QString)));
    gp_copyDirThread->start();
}

CopyDir::~CopyDir()
{
}

void CopyDir::slot_button_3Deploy_onClicked()
{
    gp_rootObject->setProperty("gv_readyReadStandard", "");
    // [Linux]
    // gv_stru.fromDir = gp_rootObject->property("gv_strFromDirPath").toString().mid(7,-1);
    // gv_stru.toDir = gp_rootObject->property("gv_strToDirPath").toString().mid(7,-1);
    //[Windows]
    gv_stru.fromDir = gp_rootObject->property("gv_strFromDirPath").toString().mid(8,-1);
    gv_stru.toDir = gp_rootObject->property("gv_strToDirPath").toString().mid(8,-1);

    if(gv_stru.fromDir!=""&& gv_stru.toDir!="")
    {
        bool lv_b = QDir(gv_stru.toDir + "/" + QDir(gv_stru.fromDir).dirName()).exists();
        if(!lv_b)
        {
            QDir(gv_stru.toDir).mkdir(QDir(gv_stru.fromDir).dirName());
            gp_rootObject->setProperty("gv_boolEnable",false);
            gv_stru.toDir = gv_stru.toDir + "/" + QDir(gv_stru.fromDir).dirName();
            emit signal_systemVar(gv_stru);
            emit signal_deployStart();
        }
        else
        {
            // [Linux]
            // gp_rootObject->setProperty("gv_readyReadStandard", QString::fromLocal8Bit("###文件夹已存在###"));
            // [Windows]
            gp_rootObject->setProperty("gv_readyReadStandard", QString::fromUtf8("###文件夹已存在###"));
            return;
        }
    }
}

void CopyDir::slot_readyReadStandard(QString str)
{
    gp_rootObject->setProperty("gv_readyReadStandard", str);
}

void CopyDir::slot_progress(int intCurrentFileCount,int intRemainingFilesCount)
{
    gp_rootObject->setProperty("gv_intCurrentFileCount", intCurrentFileCount);
    // [Linux]
    // gp_rootObject->setProperty("gv_readyReadStandard", QString::fromLocal8Bit("剩余文件个数:%1").arg(intRemainingFilesCount));
    // [Windows]
    gp_rootObject->setProperty("gv_readyReadStandard", QString::fromUtf8("剩余文件个数:%1").arg(intRemainingFilesCount));
}

void CopyDir::slot_allFileCount(int i)
{
    gp_rootObject->setProperty("gv_intAllFileCount", i);
}

void CopyDir::slot_deployFinish()
{
    emit signal_deployFinish();
    gp_rootObject->setProperty("gv_boolEnable",true);
}
