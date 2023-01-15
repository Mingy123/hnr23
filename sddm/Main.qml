import QtQuick 2.9
import QtWebEngine 1.0
import SddmComponents 2.0

Rectangle {
    id: root
    color: "#333f48"
    width: 1920; height: 1080
    property real ratio: 1080/1920
    property real eWidth: {
        if (height/width > ratio) return width
        return height/ratio
    } property real eHeight: ratio*eWidth
    property real eScale: eWidth/1920
    property bool unlock: false
    property bool almost: false
    property var date: new Date()
    Timer {
        id: ai_timer
        repeat: true
        interval: 1000
        running: true
        onTriggered: {
          var req = new XMLHttpRequest();
          req.open("GET", "http://localhost:5000/jumping");
          req.onreadystatechange = function() {
            if (req.readyState == XMLHttpRequest.DONE) {
              if (req.responseText == '2') unlock = true
              else if (req.response == '1') almost = true
              else almost = false
            }
          } req.send()
        }
    }

    Item {
        id: virt
        height: eHeight
        width: eWidth
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    Image {
        id: iwantyou
        source: "assets/iwantyou.png"
        height: eHeight * 0.9
        width: height * sourceSize.width / sourceSize.height
        anchors {
            verticalCenter: virt.verticalCenter
            left: virt.left
            leftMargin: eWidth * 0.05
        }
    }

    Rectangle {
        id: webcam_frame
        color: clock.color
        width: webcam.width + (10 * eScale)
        height: webcam.height + (10 * eScale)
        anchors.centerIn: webcam
    }

    WebEngineView {
        id: webcam
        url: "http://127.0.0.1:5000/video_feed"
        width: 640 * eScale
        height: 480 * eScale
        anchors {
            top: virt.top
            right: virt.right
            topMargin: eHeight * 0.15
            rightMargin: eWidth * 0.12
        }
    }

    Text {
        id: clock
        anchors {
            horizontalCenter: webcam.horizontalCenter
            top: virt.top
            topMargin: eHeight * 0.03
        }
        text: {
            if (unlock) return "Unlocked!"
            else if (almost) return "Almost!"
            return pad(date.getHours(), 2) + ":" + pad(date.getMinutes(), 2)
        }
        color: {
            if (unlock) return "#00ff00"
            else if (almost) return "#FFD700"
            else return "white"
        }
        font.pointSize: 48
        scale: eScale
    }

    Item {
        id: login_box
        height: eHeight * 0.25
        width: eWidth * 0.4
        anchors {
            horizontalCenter: webcam.horizontalCenter
            bottom: virt.bottom
            bottomMargin: eHeight * 0.1
        }

        Image {
            id: user_icon
            width: height
            anchors {
                top: parent.top
                bottom: parent.bottom
                left: parent.left
                margins: eWidth * 0.02
            }
        }

        TextBox {
            enabled: unlock
            id: username_box
            font.pointSize: 24
            anchors {
                bottom: parent.verticalCenter
                bottomMargin: eHeight * 0.01
                right: parent.right
                rightMargin: eWidth * 0.03
            }
            height: eHeight * 0.07
            width: eWidth * 0.22
            text: userModel.lastUser
            color: unlock ? "#30000000" : "#10000000"
            hoverColor: unlock ? "#00a499" : "transparent"
            borderColor: "transparent"
            textColor: "white"
        }

        PasswordBox {
            enabled: unlock
            id: password_box
            anchors {
                top: parent.verticalCenter
                topMargin: eHeight * 0.01
                right: parent.right
                rightMargin: eWidth * 0.03
            }
            height: eHeight * 0.07
            width: eWidth * 0.22
            color: unlock ? "#30000000" : "#10000000"
            borderColor: "transparent"
            hoverColor: unlock ? "#00a499" : "transparent"
            textColor: "white"
        }

        Keys.onPressed: (kev) => {
            if (!unlock || !username_box.text || !password_box.text) return;
            if (kev.key == Qt.Key_Enter || kev.key == Qt.Key_Return) {
                sddm.login(username_box.text, password_box.text, session.index)
            }
        }
    }

    Connections {
        target: sddm
        onLoginFailed: unlock = false
        onLoginSucceeded: {
          var req = new XMLHttpRequest();
          req.open("POST", "http://localhost:5000/log/in");
          req.send()
        }
    }

    // copied from https://github.com/3ximus/aerial-sddm-theme
    Rectangle {
        id: actionBar
        width: eWidth
        height: eHeight * 0.04
        anchors.top: virt.top;
        anchors.horizontalCenter: parent.horizontalCenter
        visible: config.showTopBar != "false"
        color: "transparent"

        Row {
            id: row_left
            anchors.left: parent.left
            anchors.margins: 1
            height: parent.height
            spacing: 10
            ComboBox {
                id: session
                width: eWidth * 0.06
                height: parent.height - 2
                anchors.verticalCenter: parent.verticalCenter
                color: "transparent"
                arrowColor: "transparent"
                textColor: "#00a499"
                borderColor: "transparent"
                hoverColor: "#5692c4"
                model: sessionModel
                index: sessionModel.lastIndex
            }
        }

        Row {
            id: row_right
            height: parent.height
            anchors.right: parent.right
            anchors.margins: 5
            spacing: 10

            ImageButton {
                id: reboot_button
                height: parent.height
                source: "assets/reboot.svg"
                visible: sddm.canReboot
                onClicked: sddm.reboot()
            }

            ImageButton {
                id: shutdown_button
                height: parent.height
                source: "assets/shutdown.svg"
                visible: sddm.canPowerOff
                onClicked: sddm.powerOff()
            }
        }
    }

    function pad(num, pad) {
        return num.toString().padStart(pad, "0");
    }

    Repeater {
        id: users
        model: userModel
        delegate: Text {
            property url icon: model.icon
        }
        Component.onCompleted: {
            user_icon.source = itemAt(0).icon
        }
    }
}
