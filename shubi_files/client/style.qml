import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

ApplicationWindow {
    objectName: "mainObj"
    visible: false
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint

    width: 190
    height: 60

    x: Screen.desktopAvailableWidth - width - 20
    y: Screen.desktopAvailableHeight - height - 20

    title: qsTr("Imputer")
    signal textUpdated(int how_many)

    Image {
        x: 0
        y: 0
        width: 190
        height: 60
        fillMode: Image.PreserveAspectCrop
        antialiasing: true
        source: "images/small.jpg"
    }

    TextField {
        background: Rectangle {
            radius: 2
            border.color: "red"
            border.width: 3
        }
        id: textField
        x: 10
        y: 10
        width: 170
        height: 40
        font.bold: false
        focus: true

        objectName: "textField"
        z: 0

        renderType: Text.NativeRendering
        font.pointSize: 12
        smooth: true
        antialiasing: true
        property int first_time: 0
        onActiveFocusChanged: {

            if (this.first_time > 0) {

                hide()

            }
            else {

            this.first_time = this.first_time + 1
            }
        }
    }


}
