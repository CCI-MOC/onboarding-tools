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

import os

from keystoneauth1 import identity
from keystoneauth1 import session as ks_session
from pytest import fixture
from selenium import webdriver

from onboarding_tools import keycloak
from onboarding_tools import settings


@fixture()
def sso_session(selenium: webdriver.Remote) -> webdriver.Remote:
    sso = keycloak.KeycloakClient()
    cookies = sso.impersonate(settings.TEST_IMPERSONATE_USER).cookies
    # Note(knikolla): We must open a page in order to set cookies.
    # Doesn't have to exist, but must be in same domain as SSO.
    selenium.get('https://sso.massopen.cloud/auth/test')
    for k, v in cookies.items():
        selenium.add_cookie({
            'name': k,
            'value': v,
            'domain': 'sso.massopen.cloud'
        })
    yield selenium


@fixture()
def openstack_session() -> ks_session.Session:
    sso = keycloak.KeycloakClient()
    access_token = sso.impersonate_access_token(settings.TEST_IMPERSONATE_USER)
    openstack_auth = identity.v3.OidcAccessToken(
        auth_url='https://kaizen.massopen.cloud:13000/v3',
        identity_provider='moc',
        protocol='openid',
        access_token=access_token
    )
    return ks_session.Session(auth=openstack_auth)


@fixture()
def dashboard_session(
        openstack_session: ks_session.Session,
        selenium: webdriver.Remote) -> webdriver.Remote:
    token = openstack_session.get_token()
    selenium.get('file://' + os.path.join(settings.SCRIPT_DIR,
                                          'files',
                                          'keystone_callback.html?token=%s' % token))
