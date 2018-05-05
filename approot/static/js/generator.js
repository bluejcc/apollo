MIDI.loadPlugin({
    instrument: "acoustic_grand_piano", // or the instrument code 1 (aka the default)
    instruments: [ "acoustic_grand_piano", "acoustic_guitar_nylon" ], // or multiple instruments
    onsuccess: function() {}
});

$(function () {
    // $("#chords").on("input",function(e){
    //     if($(this).val() != ""){
    //         $("#btn_go").removeAttr("disabled");
    //     } else {
    //         $("#btn_go").attr("disabled", "disabled");
    //     }
    // });
    $("#btn_go").click(function () {
        mid_url = "generate/mid?chords=" + $("#chords").val().replace(" ", "+");
        MIDI.Player.loadFile(mid_url);
    });

});
