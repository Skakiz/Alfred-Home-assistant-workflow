import home_assistant as util
import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

def main(wf):

	####################################################################
     # Check that we have an API key saved
    ####################################################################
    ##query = wf.args[0]
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    password = util.getPassword(wf)
    url = util.getURL(wf)
    
    sys.stderr.write('Trigger lights : ' + args.query + '\n')
    result = util.post_to_ha(url, 'light/toggle', password, args.query);

    util.updateData(wf)

    return result

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))