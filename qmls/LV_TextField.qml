import QtQuick
import QtQuick.Controls

TextField {
    id: textField
    y: 2
    width: 145
    height: 35
    text: gv_strOSType
    enabled: gv_boolEnable
    color: "white"
    anchors.left: label_3.right
    anchors.leftMargin: 10
    readOnly: true
    background: Rectangle {
        id: regtangle_1
        implicitWidth: 200
        implicitHeight: 40
        color: textField.enabled ? "green" : "transparent"
        border.color: "white"
    }

    Canvas {
        id: canvas_1
        x: textField.width - width - textField.rightPadding
        y: textField.height / 2 - height / 2
        width: 12
        height: 8
        contextType: "2d"

        onPaint: {
            context.reset();
            context.moveTo(0, 0);
            context.lineTo(width, 0);
            context.lineTo(width / 2, height);
            context.closePath();
            context.fillStyle = gv_boolEntered ? 'white' : 'black';
            context.fill();
        }
    }

    MouseArea{
        onEntered: {
            gv_boolEntered = true;
            regtangle_1.border.color = "white";
            canvas_1.requestPaint()}
        onExited: {
            gv_boolEntered = false;
            regtangle_1.border.color = "transparent";
            canvas_1.requestPaint()}
        onClicked: (mouse)=> {
                       gv_boolEntered = true
                       regtangle_1.border.color = "white"
                       canvas_1.requestPaint()
                       if (mouse.button === Qt.LeftButton)
                       menu.popup()
                   }
        onPressAndHold: (mouse)=> {
                            if (mouse.button === Qt.RightButton && mouse.source === Qt.MouseEventNotSynthesized)
                            menu.popup()
                        }
        id: mouseArea_1
        anchors.fill: textField
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        Menu {
            id: menu

            Menu {
                id: menu_1
                title: qsTr("centos")
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "centos_6.x_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_1.title
                        gv_strOSName = menuItem_1_1.text
                        //                                console.log(gv_strOSType, gv_strOSName, )
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "centos_6.x_BIOS"
                    id: menuItem_1_1
                    implicitWidth: 145
                    implicitHeight: 35

                    contentItem: Text {
                        leftPadding: menuItem_1_1.indicator.width
                        rightPadding: menuItem_1_1.arrow.width
                        text: menuItem_1_1.text
                        font: menuItem_1_1.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_1_1.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_1_1.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "centos_7.x";
                        button_2.visible = false;
                        gv_strOSType = menu_1.title
                        gv_strOSName = menuItem_1_2.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "centos_7.x"
                    id: menuItem_1_2
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_1_2.indicator.width
                        rightPadding: menuItem_1_2.arrow.width
                        text: menuItem_1_2.text
                        font: menuItem_1_2.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_1_2.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_1_2.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "centos_8.x";
                        button_2.visible = false;
                        gv_strOSType = menu_1.title
                        gv_strOSName = menuItem_1_3.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "centos_8.x"
                    id: menuItem_1_3
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_1_3.indicator.width
                        rightPadding: menuItem_1_3.arrow.width
                        text: menuItem_1_3.text
                        font: menuItem_1_3.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_1_3.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_1_3.highlighted ? "green" : "transparent"
                    }
                }

                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 40
                    color: "#808080"
                    border.color: "green"
                    radius: 2
                }

            }

            Menu {
                id: menu_2
                title: qsTr("esxi")

                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "esxi_5.x_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_2.title
                        gv_strOSName = menuItem_2_1.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "esxi_5.x_BIOS"
                    id: menuItem_2_1
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_2_1.indicator.width
                        rightPadding: menuItem_2_1.arrow.width
                        text: menuItem_2_1.text
                        font: menuItem_2_1.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_2_1.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_2_1.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "esxi_5.x_UEFI";
                        button_2.visible = false;
                        gv_strOSType = menu_2.title
                        gv_strOSName = menuItem_2_2.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "esxi_5.x_UEFI"
                    id: menuItem_2_2
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_2_2.indicator.width
                        rightPadding: menuItem_2_2.arrow.width
                        text: menuItem_2_2.text
                        font: menuItem_2_2.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_2_2.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_2_2.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "esxi_6.x_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_2.title
                        gv_strOSName = menuItem_2_3.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "esxi_6.x_BIOS"
                    id: menuItem_2_3
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_2_3.indicator.width
                        rightPadding: menuItem_2_3.arrow.width
                        text: menuItem_2_3.text
                        font: menuItem_2_3.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_2_3.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_2_3.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "esxi_6.x_UEFI";
                        button_2.visible = false;
                        gv_strOSType = menu_2.title
                        gv_strOSName = menuItem_2_4.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "esxi_6.x_UEFI"
                    id: menuItem_2_4
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_2_4.indicator.width
                        rightPadding: menuItem_2_4.arrow.width
                        text: menuItem_2_4.text
                        font: menuItem_2_4.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_2_4.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_2_4.highlighted ? "green" : "transparent"
                    }
                }
                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 40
                    color: "#808080"
                    border.color: "green"
                    radius: 2
                }
            }

            Menu {
                id: menu_3
                title: qsTr("ubuntu")
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "ubuntu_18.x.x";
                        button_2.visible = false;
                        gv_strOSType = menu_3.title
                        gv_strOSName = menuItem_3_1.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "ubuntu_18.x.x"
                    id: menuItem_3_1
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_3_1.indicator.width
                        rightPadding: menuItem_3_1.arrow.width
                        text: menuItem_3_1.text
                        font: menuItem_3_1.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_3_1.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_3_1.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "ubuntu_20.x.x";
                        button_2.visible = false;
                        gv_strOSType = menu_3.title
                        gv_strOSName = menuItem_3_2.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "ubuntu_20.x.x"
                    id: menuItem_3_2
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_3_2.indicator.width
                        rightPadding: menuItem_3_2.arrow.width
                        text: menuItem_3_2.text
                        font: menuItem_3_2.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_3_2.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_3_2.highlighted ? "green" : "transparent"
                    }
                }

                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 40
                    color: "#808080"
                    border.color: "green"
                    radius: 2
                }
            }

            Menu {
                id: menu_4
                title: qsTr("windows")
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "win_7_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_1.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "win_7_BIOS"
                    id: menuItem_4_1
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_1.indicator.width
                        rightPadding: menuItem_4_1.arrow.width
                        text: menuItem_4_1.text
                        font: menuItem_4_1.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_1.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_1.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "win_7_UEFI";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_2.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "win_7_UEFI"
                    id: menuItem_4_2
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_2.indicator.width
                        rightPadding: menuItem_4_2.arrow.width
                        text: menuItem_4_2.text
                        font: menuItem_4_2.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_2.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_2.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "win_10_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_3.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "win_10_BIOS"
                    id: menuItem_4_3
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_3.indicator.width
                        rightPadding: menuItem_4_3.arrow.width
                        text: menuItem_4_3.text
                        font: menuItem_4_3.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_3.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_3.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "win_10_UEFI";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_4.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "win_10_UEFI"
                    id: menuItem_4_4
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_4.indicator.width
                        rightPadding: menuItem_4_4.arrow.width
                        text: menuItem_4_4.text
                        font: menuItem_4_4.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_4.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_4.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "serverStandard_2016_BIOS";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_5.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "serverStandard_2016_BIOS"
                    id: menuItem_4_5
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_5.indicator.width
                        rightPadding: menuItem_4_5.arrow.width
                        text: menuItem_4_5.text
                        font: menuItem_4_5.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_5.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_5.highlighted ? "green" : "transparent"
                    }
                }
                MenuItem {
                    onClicked: {
                        gv_strOSVersion = "serverStandard_2016_UEFI";
                        button_2.visible = false;
                        gv_strOSType = menu_4.title
                        gv_strOSName = menuItem_4_6.text
                        //                                console.log(gv_strOSType, gv_strOSName)
                        gv_boolEntered = false; regtangle_1.border.color = "transparent"; canvas_1.requestPaint()
                    }
                    text: "serverStandard_2016_UEFI"
                    id: menuItem_4_6
                    implicitWidth: 200
                    implicitHeight: 40

                    contentItem: Text {
                        leftPadding: menuItem_4_6.indicator.width
                        rightPadding: menuItem_4_6.arrow.width
                        text: menuItem_4_6.text
                        font: menuItem_4_6.font
                        opacity: enabled ? 1.0 : 0.3
                        color: menuItem_4_6.highlighted ? "white" : "black" //二级目录文字颜色
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 200
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        color: menuItem_4_6.highlighted ? "green" : "transparent"
                    }
                }
                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 40
                    color: "#808080"
                    border.color: "green"
                    radius: 2
                }
            }

            topPadding: 2
            bottomPadding: 2

            delegate: MenuItem {
                onFocusChanged: {
                    arrow.requestPaint()
                    if(gv_strOSType == "centos")
                    {
                        rectangle_5.visible = true
                    }
                    else
                    {
                        rectangle_5.visible = false
                    }
                }
                id: menuItem
                implicitWidth: 200
                implicitHeight: 40
                contentItem: Text {
                    id: text_1
                    leftPadding: menuItem.indicator.width
                    rightPadding: menuItem.arrow.width
                    text: menuItem.text
                    font: menuItem.font
                    opacity: enabled ? 1.0 : 0.3
                    color: menuItem.highlighted ? "white" : "black" //一级目录文字
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                arrow: Canvas {
                    id: arrow
                    x: parent.width - width
                    implicitWidth: 40
                    implicitHeight: 40
                    visible: menuItem.subMenu
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.fillStyle = menuItem.highlighted ? "white" : "black"
                        ctx.moveTo(15, 15)
                        ctx.lineTo(width - 15, height / 2)
                        ctx.lineTo(15, height - 15)
                        ctx.closePath()
                        ctx.fill();
                    }
                }

                background: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 40
                    opacity: enabled ? 1 : 0.3
                    color: menuItem.highlighted ? "green" : "transparent" //高亮底色绿
                }
//                MouseArea{
//                    hoverEnabled: true
//                    anchors.fill: parent
//                    onEntered: { gv_boolEntered = true; regtangle_1.border.color = "white"; canvas_1.requestPaint()}
//                }
            }

            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 40
                color: "#808080"
                border.color: "green"
                radius: 2
            }
        }


    }
}
