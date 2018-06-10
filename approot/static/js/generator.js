var midiUpdate = function(time) {
    console.log(time);
}
var midiStop = function() {
    $("#btn_play").removeAttr("disabled");
}

$(function () {
    var midiOutput = "";

    $("#btn_go").click(function () {
        if ($("#btn_play").prop("disabled")) {
            $("#btn_play").removeAttr("disabled");
            $("#player").midiPlayer.stop();
        }
        $("#result").show();
        $(".well_head").show();
        let chords = $("#chords").val();
        if (!chords || chords.length == 0) {
            chords = "G D Em C G";
        }
        chords = chords.replace(/ /g, "+");

        var VexDocument = null;
        var VexFormatter = null;
        $.ajax({
            url: "generate/musicxml?chords=" + chords,
            success: function(data) {
                var start = new Date().getTime(); // time execution
                VexDocument = new Vex.Flow.Document(data);
                var content = $(".music_xml_viewer")[0];
                if (VexDocument) {
                    VexFormatter = VexDocument.getFormatter();
                    VexFormatter.draw(content);
                }
                var elapsed = (new Date().getTime() - start)/1000;
                var debouncedResize = null;
                $(window).resize(function() {
                    if (! debouncedResize)
                        debouncedResize = setTimeout(function() {
                            VexFormatter.draw(content);
                            debouncedResize = null;
                        }, 500);
                });
            }
        });
        mid_url = "generate/mid?chords=" + chords + "&t=" + Date.now();

        let xhr = new XMLHttpRequest();
        xhr.open("GET", mid_url);
        xhr.overrideMimeType("text/plain; charset=x-user-defined");
        xhr.onreadystatechange = function() {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    let t = this.responseText || '';
                    let ff = []
                    let mx = t.length;
                    let scc = String.fromCharCode;
					          for (let z = 0; z < mx; z++) {
						            ff[z] = scc(t.charCodeAt(z) & 255);
					          }
					          let data = ff.join('');
                    midiOutput = "data:audio/midi;base64," + window.btoa(data);
                    $("#player").midiPlayer.play(t);
                }
            }
        };
        xhr.send();
    });

    $("#btn_play").click(function() {
        $(this).attr("disabled","disabled");
        $("#player").midiPlayer.play(midiOutput);
    });

    $("#player").midiPlayer({
        color: "#FF5600",
        //onUpdate: midiUpdate,
        onStop: midiStop,
        width: 250
    });

});
