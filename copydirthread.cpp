#include "copydirthread.h"

CopyDirThread::CopyDirThread(QObject *parent) : QObject(parent)
  ,gv_isStop(false)
  ,gv_stopMutex()
{
}

CopyDirThread::~CopyDirThread()
{
}

void CopyDirThread::slot_systemVar(StructCopyFileDirectory stru)
{
    gv_stru.fromDir = stru.fromDir;
    gv_stru.toDir = stru.toDir;
    qDebug()<<gv_stru.fromDir<<gv_stru.toDir;
}


void CopyDirThread::slot_deployStart()
{
    QMutexLocker locker(&gv_stopMutex);
    //    qDebug()<<gv_stru.isoFilePath<<gv_stru.osVersion<<gv_stru.osIndex;
    gv_stru.isStop = false;
    gv_stru.firstRead = true;
    gv_stru.coverFileIfExist = true;
    gv_stru.floatTotal = 0;
    gv_stru.floatValue = 0;
    gv_stru.currentFileCount = 0;
    gv_stru.allFileCount = 0;
    CopyDirThread::gm_getFileCount(QString::fromLocal8Bit("%1").arg(gv_stru.fromDir));
    signal_allFileCount(gv_stru.allFileCount);
    qDebug()<<gv_stru.allFileCount;
    CopyDirThread::copyFileDirectory();
    if(gv_stru.isStop)
        return;
    emit signal_deployFinish();
}

void CopyDirThread::slot_button_4Cancel_onClicked()
{
    gv_stru.isStop = true;
    emit signal_errorBreak();
}

void CopyDirThread::slot_errorBreak()
{
    emit signal_readyReadStandard(QString::fromLocal8Bit("拷贝文件被中断"));
    emit signal_deployFinish();
}

int CopyDirThread::gm_getFileCount(QString frompath)
{
    QDir lv_myDir(frompath);
    lv_myDir.setFilter(QDir::AllEntries|QDir::Hidden|QDir::NoSymLinks);
    QFileInfo lv_fileInfo;
    gv_stru.allFileCount = gv_stru.allFileCount + static_cast<int>(lv_myDir.entryInfoList().count());
    for(unsigned int i=0;i<lv_myDir.count();i++)
    {
        lv_fileInfo=QFileInfo(lv_myDir.filePath(lv_myDir[static_cast<int>(i)]));
        //        qDebug()<<lv_fileInfo.fileName();
        if((lv_fileInfo.fileName()==".")||(lv_fileInfo.fileName()==".."))
        {
            gv_stru.allFileCount = gv_stru.allFileCount - 1;
            continue;
        }
        if(lv_fileInfo.isDir())
        {
            gv_stru.allFileCount = gv_stru.allFileCount - 1;
            CopyDirThread::gm_getFileCount(lv_myDir.filePath(lv_myDir[static_cast<int>(i)]));
            //            qDebug()<<lv_intRemainingFilesCount;
        }
    }
    return gv_stru.allFileCount;
}

struct StructCopyFileDirectory CopyDirThread::copyFileDirectory()
{
    QDir lv_sourceDir(gv_stru.fromDir);
    lv_sourceDir.setFilter(QDir::AllEntries|QDir::Hidden|QDir::NoSymLinks);
    QDir lv_targetDir(gv_stru.toDir);
    if(!lv_targetDir.exists()){/**< 如果目标目录不存在，则进行创建 */
        if(!lv_targetDir.mkdir(lv_targetDir.absolutePath())) {
            return gv_stru;
        }
    }
    QFileInfoList lv_fileInfoList = lv_sourceDir.entryInfoList();
    if(gv_stru.firstRead) {
        int lv_isfileTMP = 0;
        foreach(QFileInfo lv_fileInfo, lv_fileInfoList){
            if(lv_fileInfo.isFile()) {
                lv_isfileTMP++;
            }
        }
        gv_stru.floatTotal = lv_fileInfoList.count() - 2 - lv_isfileTMP; // 2为.和..
        gv_stru.floatValue = 0;
        gv_stru.firstRead = false;
        if(std::abs(gv_stru.floatValue - gv_stru.floatTotal) <= 0.000001f) {
            gv_stru.firstRead = true;
        }
    } else {
        gv_stru.floatValue++;
        if(std::abs(gv_stru.floatValue - gv_stru.floatTotal) <= 0.000001f) {
            gv_stru.firstRead = true;
        }
    }
    foreach(QFileInfo lv_fileInfo, lv_fileInfoList){
        if(lv_fileInfo.fileName() == "." || lv_fileInfo.fileName() == "..") {
            continue;
        }
        if(lv_fileInfo.isDir()){/**< 当为目录时，递归的进行copy */
            //            qDebug()<<lv_fileInfo.fileName();
            gv_stru.fromDir = lv_fileInfo.filePath();
            gv_stru.toDir = lv_targetDir.filePath(lv_fileInfo.fileName());
            CopyDirThread::copyFileDirectory();
        } else{/**< 当允许覆盖操作时，将旧文件进行删除操作 */
            if(gv_stru.coverFileIfExist && lv_targetDir.exists(lv_fileInfo.fileName())){
                lv_targetDir.remove(lv_fileInfo.fileName());
            }
            /// 进行文件copy
            //            qDebug()<<lv_fileInfo.filePath();

            char *byteTemp = new char[4096];
            qint64 fileSize = 0;
            qint64 totalCopySize = 0;
            QFile tofile;
            tofile.setFileName(lv_targetDir.filePath(lv_fileInfo.fileName()));
            if(!tofile.open(QIODevice::WriteOnly)){
                emit signal_readyReadStandard(QString::fromLocal8Bit("open %1 failed").arg(lv_targetDir.filePath(lv_fileInfo.fileName())));
                return gv_stru;
            }
            QDataStream out(&tofile);
            out.setVersion(QDataStream::Qt_5_12);
            QFile fromfile;
            fromfile.setFileName(lv_fileInfo.filePath());
            if(!fromfile.open(QIODevice::ReadOnly)){
                emit signal_readyReadStandard(QString::fromLocal8Bit("open %1 failed").arg(lv_fileInfo.filePath()));
                return gv_stru;
            }
            fileSize = fromfile.size();
            emit signal_allFileCount(fileSize / 1024 / 1024);
            QDataStream in(&fromfile);
            in.setVersion(QDataStream::Qt_5_12);
            //            qDebug()<<fromfile<<tofile;
            qint64 readSize = 0;
            gv_stru.allFileCount--;
            while (!in.atEnd()) {
                readSize = in.readRawData(byteTemp, 4096);
                out.writeRawData(byteTemp, readSize);
                totalCopySize += readSize;
                emit signal_progress(totalCopySize / 1024 / 1024, gv_stru.allFileCount);
                if(gv_stru.isStop){
                    return gv_stru;
                }
            }
            if(totalCopySize == fileSize){
                tofile.setPermissions(QFile::ExeUser);
                tofile.close();
                fromfile.close();
                gv_stru.currentFileCount++;
            }

            //            QFile::copy(lv_fileInfo.filePath(), lv_targetDir.filePath(lv_fileInfo.fileName()));
            //            emit signal_progress(gv_stru.currentFileCount, gv_stru.allFileCount);
        }
    }
    return gv_stru;
}

struct StructCopyFileDirectory CopyDirThread::copyFile()
{

    /**< 当允许覆盖操作时，将旧文件进行删除操作 */
    if(gv_stru.coverFileIfExist && QFile(gv_stru.toDir).exists()){
        QFile(gv_stru.toDir).remove();
    }
    /// 进行文件copy
    char *byteTemp = new char[4096];
    qint64 fileSize = 0;
    qint64 totalCopySize = 0;
    QFile tofile;
    tofile.setFileName(gv_stru.toDir);
    if(!tofile.open(QIODevice::WriteOnly)){
        emit signal_readyReadStandard(QString::fromLocal8Bit("open %1 failed").arg(gv_stru.toDir));
        return gv_stru;
    }
    QDataStream out(&tofile);
    out.setVersion(QDataStream::Qt_5_12);
    QFile fromfile;
    fromfile.setFileName(gv_stru.fromDir);
    if(!fromfile.open(QIODevice::ReadOnly)){
        emit signal_readyReadStandard(QString::fromLocal8Bit("open %1 failed").arg(gv_stru.fromDir));
        return gv_stru;
    }
    fileSize = fromfile.size();
    emit signal_allFileCount(fileSize / 1024 / 1024);
    QDataStream in(&fromfile);
    in.setVersion(QDataStream::Qt_5_12);
    //            qDebug()<<fromfile<<tofile;
    qint64 readSize = 0;
    gv_stru.allFileCount--;
    while (!in.atEnd()) {
        readSize = in.readRawData(byteTemp, 4096);
        out.writeRawData(byteTemp, readSize);
        totalCopySize += readSize;
        emit signal_progress(totalCopySize / 1024 / 1024, gv_stru.allFileCount);
        if(gv_stru.isStop){
            return gv_stru;
        }
    }
    if(totalCopySize == fileSize){
        tofile.setPermissions(QFile::ExeUser);
        tofile.close();
        fromfile.close();
        gv_stru.currentFileCount++;
    }

    //            QFile::copy(lv_fileInfo.filePath(), lv_targetDir.filePath(lv_fileInfo.fileName()));
    //            emit signal_progress(gv_stru.currentFileCount, gv_stru.allFileCount);
    return gv_stru;
}

void CopyDirThread::slot_onCopyDirClose()
{
    return;
}
