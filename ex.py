import urllib.request, json
import pprint
import csv

column_names = ['email','emailHash','twitter','phone','fullName','ageRange','gender','location','title','organization',
            'linkedin','facebook','bio','avatar','website']
Key = "8dENnYQ25g9cmBtufbesokUKPtMZati2"

def get_csv_row(x):
    ret = []
    for column in column_names:
        ret.append(x.get(column, ''))

    print(ret)
    return ret



req = urllib.request.Request('https://api.fullcontact.com/v3/person.enrich')
req.add_header('Authorization', 'Bearer {}'.format(Key))


data = json.dumps({
    "email": "bart@fullcontact.com"
})

response = urllib.request.urlopen(req, data.encode())

x = response.read().decode('utf-8')
print(type(x))
xx = json.loads(x)
f = csv.writer(open("test.csv", "w"))
f.writerow(column_names)
f.writerow(get_csv_row(xx))

    
