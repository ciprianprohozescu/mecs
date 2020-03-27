from flask import Flask, render_template
from data_dump import data_dump
from flask import jsonify
app = Flask(__name__)

# calls a method that reads local events and returns them
dump_data = data_dump()

#Routing
""" Main Page """
@app.route('/')
def index():
    # render home page and pass the data
    return render_template('home.html', data = dump_data)

""" If we want to credit anybody/anything or just write something"""
@app.route('/about')
def about():
    return render_template('about.html')

""" Returns all jsonified events """
@app.route('/all', methods=['GET'])
def api_all():
    return jsonify(dump_data)

""" Returns jsonified event at the n-th position """
@app.route('/<string:id>/', methods=['GET'])
def api_event_id(id):
    num_id = int(id)
    return jsonify(dump_data[num_id-1])

if __name__ == '__main__':
    app.run(debug = True, use_reloader = False) # if use_reloader=True, debug=True causes SystemExit error