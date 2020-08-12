let palette_ID = 0;
let effects_ID = 0;

function createNewPaletteEntry(name="white", color="#ffffff") {
    let newPalette = $(document.createElement('div')).attr('id', 'palette-' + palette_ID);
        newPalette.attr("class", "palette-block input-group");

        newPalette.after().html('' +
            '<input type="text" class="form-control palette-name" aria-describedby="palette" value='+name+'>' +
            '<input type="text" class="form-control palette-color" aria-describedby="palette" value='+color+'>' +
            '<button class="remove-dynamicaly">X</button>')

        newPalette.appendTo("#palette");

        let ret = palette_ID;
        palette_ID++;

        return ret;
}

function createNewEffectEntry(type="Curve", length=16,
                              spec_start=1, spec_stop=16, spec_step=1,
                              data={})
{
    let newEffectTab = $(document.createElement("li")).attr("class", "nav-item");
        newEffectTab.attr("id", 'nav-item-effect-'+effects_ID);

        let newEffect = $(document.createElement('div')).attr('id', 'effect-' + effects_ID);

        if (effects_ID === 0) {
            newEffectTab.html('<a class="nav-link active" href="#effect-'+effects_ID+'">N° '+effects_ID+'</a>');
            newEffect.attr("class", "tab-pane active ambibox-effect"); newEffect.attr("role", "tabpanel");
        } else {
            newEffectTab.html('<a class="nav-link" href="#effect-'+effects_ID+'">N° '+effects_ID+'</a>');
            newEffect.attr("class", "tab-pane ambibox-effect"); newEffect.attr("role", "tabpanel");
        }

        newEffectTab.appendTo("#effects-tabs");

        newEffect.after().html( '' +
            '<label for="effect-type">Type</label>' +
            '<select name="effect-type" class="form-control effect-type">' +
                '<option>Color</option>' +
                '<option>Colors</option>' +
                '<option>Curve</option>' +
                '<option>Rainbow</option>' +
                '<option>Shades</option>' +
            '</select>' +

            '<label for="effect-length">Number of leds</label>' +
            '<input type="number" class="form-control effect-length" value='+length+'>' +

            '<div class="effect-config"></div>' +

            '<h4>Spectrum:</h4>' +
            '<div class="effect-spectrum">' +
                '<label for="spectrum-type">Spectrum type</label>' +
                '<select class="form-control spectrum-type">' +
                    '<option>automatic</option>' +
                    //'<option>manual</option>' +
                '</select>' +

                '<label>Start Stop Step</label>' +
                '<input type="number" class="form-control spectrum-start" value='+spec_start+'>' +
                '<input type="number" class="form-control spectrum-stop" value='+spec_stop+'>' +
                '<input type="number" class="form-control spectrum-step" value='+spec_step+'>' +
            '</div>' +

            '<button class="remove-dynamicaly">X</button>')


        newEffect.appendTo("#ambibox-leds-effect");

        $('[name=effect-type] option').filter(function() {
            return ($(this).text() === type);
        }).prop('selected', true);

        let effectconfig = newEffect.find(".effect-config");
        onEffectTypeChanged(effectconfig, type, data);

        let ret = effects_ID;
        effects_ID++;

        return ret;
}

function onEffectTypeChanged(effectconfig, type, input_data) {
    let html = "";

    let data_default = {
        "color": "white",
        "colors": ["white"],
        "clockwise": 'on',
        "red": 200,
        "green": 60,
        "blue": 20,
        "start": "red",
        "end": "blue"
    }

    let data = data_default;

    if (input_data !== undefined)
    {
        data = Object.assign(data_default, input_data)
    }
    
    switch(type) {
        case "Color":
            html = '' +
                '<label for="effect-color">Color</label>' +
                '<input type="text" class="form-control effect-color" value="'+data["color"]+'">';
            break;
        case "Colors":
            html = '' +
                '<label for="effect-colors">Colors</label>' +
                '<div class="input-group effect-colors">'
                    for (let i=0; i < 10; i++) {
                        if (i < data["colors"].length && data["colors"][i] !== "")
                            html += '<input type="text" class="form-control effect-colors-color" value="'+data["colors"][i]+'">'
                        else
                            html += '<input type="text" class="form-control effect-colors-color" value="">'
                    }
            html += '</div>'
            break;
        case "Curve":
            html = '' +
                '<label for="effect-rgb">Red Green Blue coefs</label>' +
                '<div id="" class="input-group effect-rgb">' +
                    '<input type="number" class="form-control effect-red"   value="'+data["red"]  +'">' +
                    '<input type="number" class="form-control effect-green" value="'+data["green"]+'">' +
                    '<input type="number" class="form-control effect-blue"  value="'+data["blue"] +'">' +
                '</div>' +

                '<div class="form-check clockwise">'
                    if(data["clockwise"] === 'on')
                        html += '<input type="checkbox" class="form-check-input effect-clockwise" checked>'
                    else
                        html += '<input type="checkbox" class="form-check-input effect-clockwise">'

                    html += '' +
                    '<label class="form-check-label" for=effect-clockwise">Generate Clockwise</label>' +
                '</div>';
            break;
        case "Rainbow":
        case "Shades":
            html = '' +
                '<label for="effect-limits">Start color and End color</label>' +
                '<div class="input-group effect-limits">' +
                    '<input type="text" class="form-control effect-start" value="'+data["start"]  +'">' +
                    '<input type="text" class="form-control effect-end" value="'+data["end"]  +'">' +
                '</div>' +

                '<div class="form-check clockwise">'
                    if(data["clockwise"] === 'on')
                        html += '<input type="checkbox" class="form-check-input effect-clockwise" checked>'
                    else
                        html += '<input type="checkbox" class="form-check-input effect-clockwise">'

                    html += '' +
                    '<label class="form-check-label" for=effect-clockwise">Generate Clockwise</label>' +
                '</div>';
            break;
    }

    effectconfig.html(html)
}

function LoadFromSave(save) {
    if (save === "405") return;

    let settings = save["settings"]
    let palette = save["palette"]
    let effects = save["effects"]["leds"]

    // TODO: change settings values dynamically

    for(let key in palette) {
        if (palette.hasOwnProperty(key))
            createNewPaletteEntry(key, palette[key])
    }

    effects.forEach(function(item, i) {
        let spectrumValues = item["spectrum"]["values"];
        createNewEffectEntry(
            item["type"], item["length"],
            spectrumValues["start"], spectrumValues["stop"], spectrumValues["step"],
            item);
    })

}

$(document).ready(function() {

    // Create new palette couple
    $("#ambibox-palette-button").click(function () {
        createNewPaletteEntry()
        return false;
    })

    // Create new effect form
    $("#ambibox-effect-button").click(function() {
        createNewEffectEntry();
        return false;
    })

    // triggered on effect-type changes (dynamicaly create effect form)
    $("#ambibox-leds-effect").on("change", ".effect-type", function() {
        onEffectTypeChanged( $(this).val() )
        return false;
    })

    // Delete dynamically effects or palettes
    $("#ambibox-form").on("click", ".remove-dynamicaly", function(event) {
        let elem = $(this).parent().attr("id");
        if( elem.indexOf("effect") >= 0 )
        {
            $("#nav-item-"+elem).remove();
        }
        $(this).parent().get(0).remove();
        return false;
    })

    // On tab switch
     $('#ambibox-tabs a').click(function (e) {
          e.preventDefault();
          $(this).tab('show');
    })

    // On tab effect switch
    $("#effects-tabs").on("click", "a", function(e) {
          e.preventDefault();
          $(this).tab('show');
    })

    // On send button pressed (get all form values and send it using ajax)
    $("#send").click(function(e) {
        e.preventDefault();

        let save = $("#save").is(":checked");

        let settings = {
            "BandsCount": parseInt ($("#bands-count").val()),
            "Fading":     parseInt (     $("#fading").val()),
            "Tempo":      parseInt (      $("#tempo").val()),
            "AutoLevel":  $("#auto-level").is(":checked"),
        }

        let palette = {}
        $('#palette').children('.palette-block').each(function () {
            let name  = $(this).children(".palette-name" ).val()
            let color = $(this).children(".palette-color").val()

            palette[name] = color;
        })

        let effects = {
            "numberOfLeds": parseInt($("#nb-leds").val()),
            "leds": []
        }
        $("#ambibox-leds-effect").children(".ambibox-effect").each(function() {

            let spectrum = $(this).children(".effect-spectrum");
            let config   = $(this).children(".effect-config");
            let type     = $(this).children(".effect-type").val();
            let length   = $(this).children(".effect-length").val()

            let effect = {
                "type":   type,
                "length": parseInt(length),
                "spectrum": {
                    "type":      spectrum.children(".spectrum-type" ).val(),
                    "values": {
                        "start": parseInt(spectrum.children(".spectrum-start").val()),
                        "stop":  parseInt(spectrum.children(".spectrum-stop" ).val()),
                        "step":  parseInt(spectrum.children(".spectrum-step" ).val())
                    }
                }
            }

            switch(type) {
                case "Color":
                    effect["color"] = config.children(".effect-color").val();
                    break;

                case "Colors":
                    let colors = []
                    config.children(".effect-colors").children(".effect-colors-color").each(function() {
                        if ($(this).val() === "") {
                            return false;
                        }

                        colors.push( $(this).val() );
                    });
                    effect["colors"] = colors;
                    break;

                case "Curve":
                    let effectRGB = config.children(".effect-rgb");

                    effect["red"]      = parseInt( effectRGB.children(".effect-red").val());
                    effect["green"]    = parseInt( effectRGB.children(".effect-green").val());
                    effect["blue"]     = parseInt( effectRGB.children(".effect-blue").val());
                    effect["clockwise"]= parseBool(config.children(".clockwise").children(".effect-clockwise").val());
                    break;

                case "Rainbow":
                case "Shades":
                    let limits = config.children(".effect-limits");

                    effect["start"]     = limits.children(".effect-start").val();
                    effect["end"]       = limits.children(".effect-end").val();
                    effect["clockwise"] = parseBool(config.children(".clockwise").children(".effect-clockwise").val());
                    break;
            }

            effects["leds"].push(effect);
        })

        let data = {"settings": settings, "palette": palette, "effects": effects, "save": save};
        console.debug("foo");


        $.ajax({
            type: "POST",
            async: false,
            url: "/ambibox-api/config",
            data: {"config": JSON.stringify(data)},
            success: function (res) {
                if (res !== "ok")
                    alert(res);
            }
        });
    })

    $(".save-link").click(function(e) {
        e.preventDefault();

        let url = $(this).attr("href");
        let id = $(this).attr("id").split("-")[1];

        $.ajax({
            type: "GET",
            async: false,
            url: url+"?id="+id,
            success: function(res) {
                LoadFromSave(res);
            }
        })

        return false;
    });

});