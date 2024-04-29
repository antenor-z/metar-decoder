from flask import Flask, render_template, redirect, request
from DB.Getter import get_all_names, get_info
from metarExt import IcaoError, get_metar
from metarDecoder import DecodeError, decode, get_wind_info
from wind.Wind import get_components, get_components_one_runway, get_wind
app = Flask(__name__)

@app.get("/")
def list_all():
    return render_template("index.html", airports=get_all_names())

@app.get("/info/<string:icao>")
def info(icao:str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return redirect(f"/info/{icao_upper}")
    
    try:
        metar = get_metar(icao)
    except IcaoError as e:
        return render_template("error.html", error=e), 400
    
    try:
        info = get_info(icao)
    except ValueError as e:
        return render_template("error.html", error=e), 400

    decoded = decode(metar)

    return render_template("airport.html", info=info, icao=icao, metar=metar, decoded=decoded)


@app.get("/wind/")
def wind():
    return render_template("wind.html")


@app.get("/windcalc/")
def windcalc():
    try:
        runway_head = int(request.args["runway_head"])
        wind_dir = int(request.args["wind_dir"])
        wind_speed = int(request.args["wind_speed"])
    except KeyError:
        return {"error": "mising args"}, 400
    except ValueError:
        return {"error": "invalid args"}, 400

    ret = get_components_one_runway(
        runway_head=runway_head,
        wind_dir=wind_dir,
        wind_speed=wind_speed)
    return ret


@app.get("/descent")
def descent():
    return render_template("vertical.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="404 | Página não encontrada."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
