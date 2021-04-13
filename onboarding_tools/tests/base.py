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

import uuid
from urllib import parse

from keystoneauth1 import identity
from keystoneauth1 import session as ks_session

from selenium import webdriver

from onboarding_tools import keycloak
from onboarding_tools import settings


class TestBase(object):

    def setup_method(self):
        self.keycloak = keycloak.KeycloakClient()

    def teardown_method(self):
        pass

    def get_sso_session(
            self,
            selenium: webdriver.Remote,
            impersonate_user=settings.TEST_IMPERSONATE_USER
    ) -> webdriver.Remote:

        cookies = self.keycloak.impersonate(impersonate_user).cookies
        # Note(knikolla): We must open a page in order to set cookies.
        # Doesn't have to exist, but must be in same domain as SSO.
        selenium.get(f'{settings.KEYCLOAK_URL}/auth/test')
        for k in [x for x in cookies.keys() if 'KEYCLOAK' in x]:
            selenium.add_cookie({
                'name': k,
                'value': cookies[k],
                'domain': parse.urlparse(settings.KEYCLOAK_URL).netloc.split(':')[0],
            })

        selenium.get(f'{settings.KEYCLOAK_URL}/auth/realms/master/account/')

        selenium.implicitly_wait(5)
        username = selenium.find_element_by_xpath('//*[@id="username"]')
        assert username.get_attribute('value') == impersonate_user
        return selenium

    def get_openstack_session(
            self,
            impersonate_user=settings.TEST_IMPERSONATE_USER
    ) -> ks_session.Session:
        access_token = self.keycloak.impersonate_access_token(impersonate_user)
        openstack_auth = identity.v3.OidcAccessToken(
            auth_url=settings.OPENSTACK_KEYSTONE_URL,
            identity_provider=settings.OPENSTACK_IDP,
            protocol='openid',
            access_token=access_token
        )
        return ks_session.Session(auth=openstack_auth)

    def get_dashboard_session(
            self,
            selenium: webdriver.Remote,
            impersonate_user=settings.TEST_IMPERSONATE_USER
    ) -> webdriver.Remote:
        sso_session = self.get_sso_session(selenium, impersonate_user)
        sso_session.get(f'{settings.HORIZON_URL}/signup/')

        horizon_endpoint = f'{settings.HORIZON_URL}/auth/websso/'
        sso_session.get(f'{settings.OPENSTACK_KEYSTONE_URL}/auth/OS-FEDERATION'
                        f'/identity_providers/{settings.OPENSTACK_IDP}'
                        f'/protocols/openid/websso?origin={horizon_endpoint}')

        sso_session.find_element_by_xpath('//*[@id="content_body"]/div[1]/div/div/div[2]/h1')
        return sso_session

    def setup_user(self, email=None):
        email = email if email else f'test-{uuid.uuid4().hex}@example.com'
        self.keycloak.create_user('master', email, 'Test', 'User')
        return email
