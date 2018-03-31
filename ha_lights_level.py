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
    #parser = argparse.ArgumentParser()
    #parser.add_argument('query', nargs='?', default=None)
    #args = parser.parse_args(wf.args)

    password = util.getPassword(wf);
    url = util.getURL(wf);

     ####################################################################
     # Fetch all data in background if the query is empty
     ####################################################################

    sys.stderr.write('query : '+ str(wf.args) + '\n')
    sys.stderr.write('el : '+ str(wf.args[0]) + '\n')

    query = wf.args[0].split(' ')



    sys.stderr.write('in : '+ '\n')
    
    level = '';
    if len(wf.args) == 2 :
        level = wf.args[1]


    def search_key_for_post(post):
        elements = []
        elements.append(post['name']) 
        elements.append(post['value']) 
        return u' '.join(elements)

    def wrapper():
        data = [{'name' : 'Off', 'value' : 'off'},
                {'name' : 'max', 'value' : '100'},
                {'name' : '90%', 'value' : '90'},
                {'name' : '80%', 'value' : '80'},
                {'name' : '70%', 'value' : '70'}, 
                {'name' : '60%', 'value' : '60'}, 
                {'name' : '50%', 'value' : '50'},
                {'name' : '40%', 'value' : '40'},
                {'name' : '30%', 'value' : '30'},
                {'name' : '20%', 'value' : '20'}, 
                {'name' : '10%', 'value' : '10'}, 
                {'name' : 'min', 'value' : '0'}]
        return data

    posts = wf.cached_data('allLightLevels', wrapper, max_age=60)

    # If script was passed a query, use it to filter posts
    if level:
        res = wf.filter(level, posts, key=search_key_for_post, min_score=20)
    else :
        res = posts;

    if not res:  # we have no data to show, so show a warning and stop
        wf.add_item('No posts found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0


    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    #for post in posts:

    for post in res:
        sys.stderr.write("post : " + str(post) + '\n')

        if post['value'] == 'off' :
            v_icon = icon.getIcon('light-off','w')
        else : 
            v_icon = icon.getIcon('light-on','w')

        wf.add_item(title=post['name'],
                    subtitle='',
                    valid=True,
                    arg=wf.args[0] + " " + post['value'],
                    #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                    icon=v_icon)

        # Send the results to Alfred as XML
    wf.send_feedback()

    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))