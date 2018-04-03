import home_assistant as util
import icon as icon
import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound
from workflow.background import run_in_background, is_running

def main(wf):

    sys.stderr.write("in ha_lights_invode : \n")

	####################################################################
     # Check that we have an API key saved
    ####################################################################
    ##query = wf.args[0]
    sys.stderr.write('query : '+ str(wf.args) + '\n')

    password = util.getPassword(wf)
    url = util.getURL(wf)

    if wf.args[1] == 'off' :
        result = util.post_to_ha(url, 'light/turn_off', password, wf.args[0]);
    else :
        json = '{"entity_id": "' + wf.args[0] + '", "brightness_pct" : ' + wf.args[1] + ', "transition":"5"}'
        result = util.post_json_to_ha(url, 'light/turn_on', password, json);

    cmd = ['/usr/bin/python', wf.workflowfile('update_data.py')]
    run_in_background('update', cmd)

    return 0

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))