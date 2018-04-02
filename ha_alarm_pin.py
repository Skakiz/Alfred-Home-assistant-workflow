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
    sys.stderr.write('action : '+ str(wf.args[1]) + '\n')

    pin = ''
    if len(wf.args) == 3 :
        sys.stderr.write('pin : '+ str(wf.args[2]) + '\n')
        pin = wf.args[2]


    query = wf.args[0].split(' ')

    data = util.getData(wf, 'alarm_control_panel')
    item = data[wf.args[0]]

    res = [{'name' : 'Enter Pin Code and press <Enter>'}];

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    #for post in posts:

    for post in res:
        sys.stderr.write("post : " + str(post) + '\n')

        wf.add_item(title=post['name'],
                    subtitle='',
                    valid=True,
                    arg=wf.args[0] + ' ' + wf.args[1] + ' ' + pin , 
                    #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                    icon=icon.getIcon('mdi:alarm','w'))

        # Send the results to Alfred as XML
    wf.send_feedback()

    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))