from flask import Flask, request
import logging
import pandas as pd
import sys


logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=logging.INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging

super_data = [
      {"name":  "Batman", "superpower":  "intellect", "weakness":  "identity"},
      {"name":  "Spawn", "superpower":  "necroplasm", "weakness": "decapitation" },
      {"name":  "Spiderman", "superpower":  "spider-sense", "weakness":  "pesticide"},
      {"name":  "Bruce Wayne", "superpower":  "intellect", "weakness":  "identity"}
  ]
super_df  = pd.DataFrame(super_data)
super_df.set_index(keys="name", drop=False, inplace=True)

app = Flask(__name__)
app.config["db"] = super_df

@app.route("/see_stats", methods=["GET"])
def stats():
    """
    API GET query to get a superhero's stats information
    """
    global super_df
    name = request.args.get("name", default=None)
    superpower = request.args.get("superpower", default=None)
    weakness = request.args.get("weakness", default=None)

    if (name is not None):
        result_df = super_df.loc[super_df["name"] == name]
        logger.info(f"Querying superhero with name: {name}")
        resp_json = {
            "query": name,
            "response": result_df.to_dict(orient="records")
        }
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers

    elif (superpower is not None) and (weakness is not None):
        result_df = super_df.loc[super_df["superpower"] == superpower]
        result_df = super_df.query("superpower == @superpower and weakness == @weakness")
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
    # name = request.args.get("name", default=None)
    # superpower = request.args.get("superpower", default=None)
    # weakness = request.args.get("weakness", default=None)

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
        logger.info(f"Added {len(heroes_added)}, did not add {len(heroes_not_added)}")
        resp_json = {f"Heroes added": f"{len(heroes_added)}",
        "result": heroes_added,
        "not added": heroes_not_added}
        resp_headers = {"content-type": "application/json"}
        return resp_json, 200, resp_headers
    except Exception as err:
        return {"status": "error", "error_msg": str(err)}, 400, {"content-type": "application/json"}



if __name__ == "__main__":
    app.run("0.0.0.0", 5050)