import csv
import json
from get import FullContactAdaptiveClient

api = FullContactAdaptiveClient()

open_file = open('sample.txt','r')

emails = map(lambda s: s.strip(),open_file.readlines())

fieldnames = ['email','name_given_fc','name_first_fc','name_last_fc','name_prefix_fc','name_suffix_fc','name_nickname_fc','fullname_fc','ageRange_fc','gender_fc','locations_fc','Title_fc','Organization_fc','Twitter_fc',
                'Linkedin_fc','Facebook_fc','Bio_Facebook_fc','Bio_Twitter_fc','Bio_Linkedin_fc','Avatar_fc','website_fc','Details_fc','birthday_year_fc','birthday_month_fc','birthday_day_fc','agerange_2_fc','age_fc',
                'locations_label_fc','locations_city_fc','locations_region_fc','locations_regionCode_fc','locations_country_fc','locations_countryCode_fc',
                'locations_formatted_fc','education_name_fc','education_degree_fc','education_endYear_fc','topics_1_fc','topics_2_fc','topics_3_fc','topics_4_fc','topics_5_fc','topics_6_fc','topics_7_fc','topics_8_fc','topics_9_fc']

def csv_dict_writer(path,filednames,data):
    """
    Writes a CSV file using DicWriter
    """
    with open(path,'w', newline='') as out_file:
        writer = csv.DictWriter(out_file,delimiter=',',fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

data = []

def get_data(response,email):
    dict_of_data = {}
    dict_of_data['email'] = email
    if 'contactInfo' in response:
        if 'fullName' in response['contactInfo']:
            dict_of_data['fullname_fc'] = response['contactInfo']['fullName']   
        else:
            fullname_fc = ''
            dict_of_data['fullname_fc'] = fullname_fc
           
        if 'givenName' in response['contactInfo']:
            dict_of_data['name_given_fc'] = response['contactInfo']['givenName']
        else:
            dict_of_data['name_given_fc'] = ''
        
        if 'familyName' in response['contactInfo']:
            dict_of_data['name_last_fc'] = response['contactInfo']['familyName']
        else:
            dict_of_data['name_last_fc'] = ''

        if 'middleName' in response['contactInfo']:
            dict_of_data['name_first_fc'] = response['contactInfo']['middleName']
        else:
            dict_of_data['name_first_fc'] = ''

        if 'prefixName' in response['contactInfo']:
            dict_of_data['name_prefix_fc'] = response['contactInfo']['prefixName']
        else:
            dict_of_data['name_prefix_fc'] = ''

        if 'suffixName' in response['contactInfo']:
            dict_of_data['name_suffix_fc'] = response['contactInfo']['suffixName']
        else:
            dict_of_data['name_suffix_fc'] = ''

        if 'nicknameName' in response['contactInfo']:
            dict_of_data['name_nickname_fc'] = response['contactInfo']['nicknameName']
        else:
            dict_of_data['name_nickname_fc'] = ''

        if 'websites' in response['contactInfo']:
            websites = response['contactInfo']['websites']
            url_list = []
            for url in websites:
                url_list.append(url['url'])

            dict_of_data['website_fc'] = ', '.join(url_list)
            
        else:
            dict_of_data['website_fc'] = ''
    
    if 'demographics' in response:
        if 'age' in response['demographics']:
            dict_of_data['age_fc'] = response['demographics']['age']
            for age in response['demographics']['age']:
                if 'birthday' in age:
                    dict_of_data['birthday_year_fc'] = birthday['year']
                    dict_of_data['birthday_month_fc'] = birthday['month']
                    dict_of_data['birthday_day_fc'] = birthday['day']
                if 'range' in age:
                    dict_of_data['agerange_2_fc'] = age['range']
                if 'value' in age:
                    dict_of_data['age_fc'] = age['value']

        if 'ageRange' in response['demographics']:
            dict_of_data['ageRange_fc'] = response['demographics']['ageRange']
        if 'locationGeneral' in response['demographics']:
            dict_of_data['locations_fc'] = response['demographics']['locationGeneral']
        else:
            dict_of_data['locations_fc'] = ''

        if 'locationDeduced' in response['demographics']:
            if 'state' in response['demographics']['locationDeduced']:
                dict_of_data['locations_label_fc'] = response['demographics']['locationDeduced']['state']['name']
                
            else:
                dict_of_data['locations_label_fc'] = ''

            if 'city' in response['demographics']['locationDeduced']:
                dict_of_data['locations_city_fc'] = response['demographics']['locationDeduced']['city']['name']
            else:
                dict_of_data['locations_city_fc'] = ''

            if 'continent' in response['demographics']['locationDeduced']:
                dict_of_data['locations_region_fc'] = response['demographics']['locationDeduced']['continent']['name']
                if 'code' in response['demographics']['locationDeduced']['continent']:
                    dict_of_data['locations_regionCode_fc'] = response['demographics']['locationDeduced']['continent']['code']
                else:
                    dict_of_data['locations_regionCode_fc'] = ''
            else:
                dict_of_data['locations_region_fc'] = ''

            
            if 'country' in response['demographics']['locationDeduced']:
                dict_of_data['locations_country_fc'] = response['demographics']['locationDeduced']['country']['name']
                if 'code' in response['demographics']['locationDeduced']['country']:
                    dict_of_data['locations_countryCode_fc'] = response['demographics']['locationDeduced']['country']['code']
                else:
                    dict_of_data['locations_countryCode_fc'] = ''
            else:
                dict_of_data['locations_country_fc'] = ''

            if 'deducedLocation' in response['demographics']['locationDeduced']:
                dict_of_data['locations_formatted_fc'] = response['demographics']['locationDeduced']['deducedLocation']
            else:
                dict_of_data['locations_formatted_fc'] = ''

                        
        else:
            dict_of_data['locations_label_fc'] = ''
            dict_of_data['locations_city_fc'] = ''
            dict_of_data['locations_region_fc'] = ''
            dict_of_data['locations_regionCode_fc'] = ''
            dict_of_data['locations_country_fc'] = ''
            dict_of_data['locations_countryCode_fc'] = ''
            dict_of_data['locations_formatted_fc'] = ''

        if 'gender' in response['demographics']:
            dict_of_data['gender_fc'] = response['demographics']['gender']
        else:
            dict_of_data['gender_fc'] = ''


    if 'digitalFootprint' in response:
        if 'topics' in response['digitalFootprint']:
            topics = response['digitalFootprint']['topics']
            
            count = 0
            for elements in topics:
                topics_list = []
               
                count = count + 1
                if count == 1:
                
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_1_fc'] = ', '.join(topics_list)
                
                if count == 2:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_2_fc'] = ', '.join(topics_list)
                if count == 3:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_3_fc'] = ', '.join(topics_list)
                if count == 4:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_4_fc'] = ', '.join(topics_list)
                if count == 5:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_5_fc'] = ', '.join(topics_list)
                if count == 6:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_6_fc'] = ', '.join(topics_list)
                if count == 7:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_7_fc'] = ', '.join(topics_list)
                if count == 8:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_8_fc'] = ', '.join(topics_list)
                if count == 9:
                    for element in elements:
                        topics_list.append(elements[element])
                    dict_of_data['topics_9_fc'] = ', '.join(topics_list)
                

    if 'organizations' in response:
        org_list = []
        title = []
        for org_element in response['organizations']:
            org_list.append(org_element['name'])
            title.append(org_element['title'])
        dict_of_data['Organization_fc'] = ','.join(org_list)
        dict_of_data['Title_fc'] = '&'.join(title)
       
    if 'socialProfiles' in response:
        for profiles in response['socialProfiles']:
            if profiles['typeName'] == 'Facebook':
                dict_of_data['Facebook_fc'] = profiles['url']
                if 'bio' in profiles:
                    dict_of_data['Bio_Facebook_fc'] = profiles['bio']
            if profiles['typeName'] == 'Twitter':
                dict_of_data['Twitter_fc'] = profiles['url']
                if 'bio' in profiles:
                    dict_of_data['Bio_Twitter_fc'] = profiles['bio']
            if profiles['typeName'] == 'LinkedIn':
                dict_of_data['Linkedin_fc'] = profiles['url']
                if 'bio' in profiles:
                    dict_of_data['Bio_Linkedin_fc'] = profiles['bio']

            # for elem in profiles:
            #     if 'bio' in elem:
            #         dict_of_data['Bio_fc'] = profiles[elem]
                    
    if 'education' in response:
        for education in response['education']:
            if 'name' in education:
                dict_of_data['education_name_fc'] = education['name']
            if 'degree' in education:
                dict_of_data['education_degree_fc'] = education['degree']
            if 'end' in education:
                dict_of_data['education_endYear_fc'] = education['end']['year']

    if 'photos' in response:
        for avatar in response['photos']:
            if 'Gravatar' in avatar['typeName']:
                dict_of_data['Avatar_fc'] = avatar['url']
            else:
                pass

    if 'details' in response:
        dict_of_data['Details_fc'] = response['details']
    
        
    return dict_of_data

for email in emails:
    res = api.call_fullcontact(email)
    dict_of_data = get_data(res,email)
    print(json.dumps(res, indent=4, sort_keys=True))
    data.append(dict_of_data)
    print(email), "done"
    
path = 'dict_output.csv'
csv_dict_writer(path,fieldnames,data)