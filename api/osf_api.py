import json
import requests
from pythosf import client

#TODO: Possibly make an OSF api object and save session on it

def create_project(session, title='osf selenium test'):
    node = client.Node(session=session)
    node.create(title=title)
    return node

def upload_quickfile(session, quickfile, user=None, query_parameters = {}):
    if not user:
        user = current_user(session)
    quickfiles_url = user.relationships.quickfiles['links']['upload']['href']
    upload_query_parameters = {
        'kind': 'file',
        'name': quickfile.name.split('/')[-1]
    }
    combined_query_parameters = {**query_parameters, **upload_query_parameters}
    #TODO: Why is it mad at me for excluding item_id and type
    return session.put(url=quickfiles_url, item_id=None, item_type='File', query_parameters=combined_query_parameters, raw_body=quickfile, token=session.token)


# Current_user only actually returns the current user if the token
# and the login information actually match up - so please don't mess it up
def current_user(session):
    user = User(session=session)
    user.get()
    return user

#TODO: Rewrite these things so they can come from pythosf
def get_user_institutions(session, user=None):
    if not user:
        user = current_user(session)
    institution_url = user.relationships.institutions['links']['related']['href']
    data = session.get(institution_url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def get_all_institutions(session):
    url = '/v2/institutions/'
    data = session.get(url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions

def delete_all_user_projects(session, user=None):
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    data = session.get(nodes_url)
    for node in data['data']:
        n = client.Node(id=node['id'], session=session)
        n.get()
        n.delete()


class User(client.APIDetail):
    def __init__(self, session, id=None, self_link=None, data=None):
        super().__init__(session=session, data=data)
        if not data:
            self.id = id
            self.type = 'users'
            self.links = None
            self.meta = None
            self.self_link = self_link
        self.providers = []


    def get(self, query_parameters=None, token=None):
        url = '/v2/users/me/'
        if self.self_link:
            url = self.self_link
        elif self.links:
            url = self.links.self
        elif self.id:
            url = '/v2/users/{}/'.format(self.id)


        response = self.session.get(url=url, query_parameters=query_parameters, token=token)
        if response:
            self._update(response=response)
        else:
            raise ValueError("No url or id to get. Set the id or self_link then try to get.")
