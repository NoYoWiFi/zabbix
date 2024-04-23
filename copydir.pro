QT += quick widgets

SOURCES += \
        copydir.cpp \
        copydirthread.cpp \
        main.cpp

resources.prefix = /$${TARGET}
RESOURCES += \
    images.qrc \
    qmls.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Additional import path used to resolve QML modules just for Qt Quick Designer
QML_DESIGNER_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    copydir.h \
    copydirthread.h

INCLUDEPATH +=$$PWD localMethod
include(localMethod/localMethod.pri)
