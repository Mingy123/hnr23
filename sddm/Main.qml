import QtQuick 2.9
import QtWebEngine 1.0

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
    property string ai_res
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
            ai_res = req.responseText
          }
        }
        req.send()
        }
    }

    Rectangle {
        id: virt
        color: "red"
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

    WebEngineView {
        url: "http://127.0.0.1:5000/video_feed"
        width: 640
        height: 480
    }

    /*
    Repeater {
        id: users
        model: userModel
        delegate: Text {
            text: model.name
            color: "white"
            style: Text.Outline
            font.pointSize: 24
            styleColor: "black"
            anchors.top: background.top
            y: index * 100
        }
    }
    */
}
