#include <QGuiApplication>
#include <QApplication>
//#include <QQmlApplicationEngine>
//#include "localMethod/localMethod.h"
#include "localMethod/localStruct.h"
#include "copydir.h"

int main(int argc, char *argv[])
{
//    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QApplication app(argc, argv);
//    qRegisterMetaType<StructInstalled>("StructInstalled");
//    qRegisterMetaType<StructAddSystem>("StructAddSystem");
    qRegisterMetaType<StructCopyFileDirectory>("StructCopyFileDirectory");
    new CopyDir();
    return app.exec();
}
