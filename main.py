from flask import Flask
import logging
import flask
import pandas as pd
import sys

logging.basicConfig(format='[%(levelname)-5s][%(asctime)s][%(module)s:%(lineno)04d] : %(message)s',
                    level=logging.INFO,
                    stream=sys.stderr)
logger: logging.Logger = logging

super_data = [
      {"name":  "Batman", "superpower":  "intellect", "weakness":  "identity"},
      {"name":  "Spawn", "superpower":  "necroplasm", "weakness": "decapitation" },
      {"name":  "Spiderman", "superpower":  "spider-sense", "weakness":  "pesticide"}
  ]
super_df  = pd.DataFrame(super_data)
super_df.set_index(keys="name", drop=False, inplace=True)

app = Flask(__name__)
app.config["db"] = super_df

@app.route("/see_stats", methods=["GET"])
def stats():
    """
    API query to get a superhero's stats information
    """
    global super_df
