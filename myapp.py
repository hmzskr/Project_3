import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

import json
app = Flask(__name__)

@app.route("/map", methods=["GET", "POST"])
def send():
    
    map_df=pd.read_csv("map_info.csv")
    
    session['name_list'] = list(map_df.Name)
    session['review_list'] = list(map_df.Review_Count)
    session['category_list'] = list(map_df.Categories_All)
    session['rating_list'] = list(map_df.Rating)
    session['latitude_list'] = list(map_df.Latitude)
    session['longitude_list'] = list(map_df.Longitude)
    session['price_list'] = list(map_df.Price)
    session['address_list'] = list(map_df.Address)
    session['city_list'] = list(map_df.City)
    session['zip_list'] = list(map_df.Zip_Code)
    session['state_list'] = list(map_df.State)
    
    return render_template('indexM.html',
    names=json.dumps(session['name_list']),
    reviews=json.dumps(session['review_list']),
    categories=json.dumps(session['category_list']),
    ratings=json.dumps(session['rating_list']),
    latitude=json.dumps(session['latitude_list']),
    longitude=json.dumps(session['longitude_list']),
    price=json.dumps(session['price_list']),
    address=json.dumps(session['address_list']),
    city=json.dumps(session['city_list']),
    zip_code=json.dumps(session['zip_list']),
    state=json.dumps(session['state_list'])
    )
	
@app.after_request
def add_header(response):
   response.cache_control.no_store = True
   return response
   
if __name__ == '__main__':
	app.run(debug=True)
