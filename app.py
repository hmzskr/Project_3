# app.py
from flask import Flask, jsonify, request, render_template, session
import pandas as pd
import numpy as np
import requests
import time
import warnings

app = Flask(__name__)

app.secret_key = "whatever"

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
            
    # cast category & zip code lists to sets to remove duplicates for html rendering             
    new_cat_list = list(set(categories_list))
    new_zip_list = list(set(zip_code_list))

    # set lists filled by API results as session variables to call elsewhere
    session['id_list'] = id_list
    session['name_list'] = name_list
    session['is_closed_list'] = is_closed_list
    session['review_count_list'] = review_count_list
    session['categories_list'] = categories_list
    session['rating_list'] = rating_list
    session['latitude_list'] = latitude_list
    session['longitude_list'] = longitude_list
    session['price_list'] = price_list
    session['address_list'] = address_list
    session['city_list'] = city_list
    session['zip_code_list'] = zip_code_list
    session['state_list'] = state_list
    session['categories_all_list'] = categories_all_list
    session['new_cat_list'] = new_cat_list
    session['new_zip_list'] = new_zip_list

    # print API search time result
    print (session['categories_list'])
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Number of items in list: ", len(new_cat_list))
    
    return jsonify(new_cat_list, new_zip_list)

@app.route('/useroptions', methods=['GET', 'POST'])
def useroptions():

    warnings.filterwarnings('ignore')
    
    # get response from javascript and convert to json
    response = request.get_json()
    print(response)
    
    # set variables based on user responses   
    user_categories = response[0]
    user_zipcode = response[1]
    user_price = response[2]       

    # create dataframe based on user choices
    restaurants_df = pd.DataFrame({
        'ID': session['id_list'],
        'Name': session['name_list'],
        'Is_Closed': session['is_closed_list'],
        'Review_Count': session['review_count_list'],
        'Categories_All': session['categories_all_list'],
        'Categories': session['categories_list'],
        'Rating': session['rating_list'],
        'Latitude': session['latitude_list'],
        'Rating': session['rating_list'],
        'Latitude': session['latitude_list'],
        'Longitude': session['longitude_list'],
        'Price': session['price_list'],
        'Address': session['address_list'],
        'City': session['city_list'],
        'Zip_Code': session['zip_code_list'],
        'State': session['state_list']
        })
    
    print(session['categories_list'])

    restaurants_df.drop_duplicates(keep = False, inplace = True)
    restaurants_df.dropna(subset = ['Address'], inplace = True)
    restaurants_df.dropna(subset = ['Price'], inplace = True)
    restaurants_df = restaurants_df[restaurants_df.Price != '']
    restaurants_df['Price'].replace({'$$$$$': 5, '$$$$': 4, '$$$': 3, '$$': 2, '$': 1}, inplace = True)
    restaurants_df['Price'] = pd.to_numeric(restaurants_df['Price'])
    restaurants_df['Categories'].replace(['American (New)', 'American (Traditional)'], 'American', inplace = True)
    restaurants_df['Categories'].replace(['New Mexican Cuisine'], 'Mexican', inplace = True)

    cat_list_df= pd.DataFrame(columns=session['new_cat_list'])
    cat_list_df['new_col'] = pd.Series()

    new_df = pd.merge(restaurants_df, cat_list_df, how='left', left_on = restaurants_df.ID, right_on = cat_list_df.new_col)

    for i in session['new_cat_list']:
        new_df.loc[(new_df.Categories.str.contains(i)==True), i] = 1

    new_df.drop(axis = 1, columns = ['Categories', 'key_0', 'new_col'], inplace = True)
    new_df.drop_duplicates(subset = 'ID', inplace = True)
    new_df.fillna(0, inplace = True)

    modeling_df = new_df.drop(axis = 1, columns = ['ID', 'Name', 'Categories_All', 'Is_Closed', 'Latitude', 'Longitude', 'Address', 'City', 'State'])
    modeling_df = pd.get_dummies(modeling_df)

    L = list(modeling_df.columns)

    for i in range(3):
        L.pop(0)

    modeling_df[L] = modeling_df[L].astype('category')

    X = modeling_df.drop(axis = 1, columns = ['Review_Count', 'Rating'])
    y = modeling_df[['Rating']]

    # set test & traning data sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5)
    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    # random forest set up
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_jobs = -1, oob_score=True, verbose=0, max_depth=3)
    rf = rf.fit(X_train, y_train)

    user_df = X.drop(X.index)
    user_df['Price'] = [0]
    user_df.fillna(0, inplace = True)
    print('************** User columns:')
    print(user_df.columns)

    # # Inputs from user
    # user_zipcode = '91604'
    # user_categories = ['Burgers']
    # user_price = 2

    user_df.Price = user_price

    zip_column = [col for col in user_df.columns if user_zipcode in col]
    user_df[zip_column] = 1

    for category in user_categories:
        cat_column = [col for col in user_df.columns if category == col]
        user_df[cat_column[0]] = 1

    # Prediction
    user_prediction = np.round(rf.predict(user_df) * 2) / 2
    user_prediction = user_prediction[0] #4

    # Prediction to display
    print(user_prediction)
    return jsonify(user_prediction)
    
        
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