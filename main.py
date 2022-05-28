from flask import Flask, request
import logging
import pandas as pd
import sys


logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=logging.INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging

# creating a list of dictionaries
super_data = [
      {"name":  "Batman", "superpower":  "intellect", "weakness":  "identity"},
      {"name":  "Spawn", "superpower":  "necroplasm", "weakness": "decapitation" },
      {"name":  "Spiderman", "superpower":  "spider-sense", "weakness":  "pesticide"},
      {"name":  "Bruce Wayne", "superpower":  "intellect", "weakness":  "identity"}
  ]
# Converting list dictionary keys into columns, and key-values into column-values for a dataframe
super_df  = pd.DataFrame(super_data)
# Setting the name column as the index
super_df.set_index(keys="name", drop=False, inplace=True)

# instantiate my API to use
app = Flask(__name__)
app.config["db"] = super_df

# creating an endpoint to bind to the API
@app.route("/see_stats", methods=["GET"])
def stats():
    """
    API GET query to get a superhero's stats information
    """
    global super_df
    # Creating queries "name", "superpower", and "weakness" for the API to request and assigning them to variables
    name = request.args.get("name", default=None)
    superpower = request.args.get("superpower", default=None)
    weakness = request.args.get("weakness", default=None)

    # if "name" query is given look for a superhero with a matching key-value pair 
    if (name is not None):
        # variable "result_df" is assigned to the row with a matching name index in the "super_df"
        result_df = super_df.loc[super_df["name"] == name]
        logger.info(f"Querying superhero with name: {name}")
        # gives user a json response with the query they entered and converts result_df is converted to a list of dicts
        resp_json = {
            "query": name,
            "response": result_df.to_dict(orient="records")
        }
        # Telling the API to expect header in json
        resp_headers = {"content-type": "application/json"}
        # "200" is added as a status to tell the user that the request was successful
        return resp_json, 200, resp_headers

    # looking for any superheroes with a matching superpower and weakness
    elif (superpower is not None) and (weakness is not None):
        result_df = super_df.loc[super_df["superpower"] == superpower]
        # pandas' Dataframe method ".query" can check for multiple matching column values in a dataframe
        # creates returned columns in "result_df" if the superpower column is equal to superpower query and weakness column is also equal to weakness query
        result_df = super_df.query("superpower == @superpower and weakness == @weakness")
        # Logger tells what was queried
        logger.info(f"Querying superheroes with superpower: {superpower} and weakness: {weakness}")
        resp_json = {
          "query": f"superpower: {superpower}, weakness: {weakness}",
          "response": result_df.to_dict(orient="records")
          }
        resp_headers = {"content-type":"application/json"}
        return resp_json, 200, resp_headers

    elif superpower is not None:
        result_df = super_df.loc[super_df["superpower"] == superpower]
        logger.info(f"Querying superheroes with superpower: {superpower}")
        resp_json = {
            "query": superpower,
            "response": result_df.to_dict(orient="records")
        }
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers

    elif weakness is not None:
        result_df = super_df.loc[super_df["weakness"] == weakness]
        logger.info(f"Querying superheroes with weakness: {weakness}")
        resp_json = {
            "query": weakness,
            "response": result_df.to_dict(orient="records")
        }
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers

    else:
        result_df = super_df
        resp_json = {"query": "None, returning database", "result": result_df.to_dict(orient="records")}
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers


@app.route("/add_stats", methods=["POST"])
def add_stats():
    """
    API POST method to add a superhero to the database
    """
    global super_df

    try:
        heroes_added = []
        heroes_not_added = []
        data = request.json
        for superhero in data:
            if ("name" in superhero) and ("superpower" in superhero) and ("weakness" in superhero):
                logger.info(f"Adding superhero: {superhero}")
                super_df.loc[superhero["name"]] = superhero
                heroes_added.append(superhero)
            else:
                logger.info(f"Superhero: {superhero} cannot be added")
                heroes_not_added.append(superhero)
        logger.info(f"Added: {len(heroes_added)}, Not added: {len(heroes_not_added)}")

        resp_json = {f"Heroes added": f"{len(heroes_added)}, {heroes_added}",
        "Not added": f"{len(heroes_not_added)}, {heroes_not_added}"}
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers
    except Exception as err:
        return {"status": "error", "error_msg": str(err)}, 400, {"content-type": "application/json"}


if __name__ == "__main__":
    app.run("0.0.0.0", 5050)