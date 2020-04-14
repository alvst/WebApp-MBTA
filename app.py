from flask import Flask, render_template, request


import mbta_helper

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        find = request.form["location"]
        checked = []
        boxes = ["RapidTransit", "ExpressBus-Downtown", "LocalBus"]
        for box in boxes:
            if box in request.form:
                checked.append(box)
        # print(checked)
        location = mbta_helper.find_stop_near(find, checked)
        # print(location)
        if len(location) > 1:
            return render_template(
                "mbta.html", location = location[0], accessible = location[1]
            )

        else:
            return render_template("mbta.html")
    return render_template("mbta.html")
