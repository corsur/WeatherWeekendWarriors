#get your data credentials by putting any sample file in the files area to the right
#then click "insert to code" and it will paste the data below, just change the name to suit
myDataCreds = {
  'auth_url':'https://identity.open.softlayer.com',
  'project':'YOUR_DATA_HERE',
  'project_id':'YOUR_DATA_HERE',
  'region':'YOUR_DATA_HERE',
  'user_id':'YOUR_DATA_HERE',
  'domain_id':'YOUR_DATA_HERE',
  'domain_name':'YOUR_DATA_HERE',
  'username':'YOUR_DATA_HERE',
  'password':"YOUR_DATA_HERE",
  'container':'YOUR_DATA_HERE',
  'tenantId':'undefined',
  'filename':'SOME_FILE_NAME.EXT'
}

def put_file(credentials, local_file_name):
    """This functions returns a StringIO object containing
    the file content from Bluemix Object Storage V3."""
    f = open(local_file_name,'r')
    my_data = f.read()
    url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': credentials['username'],'domain': {'id': credentials['domain_id']},
            'password': credentials['password']}}}}}
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    resp1_body = resp1.json()
    #print resp1_body
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']=='dallas'):
                            url2 = ''.join([e2['url'],'/', credentials['container'], '/', local_file_name])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    resp2 = requests.put(url=url2, headers=headers2, data = my_data )
    print resp2

df = pd.DataFrame(numpy.random.randint(0,100,size=(100,4)), columns=list('ABCD'))
df.to_csv('myData.csv',index=False)
put_file(myDataCreds,'myData.csv')
