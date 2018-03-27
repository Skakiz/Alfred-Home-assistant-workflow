import home_assistant as util
import sys
import argparse
import json
from workflow import (Workflow, ICON_WEB, ICON_INFO, ICON_WARNING, PasswordNotFound)
#from workflow.background import run_in_background, is_running

def search_key_for_post(post):
    """Generate a string search key for a post"""

    item = data[post]

    return '{} {}'.format(item['friendly_name'], item['name'])

    #elements = []
    #elements.append(post['name'])  # title of post
    #elements.append(post['friendly_name'])
    #elements.append(post['tags'])  # post tags
    #elements.append(post['extended'])  # description
    #return u' '.join(elements)

def main(wf):

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
    #cmd = ['/usr/bin/python', wf.workflowfile('update_data.py allLights')]
    #run_in_background('update', cmd)

    # Notify the user if the cache is being updated
    #if is_running('update'):
    #    wf.add_item('Getting entities from Home Assistant',
    #                valid=False,
    #                icon=ICON_INFO)

    data = util.getData(wf, 'light')

    def search_key_for_post3(post):
        """Generate a string search key for a post"""
        item = data[post]

        #sys.stderr.write('item :  ' + str(item) + '\n')

        elements = []
        elements.append(item['name'])  # title of post
        elements.append(item['friendly_name'])

        return u' '.join(elements)

    def wrapper():
        return data

    posts = wf.cached_data('allLights', wrapper, max_age=60)

    #sys.stderr.write('args.query : ' + str(args.query) +  '\n')
    #sys.stderr.write('posts : ' + str(posts) +  '\n')

    #result = []
    #for post in posts:
        #result.append(posts[post])

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
            wf.add_item(title=item['friendly_name'],
                        valid=True,
                        arg=item['name'],
                        #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                        icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()
    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))