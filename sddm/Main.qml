import QtQuick 2.9

Item {
    function check_good() {
    }

    id: root
    width: 1920; height: 1080
    property real ratio: 1080/1920
    property real eWidth: {
        if (height/width > ratio) return width
        return height/ratio
    } property real eHeight: ratio*eWidth
    property real eScale: eWidth/1920
    property int ai_res: 0
    Timer {
        id: ai_timer
        repeat: true
        interval: 1000
        running: true
        onTriggered: {
        var req = new XMLHttpRequest();
        req.open("GET", "http://localhost:5000");
        req.onreadystatechange = function() {
          if (req.readyState == XMLHttpRequest.DONE) {
            ai_res = req.responseText
          }
        }
        req.send()
        }
    }

    Image {
        id: background
        source: "assets/background.jpg"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        height: eHeight
        width: eWidth
    }

    Text {
        text: "NUS Hackers" + ai_res
        font.pointSize: 36
        anchors.centerIn: parent
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
