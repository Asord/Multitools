from Web import flask_app

Views = []
Services = []

def _viewDesc(route="/", name="", url="", image="", desc=""):
    return {"route": route, "name": name, "url": url, "image": image, "desc": desc}

def _serviceDesc(api_route="/api", route="/", name="", url=""):
    return {"api": api_route, "route": route, "name": name, "url": url}

def registerView(func, route, indexLinked=True, **kwargs):
    image = kwargs.pop("image", "images/default.png")
    desc = kwargs.pop("desc", "No description")
    name = kwargs.pop("name", func.__name__)

    if indexLinked:
        Views.append( _viewDesc(route, name, name, image, desc) )

    flask_app.add_url_rule(route, name, func, **kwargs)

def registerService(func, route, **kwargs):
    api_route = kwargs.pop("api_route", "/api")
    name = kwargs.pop("name", func.__name__)

    Services.append(_serviceDesc(api_route, route, name, name))
    flask_app.add_url_rule(api_route + route, name, func, **kwargs)