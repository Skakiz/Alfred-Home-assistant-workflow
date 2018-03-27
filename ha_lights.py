import home_assistant as util
import sys
import argparse
from workflow import (Workflow, ICON_WEB, ICON_INFO, ICON_WARNING, PasswordNotFound)
from workflow.background import run_in_background, is_running

def main(wf):

    ICON_LIGHT_ON = './lightbulb-on-outline.png';
    ICON_LIGHT_OFF = './lightbulb-outline.png'
	####################################################################
     # Get init data
    ####################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    password = util.getPassword(wf);
    url = util.getURL(wf);

     ####################################################################
     # Fetch all lamps to display
     ####################################################################
    if not is_running('update'):
        cmd = ['/usr/bin/python', wf.workflowfile('update_data.py')]
        run_in_background('update', cmd)

    data = util.getData(wf, 'light')

    def search_key_for_post3(post):
        """Generate a string search key for a post"""
        item = data[post]

        elements = []
        elements.append(item['name'])  # title of post
        elements.append(item['friendly_name'])
        elements.append(item['entity_id'])

        return u' '.join(elements)

    def wrapper():
        return data

    posts = wf.cached_data('allLights', wrapper, max_age=60)

    # If script was passed a query, use it to filter posts
    if args.query and data:
    	posts = wf.filter(args.query, data, key=search_key_for_post3)

    if not posts:  # we have no data to show, so show a warning and stop
        wf.add_item('No posts found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0


    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    #for post in posts:

    for post in posts:
        sys.stderr.write("post : " + str(post) + '\n')
        item = data[post];

        if item['state'] != 'unavailable':

            if item['state'] == 'on':
                ICON = ICON_LIGHT_ON
            else:
                ICON = ICON_LIGHT_OFF

            wf.add_item(title=item['friendly_name'],
                        valid=True,
                        arg=item['entity_id'],
                        #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                        icon=ICON)

    # Send the results to Alfred as XML
    wf.send_feedback()
    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))