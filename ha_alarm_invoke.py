import home_assistant as util
import icon as icon
import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound
from workflow.background import run_in_background, is_running

def main(wf):

    sys.stderr.write('in ha_alarm_invoke, query : '+ str(wf.args) + '\n')

	####################################################################
     # Check that we have an API key saved
    ####################################################################
    ##query = wf.args[0]

    password = util.getPassword(wf)
    url = util.getURL(wf)

    json = '{"entity_id": "' + wf.args[0] + '", "code" : "' + wf.args[2] + '""}'

    #if wf.args[1] == 'disarm' :
    #    result = util.post_json_to_ha(url, 'alarm_control_panel/alarm_disarm', password, json);
    #elif wf.args[1] == 'arm_home' :
    #    result = util.post_json_to_ha(url, 'alarm_control_panel/alarm_arm_home', password, json);
    #elif wf.args[1] == 'arm_away' :
    #    result = util.post_json_to_ha(url, 'alarm_control_panel/alarm_arm_away', password, json);

    cmd = ['/usr/bin/python', wf.workflowfile('update_data.py')]
    run_in_background('update', cmd)

    return 0

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))