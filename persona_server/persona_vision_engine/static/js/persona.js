//import jQuery from "./jquery.min.js";
//window.$ = window.jQuery = jQuery;
// Set to true if you want to save the data even if you reload the page.
window.saveDataAcrossSessions = false;

const personaDetectorSVG = "personaDetectorSVG";
var force = [];
var nodes = [];

window.onload = async function () {

    if (!window.saveDataAcrossSessions) {
        var localstorageDataLabel = 'webgazerGlobalData';
        localforage.setItem(localstorageDataLabel, null);
        var localstorageSettingsLabel = 'webgazerGlobalSettings';
        localforage.setItem(localstorageSettingsLabel, null);
    }
    const webgazerInstance = await webgazer.setRegression('ridge') /* currently must set regression and tracker */
        .setTracker('TFFacemesh')
        .begin();
    webgazerInstance.showVideoPreview(true) /* shows all video previews */
        .showPredictionPoints(true) /* shows a square every 100 milliseconds where current prediction is */
        .applyKalmanFilter(true); // Kalman Filter defaults to on.
    // Add the SVG component on the top of everything.
    setupPersonaGazeTracker();

    webgazer.setGazeListener(collisionEyeListener);
};

window.onbeforeunload = function () {
    if (window.saveDataAcrossSessions) {
        webgazer.end();
    } else {
        localforage.clear();
    }
}

function setupPersonaGazeTracker() {
    var width = window.innerWidth;
    var height = window.innerHeight;

    var svg = d3.select("body").append("svg")
        .attr("id", personaDetectorSVG)
        .attr("width", width)
        .attr("height", height)
        .style("top", "0px")
        .style("left", "0px")
        .style("margin", "0px")
        .style("position", "absolute")
        .style("z-index", 100000);

    svg.append("line")
        .attr("id", "eyeline1")
        .attr("stroke-width", 2)
        .attr("stroke", "greenyellow");

    svg.append("line")
        .attr("id", "eyeline2")
        .attr("stroke-width", 2)
        .attr("stroke", "greenyellow");

    svg.append("rect")
        .attr("id", "predictionSquare")
        .attr("width", 5)
        .attr("height", 5)
        .attr("fill", "greenyellow");
    svg.append("rect")
        .attr("id", "faceSquare")
        .attr("width", 1)
        .attr("height", 1)
        .attr("fill", " blue");
}


var webgazerCanvas = null;

var previewWidth = webgazer.params.videoViewerWidth;



var collisionEyeListener = async function (data, clock) {
    let facing = await webgazer.isUserFacing();
    let rightEyeX = 0;
    let rightEyeY = 0;
    let leftEyeX = 0;
    let leftEyeY = 0;

    if (data) {

        //console.log("Data", data);
        if (!webgazerCanvas) {
            webgazerCanvas = webgazer.getVideoElementCanvas();
        }

        await webgazer.getTracker().getEyePatches(webgazerCanvas, webgazerCanvas.width, webgazerCanvas.height);
        var fmPositions = await webgazer.getTracker().getPositions();
        //console.log("params", webgazer.params);

        var whr = webgazer.getVideoPreviewToCameraResolutionRatio();

        /* Eyes position are copied from the webgazer example, they are hard coded in the fmPositions array, we then calculate
        the face position based on them. */
        rightEyeX = previewWidth - fmPositions[145][0] * whr[0];
        rightEyeY = fmPositions[145][1] * whr[1];
        leftEyeX = previewWidth - fmPositions[374][0] * whr[0];
        leftEyeY = fmPositions[374][1] * whr[1];

        var faceSquare = d3.select('#faceSquare')
            .attr("x", 0)
            .attr("y", 0);

        var line = d3.select('#eyeline1')
            .attr("x1", data.x)
            .attr("y1", data.y)
            .attr("x2", previewWidth - fmPositions[145][0] * whr[0])
            .attr("y2", fmPositions[145][1] * whr[1]);

        var line = d3.select("#eyeline2")
            .attr("x1", data.x)
            .attr("y1", data.y)
            .attr("x2", previewWidth - fmPositions[374][0] * whr[0])
            .attr("y2", fmPositions[374][1] * whr[1]);

        var dot = d3.select("#predictionSquare")
            .attr("x", data.x)
            .attr("y", data.y);
    } else {
        data = {"x":0, "y":0}
    }

    let packet = {
        "facing": facing,
        "right_eye": {
            "x": rightEyeX,
            "y": rightEyeY
        },
        "left_eye": {
            "x": leftEyeX,
            "y": leftEyeY
        },
        "prediction": {
            "x": data.x,
            "y": data.y
        }
    }
    console.log(facing);
    $.ajax({
        type: "POST",
        url: "https://127.0.0.1:5000/data",
        data: JSON.stringify({ "packet": packet }),
        contentType: "application/json",
        success: function (result) {
            //console.log(result);
        },
        error: function (result, status) {
            console.log(result);
        }
    });
    //await new Promise(r => setTimeout(r, 1000));
}

// sleep time expects milliseconds
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}