# app.py
from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
import requests
import time

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/citytest', methods=['GET', 'POST'])
def citytest():
    response = request.get_json()
    for i in response:
        city = response[i]
        print(city)  

    pd.options.display.max_rows = 999
    pd.options.display.max_columns = 999

    start_time = time.time()

    ykey = "Ii7Pa9IZug_H12vEjc6Z8Q7PVKDIkFXZDYLKJR9xdtTWkgw75dqoWkhpaHQ__jFcmvrmytLdF3plPxFDfw6cJqe5ugr-HOUirTiSPMFI7aYZ1W9mvifY2AJY7Sk5XXYx"

    yelp_url = 'https://api.yelp.com/v3/businesses/search'
    yelp_headers = {'Authorization': 'Bearer %s' % ykey}

    # Columns of DataFrame

    id_list = []
    name_list = []
    is_closed_list = []
    review_count_list = []
    categories_list = []
    rating_list = []
    latitude_list = []
    longitude_list = []
    price_list = []
    address_list = []
    city_list = []
    zip_code_list = []
    state_list = []
    categories_all_list = []

    restaurant_count = 0

    for offset in range(0, 1000, 20):
    # print(f'Retrieving restaurants in {city}')
        yelp_params = {'location': city, 'term': 'restaurants', 'limit': '20', 'offset': offset}
        yelp_response = requests.get(yelp_url, yelp_params, headers = yelp_headers)
        yelp_data = yelp_response.json()
    # print(yelp_data)
        restaurant_data = yelp_data['businesses']

        for restaurant in restaurant_data:
            categories_all_list_sub = []
            for category in restaurant['categories']: 
                categories_all_list_sub.append(category['title'])
            
            for category in restaurant['categories']: 
                id_list.append(restaurant['id'])         
                name_list.append(restaurant['name'])
                is_closed_list.append(restaurant['is_closed'])
                review_count_list.append(restaurant['review_count'])
                categories_list.append(category['title'])
                rating_list.append(restaurant['rating'])
                latitude_list.append(restaurant['coordinates']['latitude'])
                longitude_list.append(restaurant['coordinates']['longitude'])
                address_list.append(restaurant['location']['address1'])
                city_list.append(restaurant['location']['city'])
                zip_code_list.append(restaurant['location']['zip_code'])
                state_list.append(restaurant['location']['state'])
                
                categories_all_list.append(', '.join(categories_all_list_sub))

                try:                
                    price_list.append(restaurant['price'])

                except:
                    price_list.append('')

            restaurant_count += 1
            print(f'Restaurant #{restaurant_count} data retrieved.')
            
                
    print("--- %s seconds ---" % (time.time() - start_time))
    new_cat_list = list(set(categories_list))
    new_zip_list = list(set(zip_code_list))
    print("Number of items in list: ", len(new_cat_list))
    print(price_list)

    return jsonify(new_cat_list, new_zip_list)

@app.route('/useroptions', methods=['GET', 'POST'])
def useroptions():
    response = request.get_json()
    print(response)
    options=response[0]
    for i in options:
        print(i)
    return jsonify(response)
        
@app.route('/')
def index():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == "__main__":
     app.run(debug=True)