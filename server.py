import os
import pymysql
import flask
import json
import datetime
from flask import request, flash, redirect, render_template, send_from_directory
from DBConfiguror import DBConfiguror

ALLOWED_EXTENSIONS = ['yaml']

app = flask.Flask(__name__, static_url_path='')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

dbc = DBConfiguror()

def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/data/download', methods=['GET'])
def get_json():
    if os.path.exists(os.path.join('data', 'data.json')):
        return send_from_directory('data', 'data.json', as_attachment=True, cache_timeout=0)
    else:
        flash("No data available for download, please perform a search first!")
        return render_template('configuration.html')

@app.route('/configuration', methods = ['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        # Check if the post request has the file part:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # Extract file:
        file = request.files['file']
        # If user did not select a file, browser will submit an empty part without a filename:
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file:
            # Check if correct extension:
            if not allowed_file(file.filename):
                flash("Not a yaml file! Please try again.")
                return redirect(request.url)
            else:
                flash("Configuration yaml file accepted!")
                dbc.configure_options_with_yaml(config_yaml_file=file.filename)
                return redirect(request.url)
    else:
        return render_template('configuration.html')

@app.route('/readings/<box_id>/<from_date>/<to_date>', methods=['GET'])
def retrieve_sensor_data_from_database(box_id, from_date, to_date):
    # Attempt to establish a connection with the database:
    try:
        con = pymysql.connect(host=dbc.get_host(),
                              user=dbc.get_user(),
                              password=dbc.get_password(),
                              port=dbc.get_port(),
                              db=dbc.get_db(),
                              cursorclass=pymysql.cursors.DictCursor)
    except:
        flash("Unable to connect to Database using current configuration.")
        return render_template('query.html', box_id=box_id, from_date=from_date, to_date=to_date)

    # Attempt to submit the query:
    try:
        with con.cursor() as cur:
            cur.execute('SELECT box_id, sensor_id, name, unit, reading, reading_ts '
                        'FROM readings INNER JOIN sensors ON readings.sensor_id = sensors.id '
                        'WHERE box_id = %s AND reading_ts > %s AND reading_ts <= %s;', (box_id, from_date, to_date,))
    except:
        flash("Invalid query! Please try again.")

    # Close connection:
    con.close()

    # Extract results and save them to a json file on disk:
    rows = cur.fetchall()
    info = []
    for row in rows:
        info.append({'box_id': row['box_id'],
                     'sensor_id': row['sensor_id'],
                     'name': row['name'],
                     'unit': row['unit'],
                     'reading': row['reading'],
                     'reading_ts': row['reading_ts'].__str__()})

    # Write file to disk:
    with open(os.path.join('data', 'data.json'), 'w') as f:
        json.dump(info, f)

    return render_template('query.html', box_id=box_id, from_date=from_date, to_date=to_date)



if __name__ == '__main__':
    app.run()
