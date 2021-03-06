import home_assistant as util
import icon as icon
import sys
import argparse
from workflow import (Workflow, ICON_WEB, ICON_INFO, ICON_WARNING, PasswordNotFound)
from workflow.background import run_in_background, is_running

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
     # Fetch all data in background if the query is empty
     ####################################################################
    if args.query == None:
        if not is_running('update'):
            cmd = ['/usr/bin/python', wf.workflowfile('update_data.py')]
            run_in_background('update', cmd)

    data = util.getData(wf, 'alarm_control_panel')

    def search_key_for_post(post):
        """Generate a string search key for a post"""
        item = data[post]

        elements = []
        elements.append(item['friendly_name'])
        elements.append(item['entity_id'])

        return u' '.join(elements)

    def wrapper():
        return data

    posts = wf.cached_data('allAAlarms', wrapper, max_age=1)

    # If script was passed a query, use it to filter posts
    if args.query and data:
        posts = wf.filter(args.query, data, key=search_key_for_post, min_score=20)

    if not posts:  # we have no data to show, so show a warning and stop
        wf.add_item('No posts found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Action this item to install the update',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    #for post in posts:

    for post in posts:
        sys.stderr.write("post : " + str(post) + '\n')
        item = data[post];
        subtitle = '<Enter> to select alarm'

        wf.add_item(title=item['friendly_name'],
                    subtitle=subtitle,
                    valid=True,
                    arg=item['entity_id'],
                    #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                    icon=icon.getIcon('mdi:alarm','w'))

    # Send the results to Alfred as XML
    wf.send_feedback()
    return 0;

if __name__ == '__main__':
    wf = Workflow(update_settings={
                # Your username and the workflow's repo's name
                'github_slug': 'Skakiz/Alfred-Home-assistant-workflow',
                # Optional number of days between checks for updates
                'frequency': 7
                })
    log = wf.logger
    sys.exit(wf.run(main))