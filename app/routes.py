from app import app
from flask import render_template, redirect
from flask import url_for, request

from app.datasets.datasets_methods import get_events_in_radius

##########
# ROUTES #
##########

# Homepage (for searching a location) ######################
@app.route("/", methods=["GET","POST"])
def index():


    return render_template("homepage.html")

# Visualisation (for  a location) ##########################
@app.route("/location/", methods=["GET","POST"])
def location():
    # Get the coordinates indicated by the user
    if request.args.get("lat", None) and request.args.get("long", None):
        coord = (request.args["lat"],request.args["long"])

        # Get all the events in the radius of a location 
        events = get_events_in_radius(coord,50)
        nb_earthquakes = len(events["earthquakes"])
        nb_volcanos = len(events["volcanos"])
        nb_tsunamis = len(events["tsunamis"])

        #info contains the sum of the damage("damageMillionsDollars", "deaths", "damageAmountOrder",
        # "deathsAmountOrder", "deathsAmountOrder", "housesDestroyedAmountOrder")
        info = dict()

        for event_type, event in events.items():
            for i in event:
                for title, containt in i.items():
                    if title in ["damages", "deaths", "housesDamaged", "injuries"]:
                        if title in info:
                            info[title] = info[title] + int(containt)
                        else:
                            info[title] = int(containt)

        return render_template("location.html", summary=[nb_volcanos, nb_earthquakes, nb_tsunamis], events=events, info=info, coord=coord)

    return redirect(url_for("index"))

# Visualisation (for comparison) ##########################
@app.route("/comparaison/", methods=["GET","POST"])
def comparaison():
     # Get the coordinates indicated by the user
    if request.args.get("lat", None) and request.args.get("long", None) and request.args.get("lat2", None) and request.args.get("long2", None):
        coord = (request.args["lat"],request.args["long"])
        coord2 = (request.args["lat2"],request.args["long2"])

        # Get all the events in the radius of the 1st location
        events = get_events_in_radius(coord,50)
        nb_earthquakes = len(events["earthquakes"])
        nb_volcanos = len(events["volcanos"])
        nb_tsunamis = len(events["tsunamis"])

        # Get all the events in the radius of the 2nd location
        events2 = get_events_in_radius(coord2,50)
        nb_earthquakes2 = len(events2["earthquakes"])
        nb_volcanos2 = len(events2["volcanos"])
        nb_tsunamis2 = len(events2["tsunamis"])

        return render_template("comparaison.html",summary=[nb_volcanos,nb_earthquakes,nb_tsunamis,nb_volcanos2,nb_earthquakes2,nb_tsunamis2],events = [events,events2], coord=[coord,coord2])

    return redirect(url_for("index"))

#######
# RUN #
#######
if __name__ == "__main__":
        app.run()