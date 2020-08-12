from Libraries.AsemcoAPI.Tools.Services import registerView, registerService, Views
from flask import render_template, request, jsonify
from json import loads, dump, load
from requests import post
from requests.exceptions import ConnectionError

from App.Ambibox import effectParser, SettingsLineParser, serializeLedsConfig
from Settings.ambibox import *

def AmbiboxConfig():
    Saves = AmbiboxLoad()

    return render_template("ambibox.html", views=Views, saves=Saves)

def AmbiboxReceiveConfig():
    if request.method == "POST":
        effect = loads(request.form["config"])
        save = effect.pop("save", True)

        baseConfig, ledsColors, spec, warn = effectParser.effectConfigParser(effect)

        if warn != "":
            return warn

        NumberOfLeds = len(ledsColors)

        LedsConfigs = []
        for LedID in range(NumberOfLeds):
            LedConfig = SettingsLineParser()
            LedConfig.clearAllColors()
            nbColors = len(ledsColors[LedID])
            LedConfig.setNbColors(nbColors)
            for colorID in range(nbColors):
                LedConfig.setColor(colorID, ledsColors[LedID][colorID])

            LedConfig.setSpectrum(spec[LedID])
            LedsConfigs.append(LedConfig)

        formatedConfig = serializeLedsConfig(LedsConfigs)

        with open(ColormusicSettingsFile, "w") as fs:
            fs.write(baseConfig)
            fs.write(formatedConfig)

        try:
            res = post("http://localhost:8088/", data={"status": "off"})
            if res.status_code == 200:
                post("http://localhost:8088/", data={"status": "on"})
        except ConnectionError as ce:
            print(ce)

        if save:
            saves = AmbiboxLoad()
            newID = len(saves)
            saves.append({"id": newID, "save": effect})
            AmbiboxSave(saves)


        return "ok"

    return "error"

def AmbiboxEffects():
    if request.method == "GET":
        _id = int(request.values.get("id"))
        saves = AmbiboxLoad()
        for save in saves:
            if save["id"] == _id:
                return jsonify(save["save"])

        return "404"
    return "405"



registerService(AmbiboxEffects, "/effects", name="ambibox_effects", api_route="/ambibox-api", methods=["GET"])
registerView(AmbiboxConfig, "/ambibox", name="Ambibox", desc="Ambibox Led Visualizer configurator", image="images/ambibox.png")
registerService(AmbiboxReceiveConfig, "/config", name="ambibox_config", api_route="/ambibox-api", methods=["POST"])
