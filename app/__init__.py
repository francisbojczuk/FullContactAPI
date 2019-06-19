
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
    column_names = ['email','fullName','ageRange','gender','location','title','organization','twitter','linkedin','facebook','bio','avatar','website', 
                'detail_given_name','detail_family_name','detail_middle_name', 'detail_full_name','detail_birthday', 'detail_age_range','detail_age_value',
                'detail_phones_1', 'detail_phones_2', 'detail_phones_3', 'detail_phones_4', 'detail_phones_5', 
                'detail_profiles_youtube_username','detail_prifiles_youtube_url', 'detail_profiles_twitter_username','detail_profiles_twitter_userid',
                'detail_profiles_twitter_url','detail_profiles_twitter_bio', 'detail_profiles_twitter_followers','detail_profiles_twitter_following', 
                'detail_profiles_github_username', 'detail_profiles_github_url', 'detail_profiles_lastfm_username','detail_profiles_lastfm_url',
                'detail_profiles_gravatar_username','detail_profiles_gravatar_userid','detail_profiles_gravatar_url','detail_profiles_gravatar_bio',
                'detail_profiles_flickr_username','detail_profiles_flickr_userid', 'detail_profiles_flickr_url','detail_profiles_facebook_username',
                'detail_profiles_facebook_url','detail_profiles_tumblr_username','detail_profiles_tumblr_url','detail_profiles_pinterest_username',
                'detail_profiles_pinterest_url','detail_profiles_pinterest_bio','detail_profiles_pinterest_followers',
                'detail_profiles_pinterest_following', 'detail_profiles_google_username','detail_profiles_google_userid','detail_profiles_google_url',
                'detail_profiles_google_bio','detail_profiles_linkedin_username','detail_profiles_linkedin_userid','detail_profiles_linkedin_url',
                'detail_profiles_linkedin_bio','detail_profiles_linkedin_followers','detail_profiles_linkedin_following',  'detail_photos_0', 'detail_photos_1',
                'detail_photos_2','detail_photos_3','detail_photos_4','detail_photos_5','detail_photos_6','detail_photos_7','detail_photos_8','detail_photos_9', 
                'detail_education_name_1','detail_education_degree_1','detail_education_end_1',
                'detail_education_name_2','detail_education_degree_2','detail_education_end_2',
                'detail_education_name_3','detail_education_degree_3','detail_education_end_3',
                'detail_education_name_4','detail_education_degree_4','detail_education_end_4',
                'detail_education_name_5','detail_education_degree_5','detail_education_end_5',
                'detail_urls_0','detail_urls_1','detail_urls_2','detail_urls_3','detail_urls_4','detail_urls_5','detail_urls_6','detail_urls_7','detail_urls_8','detail_urls_9',
                'detail_topics_0','detail_topics_1','detail_topics_2','detail_topics_3','detail_topics_4','detail_topics_5','detail_topics_6','detail_topics_7','detail_topics_8','detail_topics_9',
                'updated']

    for i in range(20):
        column_names.append('detail_employment_name_{}'.format(i))
        column_names.append('detail_employment_current_{}'.format(i))
        column_names.append('detail_employment_title_{}'.format(i))
        column_names.append('detail_employment_start_{}'.format(i))
        column_names.append('detail_employment_end_{}'.format(i))
    
    for i in range(120):
        column_names.append('detail_interests_name_{}'.format(i))
        column_names.append('detail_interests_id_{}'.format(i))
        column_names.append('detail_interests_affinity_{}'.format(i))
        column_names.append('detail_interests_parentIds_{}'.format(i))
        column_names.append('detail_interests_category_{}'.format(i))  

    for i in range(20):
        column_names.append('addon_id_{}'.format(i))
        column_names.append('addon_name_{}'.format(i))
        column_names.append('addon_enabled_{}'.format(i))
        column_names.append('addon_applied_{}'.format(i))
        column_names.append('addon_description_{}'.format(i))
        column_names.append('addon_docLink_{}'.format(i))    
    
    def get_csv_row(x,email):
        ret = []    
        for column in column_names:
            ret.append(x.get(column, ''))
        ret[0] = email
        if len(x) == 0:
            return ret
        if x.get('details'):
            try:
                if x.get('details').get('name'):
                    try:
                        ret[13] = str(x.get('details').get('name').get('given',''))
                    except:
                        ret[13] = ''
                    try:
                        ret[14] = str(x.get('details').get('name').get('family',''))
                    except:
                        ret[14] = ''
                    try:
                        ret[15] = str(x.get('details').get('name').get('middle',''))
                    except:
                        ret[15] = ''
                    try:
                        ret[16] = str(x.get('details').get('name').get('full',''))
                    except:
                        ret[16] = ''
            except:
                print("Value error in x.get('details').get('name'): {}".format(email))
            try:
                if x.get('details').get('age'):
                    try:
                        birth = str(x.get('details').get('age').get('birthday'))
                    except:
                        pass
                    try:
                        ret[17] = str(birth.get('year','')) + '.' + str(birth.get('month','')) +'.'+ str(birth.get('day',''))  
                    except:
                        ret[17] = ''
                    try:
                        ret[18] = str(x.get('details').get('age').get('range',''))
                    except:
                        ret[18] = ''
                    try:
                        ret[19] = str(x.get('details').get('age').get('value',''))
                    except: 
                        ret[19] = ''
            except:
                print("Value error in x.get('details').get('age'): {}".format(email))
            try:
                if x.get('details').get('phones'):
                    for i in range(len( x.get('details').get('phones'))):
                        try:
                            ret[20 + i] = str(x.get('details').get('phones')[i])
                        except:
                            ret[20 + i] = ''
            except:
                pass
            try:        
                if x.get('details').get('profiles'):
                    try:
                        ret[25] = str(x.get('details').get('profiles').get('youtube').get('username',''))
                    except:
                        ret[25] = ''
                    try:
                        ret[26] = str(x.get('details').get('profiles').get('youtube').get('url',''))
                    except:
                        ret[26] = ''
                    try:
                        ret[27] = str(x.get('details').get('profiles').get('twitter').get('username',''))
                    except:
                        ret[27] = ''
                    try:
                        ret[28] = str(x.get('details').get('profiles').get('twitter').get('userid',''))
                    except:
                        ret[28] = ''
                    try:
                        ret[29] = str(x.get('details').get('profiles').get('twitter').get('url',''))
                    except:
                        ret[29] = ''
                    try:
                        ret[30] = str(x.get('details').get('profiles').get('twitter').get('bio','')).replace(';','')
                    except:
                        ret[30] = ''
                    try:
                        ret[31] = str(x.get('details').get('profiles').get('twitter').get('followers',''))
                    except:
                        ret[31] = ''
                    try:
                        ret[32] = str(x.get('details').get('profiles').get('twitter').get('following',''))
                    except:
                        ret[32] = ''
                    try:
                        ret[33] = str(x.get('details').get('profiles').get('github').get('username',''))
                    except:
                        ret[33] = ''
                    try:
                        ret[34] = str(x.get('details').get('profiles').get('github').get('url',''))
                    except:
                        ret[34] = ''
                    try:
                        ret[35] = str(x.get('details').get('profiles').get('lastfm').get('username',''))
                    except:
                        ret[35] = ''
                    try:
                        ret[36] = str(x.get('details').get('profiles').get('lastfm').get('url',''))
                    except:
                        ret[36] = ''
                    try:
                        ret[37] = str(x.get('details').get('profiles').get('gravatar').get('username',''))
                    except:
                        ret[37] = ''
                    try:
                        ret[38] = str(x.get('details').get('profiles').get('gravatar').get('userid',''))
                    except:
                        ret[38] = ''
                    try:
                        ret[39] = str(x.get('details').get('profiles').get('gravatar').get('url',''))
                    except:
                        ret[39] = ''
                    try:
                        ret[40] = str(x.get('details').get('profiles').get('gravatar').get('bio','')).replace(';','')
                    except:
                        ret[40] = ''
                    try:
                        ret[41] = str(x.get('details').get('profiles').get('flickr').get('username',''))
                    except:
                        ret[41] = ''
                    try:
                        ret[42] = str(x.get('details').get('profiles').get('flickr').get('userid',''))
                    except:
                        ret[42] = ''
                    try:
                        ret[43] = str(x.get('details').get('profiles').get('flickr').get('url',''))
                    except:
                        ret[43] = ''
                    try:
                        ret[44] = str(x.get('details').get('profiles').get('facebook').get('username',''))
                    except:
                        ret[44] = ''
                    try:
                        ret[45] = str(x.get('details').get('profiles').get('facebook').get('url',''))
                    except:
                        ret[45] = ''
                    try:
                        ret[46] = str(x.get('details').get('profiles').get('tumblr').get('username',''))
                    except:
                        ret[46] = ''
                    try:
                        ret[47] = str(x.get('details').get('profiles').get('tumblr').get('url',''))
                    except:
                        ret[47] = ''
                    try:
                        ret[48] = str(x.get('details').get('profiles').get('pinterest').get('username',''))
                    except:
                        ret[48] = ''
                    try:
                        ret[49] = str(x.get('details').get('profiles').get('pinterest').get('url',''))
                    except:
                        ret[49] = ''
                    try:
                        ret[50] = str(x.get('details').get('profiles').get('pinterest').get('bio','')).replace(';','')
                    except:
                        ret[50] = ''
                    try:
                        ret[51] = str(x.get('details').get('profiles').get('pinterest').get('followers',''))
                    except:
                        ret[51] = ''
                    try:
                        ret[52] = str(x.get('details').get('profiles').get('pinterest').get('following',''))
                    except:
                        ret[52] = ''
                    try:
                        ret[53] = str(x.get('details').get('profiles').get('google').get('username',''))
                    except:
                        ret[53] = ''
                    try:
                        ret[54] = str(x.get('details').get('profiles').get('google').get('userid',''))
                    except:
                        ret[54] = ''
                    try:
                        ret[55] = str(x.get('details').get('profiles').get('google').get('url',''))
                    except:
                        ret[55] = ''
                    try:
                        ret[56] = str(x.get('details').get('profiles').get('google').get('bio','')).replace(';','')
                    except:
                        ret[56] = ''
                    try:
                        ret[57] = str(x.get('details').get('profiles').get('linkedin').get('username',''))
                    except:
                        ret[57] = ''
                    try:
                        ret[58] = str(x.get('details').get('profiles').get('linkedin').get('userid',''))
                    except:
                        ret[58] = ''
                    try:
                        ret[59] = str(x.get('details').get('profiles').get('linkedin').get('url',''))
                    except:
                        ret[59] = ''
                    try:
                        ret[60] = str(x.get('details').get('profiles').get('linkedin').get('bio','')).replace(';','')
                    except:
                        ret[60] = ''
                    try:
                        ret[61] = str(x.get('details').get('profiles').get('linkedin').get('followers',''))
                    except:
                        ret[61] = ''
                    try:
                        ret[62] = str(x.get('details').get('profiles').get('linkedin').get('following',''))
                    except:
                        ret[62] = ''
            except:
                print("Value error in x.get('details').get('profile'): {}".format(email))
            try:                    
                if x.get('details').get('employment'):
                    for i in range(len(x.get('details').get('employment'))):
                        try:
                            ret[109+(i*6)] = str(x.get('details').get('employment')[i].get('name',''))
                        except:
                            ret[109+(i*6)] = ''
                        try:
                            ret[110+(i*6)] = str(x.get('details').get('employment')[i].get('domain',''))
                        except:
                            ret[110+(i*6)] = ''
                        try:
                            ret[111+(i*6)] = str(x.get('details').get('employment')[i].get('current',''))
                        except:
                            ret[111+(i*6)] = ''
                        try:
                            ret[112+(i*6)] = str(x.get('details').get('employment')[i].get('title',''))
                        except:
                            ret[112+(i*6)] = ''
                        try:
                            ret[113+(i*6)] = str(x.get('details').get('employment')[i].get('start').get('year','') + '.' + \
                                        x.get('details').get('employment')[i].get('start').get('month',''))
                        except:
                            ret[113+(i*6)] = ''
                        try:
                            ret[114+(i*6)] = str(x.get('details').get('employment')[i].get('end').get('year','') + '.' + \
                                        x.get('details').get('employment')[i].get('end').get('month',''))
                        except:
                            ret[114+(i*6)] = ''
                    
            except:
                print("Value error in x.get('details').get('employment'): {}".format(email))
            try:
                if x.get('details').get('photos'):
                    for i in range(len(x.get('details').get('photos'))):
                        try:
                            ret[63 + i] = str(x.get('details').get('photos')[i].get('value',''))
                            # print(ret[63 + i])
                        except:
                            ret[63 + i] = ''
            except:
                print("Value error in x.get('details').get('photos'): {}".format(email))
            try:
                if x.get('details').get('education'):
                    for i in range(len(x.get('details').get('education'))):
                        try:
                            ret[73 + (i*3)] = str(x.get('details').get('education')[i].get('name',''))
                        except:
                            ret[73 + (i*3)] = ''
                        try:
                            ret[74 + (i*3)] = str(x.get('details').get('education')[i].get('degree',''))
                        except:
                            ret[74 + (i*3)] = ''
                        try:
                            ret[75 + (i*3)] = str(x.get('details').get('education')[i].get('end').get('year',''))
                        except:
                            ret[75 + (i*3)] = ''
            except:
                print("Value error in x.get('details').get('education'):{}".format(email))
            try:
                if x.get('details').get('urls'):
                    for i in range(len(x.get('details').get('urls'))):
                        try:
                            ret[88 + i] = str(x.get('details').get('urls')[i].get('value',''))
                        except:
                            ret[88 + i] = ''
            except:
                print("Value error in x.get('details').get('urls'): {}".format(email))
            try:
                if x.get('details').get('interests'):
                    for i in range(len(x.get('details').get('interests'))):
                        
                        try:
                            ret[129 + (i*5)] = str(x.get('details').get('interests')[i].get('name',''))
                        except:
                            ret[129 + (i*5)] = ''
                        try:
                            ret[130 + (i*5)] = str(x.get('details').get('interests')[i].get('id',''))
                        except:
                            ret[130 + (i*5)] = ''
                        try:
                            ret[131 + (i*5)] = str(x.get('details').get('interests')[i].get('affinity',''))
                        except:
                            ret[131 + (i*5)] = ''
                        try:
                            ret[132 + (i*5)] = str(x.get('details').get('interests')[i].get('parentIds')[0])
                        except:
                            ret[132 + (i*5)] = ''
                        try:
                            ret[133 + (i*5)] = str(x.get('details').get('interests')[i].get('category',''))
                        except:
                            ret[133 + (i*5)] = ''
            except:
                pass
            try:
                if x.get('details').get('topics'):
                    for i in range(len(x.get('details').get('topics'))):
                        try:
                            ret[98 + i] = str(x.get('detail').get('topics')[i])
                        except:
                            ret[98 + i] = ''
            except:
                print("Value error in x.get('details').get('interests'): {}".format(email))
        try:
            if x.get('dataAddOns'): 

                for i in range(len(x.get('dataAddOns'))):
                    try:
                        ret[249 + (i*6)] = str(x.get('dataAddOns')[i].get('id',''))
                    except:
                        ret[251 + (i*6)] = ''
                    try:
                        ret[252 + (i*6)] = str(x.get('dataAddOns')[i].get('name',''))
                    except:
                        ret[253 + (i*6)] = ''
                    try:
                        ret[254 + (i*6)] = str(x.get('dataAddOns')[i].get('enabled',''))
                    except:
                        ret[255 + (i*6)] = ''
                    try:
                        ret[256 + (i*6)] = str(x.get('dataAddOns')[i].get('applied',''))
                    except:
                        ret[257 + (i*6)] = ''
                    try:
                        ret[258 + (i*6)] = str(x.get('dataAddOns')[i].get('description',''))
                    except:
                        ret[259 + (i*6)] = ''
                    try:
                        ret[260 + (i*6)] = str(x.get('dataAddOns')[i].get('docLink',''))
                    except:
                        ret[261 + (i*6)] = ''

        except:
            print("Value error in x.get('details').get('dataAddOns'): {}".format(email))
        try:
            if x.get('updated'):
                ret[108] = str(x.get('updated', ''))
        except:
            pass
        print(x)   
        print('=======================================')
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

                    # line_count = 0
                    for row in csv_reader:
                        if row:
                            email = row[0]
                            # line_count += 1
                            # if line_count%100 == 0:
                            #     time.sleep(30)
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
                            except urllib.error.HTTPError as e:
                                print('API HTTPrequest handling error{0}: {1}'.format(e.getcode(), email))
                                if e.getcode() == 403:
                                    time.sleep(300)
                                    print('rised x-limit, so please for a while...')
                                xx = {}
                                csv_out.writerow(get_csv_row(xx, email))
                            except urllib.error.URLError as e:
                                # Not an HTTP-specific error (e.g. connection refused)
                                # ...
                                print('URLError: {0}: {1}'.format(e.reason, email))
                                xx = {}
                                csv_out.writerow(get_csv_row(xx, email))           
                                
                    flash('Hello, Success!')  
                    
                ##################################

            else:
                flash('Error: All Fields are Required')

        # load registration template
        return render_template('index.html', title='Scraper via FullContactAPI', form=form)

    return app