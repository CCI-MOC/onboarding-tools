# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib

from onboarding_tools import settings

import requests


class KeycloakClient(object):
    def __init__(self):
        self.session = requests.session()
        self._admin_auth()

    @staticmethod
    def construct_url(realm, path):
        return f'{settings.KEYCLOAK_URL}/auth/admin/realms/{realm}/{path}'

    @property
    def url_base(self):
        return f'{settings.KEYCLOAK_URL}/auth/admin/realms'

    @staticmethod
    def auth_endpoint(realm):
        return f'{settings.KEYCLOAK_URL}/auth/realms/{realm}/protocol/openid-connect/auth'

    @staticmethod
    def token_endpoint(realm):
        return f'{settings.KEYCLOAK_URL}/auth/realms/{realm}/protocol/openid-connect/token'

    def _admin_auth(self):
        params = {
            'grant_type': 'password',
            'client_id': 'admin-cli',
            'username': settings.KEYCLOAK_USERNAME,
            'password': settings.KEYCLOAK_PASSWORD,
            'scope': 'openid',
        }
        r = requests.post(self.token_endpoint('master'), data=params).json()
        headers = {
            'Authorization': ("Bearer %s" % r['access_token']),
            'Content-Type': 'application/json'
        }
        self.session.headers.update(headers)
        return r

    def get_user_id(self, username):
        self._admin_auth()
        r = self.session.get(self.construct_url('master', f'users?username={username}')).json()
        return r[0]['id']

    def impersonate(self, user):
        self._admin_auth()
        user = self.get_user_id(user)
        return self.session.post(self.construct_url('master', f'users/{user}/impersonation'))

    def impersonate_access_token(self, user):
        user_session = requests.session()
        user_session.cookies.update(self.impersonate(user).cookies)
        params = {
            'response_mode': 'fragment',
            'response_type': 'token',
            'client_id': settings.OIDC_CLIENT_ID,
            'client_secret': settings.OIDC_CLIENT_SECRET,
            'redirect_uri': settings.OPENSTACK_KEYSTONE_URL,
        }
        response = user_session.get(self.auth_endpoint('master'), params=params, allow_redirects=False)
        redirect = response.headers['Location']
        token = urllib.parse.parse_qs(redirect)['access_token'][0]
        return token

    def create_user(self, email, first_name, last_name):
        self._admin_auth()
        data = {
            'username': email,
            'email': email,
            'firstName': first_name,
            'lastName': last_name,
            'enabled': True,
            'emailVerified': True,
            'requiredActions': []
        }
        return self.session.post(self.construct_url('users'), json=data)

    def get_client(self, realm, client_id):
        self._admin_auth()
        r = self.session.get(f'{self.url_base}/{realm}/clients?clientId={client_id}').json()
        return r

    def create_client(self, realm, client_id, client_secret, redirect_uris):
        self._admin_auth()
        data = {
                'clientId': client_id,
                'secret': client_secret,
                'redirectUris': redirect_uris,
                'implicitFlowEnabled': True,
        }
        return self.session.post(self.construct_url(realm, 'clients'), json=data)
