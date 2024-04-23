import QtQuick
import QtQuick.Window
import QtQuick.Controls
import Qt.labs.platform

Window {
    property url statusBackgroud: "qrc:/images/background.png"
    property string gv_strFromDirPath: ""
    property string gv_strToDirPath: ""
    property string gv_readyReadStandard: ""
    property string gv_strCurrentOSVersion: ""
    property string gv_strInstallModel: "M"
    property bool gv_boolM: true
    property bool gv_boolG: false
    property bool gv_boolEnable: true
    property int gv_intAllFileCount: 0
    property int gv_intCurrentFileCount: 0
    property string gv_strOSType: ""
    property string gv_strOSName: ""
    property string gv_strOSVersion: ""
    property bool gv_boolEntered: false

    signal signal_onCopyDirClose()
    signal signal_button_1Browse_onClicked()
    signal signal_button_3Deploy_onClicked()
    signal signal_button_4Cancel_onClicked()

    onVisibleChanged: {
        if(root.visible == true)
        {
            root.x = Screen.width / 2 - width / 2
            root.y = Screen.height / 2 - height / 2
        }
        else
        {
            signal_onCopyDirClose()
            gv_boolEnable = true
        }
    }
    id: root
    width:600; height:300
    maximumWidth: 600; maximumHeight: 300
    minimumWidth: 600; minimumHeight: 300
    visible: true
    color: "#ffffff"
    title: qsTr("发布系统")
    modality: Qt.ApplicationModal
    flags: Qt.MSWindowsFixedSizeDialogHint

    Image {
        id: image_1
        z: -1
        anchors.fill: parent
        source: root.statusBackgroud
        fillMode: Image.PreserveAspectCrop
    }

    Rectangle {
        id: rectangle_1
        x: 8
        width: 585
        height: 40
        color: "#808080"
        radius: 13
        anchors.top: parent.top
        anchors.horizontalCenterOffset: 0
        anchors.topMargin: 32
        border.color: "#808080"
        anchors.horizontalCenter: parent.horizontalCenter

        Label {
            id: label_1
            height: 35
            text: "源文件夹"
            font.pixelSize: 18
            anchors.left: parent.left
            anchors.leftMargin: 10
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.verticalCenter: parent.verticalCenter
        }

        Rectangle {
            id: rectangle_2
            y: 0
            width: 417
            height: 35
            color: "#00000000"
            anchors.verticalCenter: parent.verticalCenter
            border.width: 1
            border.color: "#000000"
            anchors.left: label_1.right
            anchors.leftMargin: 28
            Label {
                id: label_2
                text: root.gv_strFromDirPath
                topPadding: 2
                anchors.fill: parent
                leftPadding: 2
                padding: 2
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
            }
        }

        Button {
            id: button_1
            width: 35
            height: 35
            text: qsTr("浏览")
            enabled: root.gv_boolEnable
            anchors.left: rectangle_2.right
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter

            contentItem: Text {
                color: button_1.down ? "green" : "white"
                text: button_1.text
                anchors.fill: parent
                font: button_1.font
                opacity: enabled ? 1.0 : 0.3
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }

            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                color: button_1.down ? "white" : "green"
                border.color: button_1.down ? "green" : "white"
                border.width: 1
                radius: 2
            }

            FolderDialog {
                 id: folderDialog_3
                 folder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                 onAccepted: root.gv_strFromDirPath = folderDialog_3.folder
                 onRejected: root.gv_strFromDirPath = ""
             }
            onClicked: {
                    folderDialog_3.open()
                }
        }
    }


    Rectangle {
        id: rectangle_6
        x: 10
        width: 585
        height: 40
        color: "#808080"
        radius: 13
        anchors.top: rectangle_5.bottom
        anchors.topMargin: 30
        anchors.horizontalCenter: parent.horizontalCenter
        border.color: "#808080"
        Label {
            id: label_5
            height: 35
            text: "进度"
            horizontalAlignment: Text.AlignHCenter
            anchors.verticalCenter: parent.verticalCenter
            verticalAlignment: Text.AlignVCenter
            anchors.leftMargin: 10
            font.pixelSize: 18
            anchors.left: parent.left
        }

        Rectangle {
            id: rectangle_7
            width: 470
            height: 35
            color: "#00000000"
            anchors.verticalCenter: parent.verticalCenter
            border.width: 1
            border.color: "#000000"
            anchors.leftMargin: 10
            TextArea {
                id: textArea_6
                text: root.gv_readyReadStandard
                readOnly: true
                horizontalAlignment: Text.AlignLeft
                padding: 2
                verticalAlignment: Text.AlignVCenter
                anchors.fill: parent
                leftPadding: 2
                topPadding: 2
            }
            anchors.left: label_5.right
        }

        Button {
            onClicked: signal_button_3Deploy_onClicked()
            id: button_3
            width: 35
            height: 35
            text: qsTr("发布")
            enabled: root.gv_boolEnable
            contentItem: Text {
                color: button_3.down ? "green" : "white"
                text: "拷贝"
                horizontalAlignment: Text.AlignHCenter
                opacity: enabled ? 1.0 : 0.3
                verticalAlignment: Text.AlignVCenter
                anchors.fill: parent
                elide: Text.ElideRight
                font: button_3.font
            }
            anchors.verticalCenter: parent.verticalCenter
            anchors.leftMargin: 10
            FileDialog {
                id: fileDialog_2
                folder: "file:///opt/"
                nameFilters: ["iso文件 (*.iso)"]
                title: qsTr("选择iso镜像系统文件")
            }
            background: Rectangle {
                color: button_3.down ? "white" : "green"
                radius: 2
                opacity: enabled ? 1 : 0.3
                implicitWidth: 100
                border.width: 1
                border.color: button_3.down ? "green" : "white"
                implicitHeight: 40
            }
            anchors.left: rectangle_7.right
        }
    }

    Rectangle {
        id: rectangle_8
        x: 19
        width: 585
        height: 40
        color: "#808080"
        radius: 13
        anchors.top: rectangle_6.bottom
        anchors.topMargin: 30
        anchors.horizontalCenter: parent.horizontalCenter
        border.color: "#808080"
        ProgressBar {
            id: progressBar_1
            width: 580
            height: 15
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            value: root.gv_intCurrentFileCount
            to: root.gv_intAllFileCount
            padding: 2

            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 6
                color: "#e6e6e6"
                radius: 3
            }

            contentItem: Item {
                width: 580
                implicitWidth: 200
                implicitHeight: 4

                Rectangle {
                    width: progressBar_1.visualPosition * parent.width
                    height: parent.height
                    radius: 2
                    border.width: 0
                    color: "#17a81a"
                }
            }
        }
    }

    Rectangle {
        id: rectangle_5
        x: 8
        width: 585
        height: 40
        color: "#808080"
        radius: 13
        border.color: "#808080"
        anchors.top: rectangle_1.bottom
        anchors.horizontalCenterOffset: 0
        anchors.topMargin: 15
        anchors.horizontalCenter: parent.horizontalCenter
        Label {
            id: label_6
            height: 35
            text: "目的文件夹"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.leftMargin: 10
        }

        Rectangle {
            id: rectangle_9
            y: 0
            width: 417
            height: 35
            color: "#00000000"
            border.color: "#000000"
            border.width: 1
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: label_6.right
            anchors.leftMargin: 10
            Label {
                id: label_7
                text: root.gv_strToDirPath
                anchors.fill: parent
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                leftPadding: 2
                padding: 2
                topPadding: 2
            }
        }

        Button {
            id: button_5
            width: 35
            height: 35
            text: qsTr("浏览")
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: rectangle_9.right
            background: Rectangle {
                opacity: enabled ? 1 : 0.3
                color: button_5.down ? "white" : "green"
                radius: 2
                border.color: button_5.down ? "green" : "white"
                border.width: 1
                implicitWidth: 100
                implicitHeight: 40
            }
            anchors.leftMargin: 10
            contentItem: Text {
                opacity: enabled ? 1.0 : 0.3
                color: button_5.down ? "green" : "white"
                text: button_5.text
                elide: Text.ElideRight
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: button_5.font
            }
            enabled: root.gv_boolEnable
            FolderDialog {
                 id: folderDialog_4
                 folder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                 onAccepted: root.gv_strToDirPath = folderDialog_4.folder
                 onRejected: root.gv_strToDirPath = ""
             }
            onClicked: {
                    folderDialog_4.open()
                }
        }
    }
}
