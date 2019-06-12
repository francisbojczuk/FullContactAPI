
import os, csv, json,  pathlib, urllib.request, time
from flask import Flask, render_template, flash, request, redirect

from config import app_config
from app.forms import IndexForm
from werkzeug.utils import secure_filename
from . import fullcontactapi

def create_app(config_name):
    app =  Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    current_dir = pathlib.Path(__file__).parent
    ALLOWED_EXTENSIONS = set(['txt', 'csv'])
    def allowed_file(filename):
    	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    ###########################################
    column_names = ['email','twitter','phone','fullName','ageRange','gender','location','title','organization',
                    'linkedin','facebook','bio','avatar','website','employment_name','employment_domain','employment_status',
                    'employment_title','employment_start','employment_end','interests_name','interests_id',
                    'interests_affinity','interests_parrentIds','interests_category','profile_twitter_info',
                    'photos_label','photos_value','urls_lable','urls_value','name_given','name_family','name_middle','name_prefix',
                    'name_suffix','name_nickname','birthday', 'age_range','age_value','gender','location_label',
                    'location_city','location_region','location_reg_code','location_country','location_coutry_code','location_formatted',
                    'education_name','education_degree','education_end','email_md5','email_sha256','topics','keypeople',
                    'dataAddOns','updated']
    def get_csv_row(x,email):
        ret = []
        for column in column_names:
            ret.append(x.get(column, ''))
        try:
            ret[0] = email
            if x.get('details'):
                if x.get('details').get('employment'):
                    ret[14] = x.get('details').get('employment').get('name','')
                    ret[15] = x.get('details').get('employment').get('domain','')
                    ret[16] = x.get('details').get('employment').get('current','')
                    ret[17] = x.get('details').get('employment').get('title','')
                    ret[18] = x.get('details').get('employment').get('start','')
                    ret[19] = x.get('details').get('employment').get('end','')
                if x.get('details').get('interests'):
                    ret[20] = x.get('details').get('interests').get('name','')
                    ret[21] = x.get('details').get('interests').get('id','')
                    ret[22] = x.get('details').get('interests').get('affinity','')
                    ret[23] = x.get('details').get('interests').get('parentIds','')
                    ret[24] = x.get('details').get('interests').get('category','')
                if x.get('details').get('profile'):
                    ret[25] = x.get('details').get('profile').get('twitter','')
                if x.get('details').get('photos'):
                    ret[26] = x.get('details').get('photos').get('label','')
                    ret[27] = x.get('details').get('photos').get('value','')
                if x.get('details').get('urls'):
                    ret[28] = x.get('details').get('urls').get('label','')
                    ret[29] = x.get('details').get('urls').get('value','')
                if x.get('details').get('name'):
                    ret[30] = x.get('details').get('name').get('given','')
                    ret[31] = x.get('details').get('name').get('family','')
                    ret[32] = x.get('details').get('name').get('middle','')
                    ret[33] = x.get('details').get('name').get('prefix','')
                    ret[34] = x.get('details').get('name').get('suffix','')
                    ret[35] = x.get('details').get('name').get('nickname','')
                if x.get('details').get('age'):
                    ret[36] = x.get('details').get('age').get('birthday','')
                    ret[37] = x.get('details').get('age').get('range','')
                    ret[38] = x.get('details').get('age').get('value','')
                if x.get('details').get('gender'):
                    ret[39] = x.get('details').get('gender','')
                if x.get('details').get('locations'):
                    ret[40] = x.get('details').get('location').get('label','')
                    ret[41] = x.get('details').get('location').get('city','')
                    ret[42] = x.get('details').get('location').get('region','')
                    ret[43] = x.get('details').get('location').get('regionCode','')
                    ret[44] = x.get('details').get('location').get('country','')
                    ret[45] = x.get('details').get('location').get('countryCode','')
                    ret[46] = x.get('details').get('location').get('formatted','')
                if x.get('details').get('education'):
                    ret[47] = x.get('details').get('location').get('name','')
                    ret[48] = x.get('details').get('location').get('degree','')
                    ret[49] = x.get('details').get('location').get('end','')
                if x.get('details').get('emails'):
                    ret[50] = x.get('details').get('emails').get('value','')
                    ret[51] = x.get('details').get('emails').get('md5','')
                    ret[52] = x.get('details').get('emails').get('sha256','')
                if x.get('details').get('topics'):
                    ret[53] = x.get('details').get('topics','')
                if x.get('details').get('keyPeople'):
                    ret[54] = x.get('details').get('keyPeople','')

            res[55] = x.get('dataAddOns','')
            res[56] = x.get('updated','')

        except:
            pass

        print(ret)
        return ret
    ###########################################

    @app.route('/')
    def index():
        form = IndexForm()
        return render_template('index.html', title='Scraper via FullContactAPI', form=form)
    @app.route('/', methods=['GET', 'POST'])
    def index_submit():
        form = IndexForm()
        if request.method == 'POST':
            
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
                
            else:
                flash('Allowed file types are txt or csv')
                return redirect(request.url)
                
           
            api_key=form.api_key.data
            if form.validate_on_submit():
                
                ##################################
                
                with open(os.path.join(current_dir,"tmp",filename)) as input_file, open('output.csv','w') as output:
                    csv_reader = csv.reader(input_file, delimiter=',')
                    csv_out = csv.writer(output,delimiter=',')
                    csv_out.writerow(column_names)

                    line_count = 0
                    for row in csv_reader:
                        if row:
                            email = row[0]
                            line_count += 1
                            if line_count%100 == 0:
                                time.sleep(30)
                            try: 
                                # response = call_fullcontact(email, api_key)
                                req = urllib.request.Request('https://api.fullcontact.com/v3/person.enrich')
                                req.add_header('Authorization', 'Bearer {}'.format(api_key))
                        
                                data = json.dumps({
                                    "email": "{}".format(email)
                                })

                                response = urllib.request.urlopen(req, data.encode())

                                x = response.read().decode('utf-8')
                                xx = json.loads(x)
                                # f = csv.writer(open("output.csv", "w"))
                                # f.writerow(column_names)
                                csv_out.writerow(get_csv_row(xx, email))
                            except:
                                pass
                    flash('Hello, Success!')  
                    
                ##################################

            else:
                flash('Error: All Fields are Required')

        # load registration template
        return render_template('index.html', title='Scraper via FullContactAPI', form=form)

    return app