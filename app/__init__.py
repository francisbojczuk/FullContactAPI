
import os, csv, json,  pathlib
from flask import Flask, render_template, flash, request, redirect

from config import app_config
from app.forms import IndexForm
from werkzeug.utils import secure_filename

def create_app(config_name):
    app =  Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    current_dir = pathlib.Path(__file__).parent
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])
    def allowed_file(filename):
    	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        form = IndexForm()
        return render_template('index.html', title='Scraper via FullContactAPI', form=form)
    @app.route('/', methods=['GET', 'POST'])
    def index_submit():
        form = IndexForm()
        if request.method == 'POST':
            email=form.email.data
            api_key=form.api_key.data
            #######################################
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_dir,"tmp",filename))
                flash('File successfully uploaded')
                return redirect('/')
            else:
                flash('Allowed file types are txt or csv')
                return redirect(request.url)
                
           
            #######################################
       
            if form.validate_on_submit():
                flash('Hello: {} {}'.format(email, api_key))
            else:
                flash('Error: All Fields are Required')

        # load registration template
        return render_template('index.html', title='Scraper via FullContactAPI', form=form)

    return app