from threading import Timer

from urllib.request import urlopen
import json

import dateutil.parser
from datetime import datetime

import re


def get_rest_json(url):
    response = urlopen(url)
    body = response.read().decode('utf-8')
    return (json.loads(body), response)


def event_cmp(event):
    time = dateutil.parser.parse(event['created_at'])

    return int(time.strftime("%s"))


class GitLabBot():

    PRIVATE_TOKEN = ''
    PROJECTS_URL = 'https://gitlab.stusta.mhn.de/api/v3/projects/?private_token=%s&per_page=100&page=%s'
    EVENTS_URL = 'https://gitlab.stusta.mhn.de/api/v3/projects/%s/events?private_token=%s'


    ISSUE_URL = '%s/issues/%s'
    MERGE_REQUEST_URL = '%s/merge_requests/%s'

    def __init__(self, bot):
        self.bot = bot
        self.all_projects = {}

        self.PRIVATE_TOKEN = self.bot.config.GITLAB_PRIVATE_TOKEN

        for project in self.get_project_list():
            self.all_projects[project['id']] = project

        bot.respond('list gitlab projects', self.list_projects)


    def start(self):
        Timer(10, self.check_for_changes).start()


    def get_project_list(self):
        projects = []
        page = 1

        while True:
            (projects_patch, response) = get_rest_json(self.PROJECTS_URL % (self.PRIVATE_TOKEN, page))

            projects.extend([project
                                for project in projects_patch
                                if project['namespace']['name'] == 'stustanet'])

            if int(response.getheader('X-Total-Pages')) <= page:
                break
            else:
                page += 1

        return projects


    def list_projects(self, bot, msg, match):

        bot.send_message(', '.join([self.all_projects[id]['name'] for id in self.all_projects]), msg['from'].bare)


    def check_for_changes(self):
        projects = self.get_project_list()

        for project in projects:
            project_id = project['id']

            last_activity_at_new = dateutil.parser.parse(project['last_activity_at'])
            last_activity_at_old = last_activity_at_new

            if self.all_projects.get(project_id) is not None:
                last_activity_at_old = dateutil.parser.parse(self.all_projects[project_id]['last_activity_at'])
            else:

                self.all_projects[project_id] = project
                (events, response) = self.get_rest_json(self.EVENTS_URL % (project['id'], self.PRIVATE_TOKEN))
                evens = sorted(evens, key=event_cmp)

                for event in events:
                    formatted_event = self.format_event(event, project)
                    if formatted_event is not None:
                        self.bot.send_message(formatted_event)

                continue

            newer = last_activity_at_new > last_activity_at_old
            if newer:
                self.get_project_changes(self.all_projects[project_id])
                self.all_projects[project_id] = project

        Timer(10, self.check_for_changes).start()


    def get_project_changes(self, project):
        last_activity_at = dateutil.parser.parse(project['last_activity_at'])

        def newest(event):
            created_at = dateutil.parser.parse(event['created_at'])
            return created_at > last_activity_at

        (events, response) = get_rest_json(self.EVENTS_URL % (project['id'], self.PRIVATE_TOKEN))
        newest = [event for event in events if newest(event)]
        newest = sorted(newest, key=event_cmp)

        if len(newest) > 0:
            for event in newest:
                formatted_event = self.format_event(event, project)
                if formatted_event is not None:
                    self.bot.send_message(formatted_event)
        else:
            print('%s updated but no events!' % project['name'])


    def format_event(self, event, project):
        author = event['author']['name']
        name = project['name']
        action = event['action_name']
        url = project['web_url']

        if action in [ 'pushed new', 'pushed to' ]:
            commit_count = int(event['data']['total_commits_count'])
            if commit_count > 0:
                commits = ('%s commit' if commit_count == 1 else '%s commits') % commit_count

                text = ','.join([ re.sub('[\r\n]+', ';', commit['message'])
                                    for commit in event['data']['commits']])

                return '%s pushed %s to %s: %s (%s)' % (author, commits, name, text, url)

        elif action in [ 'opened', 'closed' ]:
            event_type = 'stuff'
            title = event['target_title']

            if event['target_type'] == 'MergeRequest':
                event_type = 'merge request'
                url = self.MERGE_REQUEST_URL % (url, event['target_id'])
            elif event['target_type'] == 'Issue':
                event_type = 'issue'
                url = self.ISSUE_URL % (url, event['target_id'])

            return '%s %s %s for %s: %s (%s)' % (author, action, event_type, title, name, url)

        elif action == 'created':
            return '%s created a new project %s (%s)' % (author, name, url)

        print(event)

        return None



def register(bot):

    gitLabBot = GitLabBot(bot)
    gitLabBot.start()
