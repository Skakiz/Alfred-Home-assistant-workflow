import sys
import argparse
import home_assistant as util
from workflow import web, Workflow, PasswordNotFound

log = None

def copyItemAndAdd(main, ent_type, entity_id, name, friendly_name, icon, unit, value, sensorType, longitude, latitude):

    search_words = getSearchWords(icon, unit, value, friendly_name)
    key = entity_id + '_' + sensorType
    ent = {key: {'type' : ent_type, 'name' : name, 'entity_id' : entity_id, 'icon' : icon, 'friendly_name' : friendly_name, 'unit' : unit, 'state' : value, 'longitude' : longitude, 'latitude' : latitude, 'search_words' : search_words}}

    if ent_type in main.keys():
        main[ent_type].update(ent)
    else:
        main[ent_type] = dict(ent);

    return main

def getSearchWords(icon, unit, value, friendly_name):
    result = '';

    if 'thermo' in icon:
        result = 'temperature '

    if 'lux' in unit:
        result = result + 'light '

    if len(unit) == 2 and (unit[1] == 'C' or unit[1] == 'F'):
        result = result + 'temperature thermometer'

    return result;

def updateData(wf):

    log.debug('Started updateing data')

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
        search_words = '';
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

        latitude = ''
        if 'latitude' in attribute.keys():
            latitude = str(attribute['latitude'])
            sys.stderr.write("latitude : " + latitude + '\n')

        longitude = ''
        if 'longitude' in attribute.keys():
            longitude = str(attribute['longitude'])      
            sys.stderr.write("longitude : " + longitude + '\n')
        

        friendly_name = item['attributes']['friendly_name']
        search_words = getSearchWords(icon, unit, state, friendly_name);

        ent = {entity_id : {'type' : ent_type, 'name' : name, 'entity_id' : entity_id, 'icon' : icon, 'friendly_name' : friendly_name, 'unit' : unit, 'state' : state, 'longitude' : longitude, 'latitude' : latitude, 'search_words' : search_words}}

        if ent_type in main.keys():
            main[ent_type].update(ent)
        else:
            main[ent_type] = dict(ent);

        if 'temperature' in item['attributes'].keys() :
            main = copyItemAndAdd(main, ent_type, entity_id, name, friendly_name, 'mdi:thermometer', '', str(item['attributes']['temperature']), 'temperature', longitude, latitude)
        if 'light_level' in item['attributes'].keys() :
            main = copyItemAndAdd(main, ent_type, entity_id, name, friendly_name, 'light-on', 'light level', str(item['attributes']['light_level']), 'light_level', longitude, latitude)
        if 'lux' in item['attributes'].keys() :
            main = copyItemAndAdd(main, ent_type, entity_id, name, friendly_name, 'light-on', 'lux', str(item['attributes']['lux']), 'lux', longitude, latitude)
        if 'battery' in item['attributes'].keys() :
            main = copyItemAndAdd(main, ent_type, entity_id, name, friendly_name, 'mdi:battery', '%', str(item['attributes']['battery']), 'battery', longitude, latitude)
    #go thur groups and store structure
    for item in main:
        wf.store_data(item, main[item])
        sys.stderr.write("item : " + str(item) + '\n')

    return 0

def main(wf):

    try:
        updateData(wf)

    except PasswordNotFound:  # API key has not yet been set
         # Nothing we can do about this, so just log it
        wf.logger.error('No Password saved')

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    wf.run(main)