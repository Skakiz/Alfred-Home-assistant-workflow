import sys
import argparse
import home_assistant as util
from workflow import web, Workflow, PasswordNotFound

def updateData(wf):

    wf.logger.debug('Load entities')

    #get URL and password
    password = util.getPassword(wf);
    url = util.getURL(wf);

    url = url + '/api/states?api_password=' + password

    params = dict(count=100, format='json')
    r = web.get(url)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by pinboard and extract the posts
    #data = json.loads(r.text.decode(r.encoding))
    data = r.json()
    #sys.stderr.write('Load entities result : '+ json.dumps(data) + '\n')

    #Rearange data, so all typs are grouped.
    main = dict()

    for item in data:
        #sys.stderr.write('Entity : '+ json.dumps(item) + '\n')
        entity_id = item['entity_id']
        ent_name_split = entity_id.split('.')
        ent_type = ent_name_split[0]
        name = ent_name_split[1]

        attribute = item['attributes']

        icon = ''
        if 'icon' in attribute.keys():
            icon = attribute['icon']

        unit = ''
        if 'unit_of_measurement' in attribute.keys():
            unit = attribute['unit_of_measurement']

        state = ''
        if 'state' in item:
            state = item['state']

        friendly_name = item['attributes']['friendly_name']
        ent = {entity_id : {'type' : ent_type, 'name' : name, 'entity_id' : entity_id, 'icon' : icon, 'friendly_name' : friendly_name, 'unit' : unit, 'state' : state}}

        #sys.stderr.write('ent :  ' + str(ent) + '\n')

        if ent_type in main.keys():
            main[ent_type].update(ent)
        else:
            main[ent_type] = dict(ent);

    #go thur groups and store structure
    for item in main:
        wf.store_data(item, main[item])
        #sys.stderr.write('store :  ' + str(main[item]) + '\n')

    return 0

def main(wf):

    try:
        updateData(wf)

    except PasswordNotFound:  # API key has not yet been set
         # Nothing we can do about this, so just log it
        wf.logger.error('No Password saved')

if __name__ == '__main__':
    wf = Workflow()
    wf.run(main)