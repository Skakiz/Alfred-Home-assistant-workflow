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
    password = util.getPassword(wf);
    url = util.getURL(wf);

     ####################################################################
     # Fetch all data in background if the query is empty
     ####################################################################

    sys.stderr.write('query : '+ str(wf.args) + '\n')
    sys.stderr.write('el : '+ str(wf.args[0]) + '\n')

    query = wf.args[0].split(' ')

    data = util.getData(wf, 'alarm_control_panel')
    item = data[wf.args[0]]

    def search_key_for_post(post):
        elements = []
        elements.append(post['name']) 
        elements.append(post['value']) 
        return u' '.join(elements)

    # If script was passed a query, use it to filter posts
    if item['state'] == 'disarmed':
        res = [{'name' : 'Arm home', 'value' : 'arm_home'},
                {'name' : 'Arm away', 'value' : 'arm_away'}]
    else :
        res = [{'name' : 'Disarmed', 'value' : 'disarmed'}];

    if not res:  # we have no data to show, so show a warning and stop
        wf.add_item('No posts found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    #for post in posts:

    for post in res:
        sys.stderr.write("post : " + str(post) + '\n')

        wf.add_item(title=post['name'],
                    subtitle='',
                    valid=True,
                    arg=wf.args[0] + " " + post['value'],
                    #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                    icon=icon.getIcon('mdi:alarm','w'))

        # Send the results to Alfred as XML
    wf.send_feedback()

    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))