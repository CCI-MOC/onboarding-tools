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
from urllib import parse

from adjutantclient.v1 import client as adjutant_client
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
    selenium.get(f'{settings.KEYCLOAK_URL}/auth/test')
    for k, v in cookies.items():
        selenium.add_cookie({
            'name': k,
            'value': v,
            'domain': parse.urlparse(settings.KEYCLOAK_URL).netloc.split(':')[0]
        })
    yield selenium


@fixture()
def openstack_session() -> ks_session.Session:
    sso = keycloak.KeycloakClient()
    access_token = sso.impersonate_access_token(settings.TEST_IMPERSONATE_USER)
    openstack_auth = identity.v3.OidcAccessToken(
        auth_url=settings.OPENSTACK_KEYSTONE_URL,
        identity_provider=settings.OPENSTACK_IDP,
        protocol='openid',
        access_token=access_token
    )
    yield ks_session.Session(auth=openstack_auth)


@fixture()
def dashboard_session(
        openstack_session: ks_session.Session,
        selenium: webdriver.Remote) -> webdriver.Remote:
    token = openstack_session.get_token()
    horizon_endpoint = f'{settings.HORIZON_URL}/auth/websso/'
    selenium.get('file://' + os.path.join(settings.SCRIPT_DIR,
                                          'files',
                                          f'keystone_callback.html?token={token}&action={horizon_endpoint}'))

    selenium.implicitly_wait(10)
    selenium.find_element_by_xpath('//*[@id="content_body"]/div[1]/div/div/div[2]/h1')
    yield selenium


@fixture()
def adjutant_session(openstack_session) -> adjutant_client.Client:
    yield adjutant_client.Client(session=openstack_session)
