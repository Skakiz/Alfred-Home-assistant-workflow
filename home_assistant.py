import sys
import argparse
import json
import unicodedata
import update_data as updater
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

def getData(wf, haType):
    data = wf.stored_data(haType)
    return data

def get_recent(url, path, password):
    url = url + '/api/states/' + path + '?api_password=' + password

    params = dict(count=100, format='json')
    r = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    result = r.json()
    posts = result['attributes']['entity_id']

    return posts

def post_to_ha(url, path, password, entity_id):

    url = url + '/api/services/' + path + '?api_password=' + password

    sys.stderr.write('url : '+ url + '\n')
    params = dict(count=100, format='json')
    #r = web.post(url, dict,  data='{"entity_id": "' + entity_id + '"}');
    data='{"entity_id": "' + entity_id + '"}'
    sys.stderr.write('data : '+ data + '\n')
    r = web.post(url, params, data, headers=None, cookies=None, files=None, auth=None, timeout=60, allow_redirects=False, stream=False)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    result = r.json()
    sys.stderr.write('post result : '+ r.text + '\n')

    return entity_id + ' is invoked';

def post_json_to_ha(url, path, password, josn):

    url = url + '/api/services/' + path + '?api_password=' + password

    sys.stderr.write('url : '+ url + '\n')
    params = dict(count=100, format='json')
    #r = web.post(url, dict,  data='{"entity_id": "' + entity_id + '"}');
    sys.stderr.write('josn : '+ josn + '\n')
    r = web.post(url, params, josn, headers=None, cookies=None, files=None, auth=None, timeout=60, allow_redirects=False, stream=False)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    result = r.json()
    sys.stderr.write('post result : '+ r.text + '\n')

    return result;

def getPassword(wf):
    try:
        password = wf.get_password('ha_password')
    except PasswordNotFound:  # API key has not yet been set
        wf.add_item('No password set.',
                    'Please use the API password on your home assistant.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
    
    return password    

def getURL(wf):
    try:
        url = wf.get_password('ha_url')
        sys.stderr.write('url : ' + url + ' \n')
    except PasswordNotFound:  # API key has not yet been set
        wf.add_item('No URL set.',
                    'Please use the base URL on your home assistant. Like haseturl htttps://wwww.url.com:8123',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
    
    return url  

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

def main(wf):

    sys.stderr.write('In main(wf)\n')
     # build argument parser to parse script args and collect their
     # values
    parser = argparse.ArgumentParser()
     # add an optional (nargs='?') --setkey argument and save its
     # value to 'apikey' (dest). This will be called from a separate "Run Script"
     # action with the API key
    parser.add_argument('-setkey', dest='apikey', nargs='?', default=None)
    parser.add_argument('-seturl', dest='seturl', nargs='?', default=None)
    parser.add_argument('-loadEntities', dest='loadEntities', nargs='?', default=None)
     # add an optional query and save it to 'query'
    parser.add_argument('query', nargs='?', default=None)
     # parse the script's arguments

    args = parser.parse_args(wf.args)

    my_query = wf.args[0]
    sys.stderr.write('my_query : ' + my_query + '\n')
     ####################################################################
     # Save the provided API key
     ####################################################################

    if args.apikey: 
        sys.stderr.write('Set password\n')
         # save the key
        wf.save_password('ha_password', args.apikey)
        return 0  # 0 means script exited cleanly

     ####################################################################
     # Save the provided URL
     ####################################################################

    if args.seturl: 
        sys.stderr.write('Set URL\n')
         # save the key
        wf.save_password('ha_url', args.seturl)
        return 0  # 0 means script exited cleanly

     ####################################################################
     # Save the entities to storage.
     ####################################################################


    if args.loadEntities:
        sys.stderr.write('Update data\n')
        updater.updateData(wf)

     ####################################################################
     # Check that we have an API key saved
     ####################################################################

    #sys.stderr.write('No argumet found!\n')
    return 0

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))