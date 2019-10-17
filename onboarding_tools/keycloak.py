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

import json

from onboarding_tools import settings

import requests


class KeycloakClient(object):
    def __init__(self):
        self.session = requests.session()
        self._admin_auth()

    def _admin_auth(self):
        params = {
            'grant_type': 'password',
            'client_id': 'admin-cli',
            'username': settings.KEYCLOAK_USERNAME,
            'password': settings.KEYCLOAK_PASSWORD,
            'scope': 'openid',
        }
        r = requests.post(settings.KEYCLOAK_TOKEN_URL, data=params)
        r = json.loads(r.text)
        headers = {
            'Authorization': ("Bearer %s" % r['access_token']),
            'Content-Type': 'application/json'
        }
        self.session.headers.update(headers)

    def get_user_id(self, email):
        self._admin_auth()
        r = self.session.get('https://sso.massopen.cloud/auth/admin/realms/moc/users?email=%s' % email)
        r = json.loads(r.text)
        return r[0]['id']

    def impersonate(self, user):
        self._admin_auth()
        user = self.get_user_id(user)
        auth_url = "https://sso.massopen.cloud/auth/admin/realms/moc/users/%s/impersonation" % user
        return self.session.post(auth_url)




