MIDI.loadPlugin({
    instrument: "acoustic_grand_piano", // or the instrument code 1 (aka the default)
    instruments: [ "acoustic_grand_piano", "acoustic_guitar_nylon" ], // or multiple instruments
    onsuccess: function() {}
});

$(function () {
    $("#btn_go").click(function () {
        $("#result").show();
        let chords = $("#chords").val();
        if (!chords || chords.length == 0) {
            chords = "G D Em C G";
        }
        chords = chords.replace(" ", "+");
        mid_url = "generate/mid?chords=" + chords;
        MIDI.Player.loadFile(mid_url);

        var VexDocument = null;
        var VexFormatter = null;
        $.ajax({
            url: "generate/musicxml?chords=" + chords,
            success: function(data) {
                var start = new Date().getTime(); // time execution
                VexDocument = new Vex.Flow.Document(data);
                //console.log(VexDocument);
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
    });

    $("#btn_play").click(function() {
        MIDI.Player.start();
    });
    $("#btn_pause").click(function() {
        MIDI.Player.pause();
    });

});
