#ifndef LOCALSTRUCT_H
#define LOCALSTRUCT_H
#include <QMetaType>
#include <QString>

struct StructCopyFileDirectory
{
    bool isStop = false;
    bool firstRead = true;
    bool coverFileIfExist = true;
    float floatTotal = 0;
    float floatValue = 0;
    int currentFileCount = 0;
    int allFileCount = 0;
    QString fromDir = "";
    QString toDir = "";
    QString fileName = "";
};
Q_DECLARE_METATYPE(StructCopyFileDirectory);
#endif // LOCALSTRUCT_H
