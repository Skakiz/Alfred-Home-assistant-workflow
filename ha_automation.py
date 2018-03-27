import home_assistant as util
import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

def search_key_for_post(post):
    """Generate a string search key for a post"""
    posts = post.split('.');
    sys.stderr.write('split  : '+ posts[1] + '\n')
    elements = []
    elements.append(posts[1])
    #elements.append(post['description'])  # title of post
    #elements.append(post['tags'])  # post tags
    #elements.append(post['extended'])  # description
    return u' '.join(elements)

def main(wf):

	####################################################################
     # Check that we have an API key saved
    ####################################################################
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    password = util.getPassword(wf);
    url = util.getURL(wf);

    def wrapper():
        return util.get_recent(url, 'group.all_automations', password)

    posts = wf.cached_data('allAutomation', wrapper, max_age=60)

    # If script was passed a query, use it to filter posts
    if args.query:
        posts = wf.filter(args.query, posts, key=search_key_for_post)

    if not posts:  # we have no data to show, so show a warning and stop
        wf.add_item('No posts found', icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # Loop through the returned posts and add an item for each to
    # the list of results for Alfred
    for post in posts:
        sys.stderr.write(post + '\n')
        wf.add_item(title=post,
                    valid=True,
                    arg=post,
                    #arg='https://browall.duckdns.org:8123/api/services/automation/trigger?api_password=DrumNBass1111',
                    icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()
    return 0;

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))