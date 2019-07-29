from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/api/data')
def data():
     return jsonify()

@app.route('/cityInput', methods=['POST'])
def cityInput():
     city_input = request.form['city_input']
     return city_input
     
@app.route('/zip_and_category', methods=['POST'])
def zip_and_category():
     zip_code = request.form['zip_code']
     category_input = request.form['category_input']
     return zip_code, category_input

if __name__ == "__main__":
     app.run(debug=True, use_reloader=False)