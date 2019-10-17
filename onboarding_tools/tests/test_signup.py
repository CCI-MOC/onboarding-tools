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

import logging
import time

import pytest
from pytest import fixture
from selenium import webdriver

from onboarding_tools import keycloak
from onboarding_tools import settings


@fixture()
def session(selenium: webdriver.Safari):
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


def test_signup(session: webdriver.Safari):
    session.get('https://onboarding.massopen.cloud/signup')
    session.implicitly_wait(10)

    # Fill the form
    project_field = session.find_element_by_name('project_name')
    project_field.send_keys('do-not-approve-automated-test')
    description_field = session.find_element_by_name('description')
    description_field.send_keys('testing by onboarding-tools')
    organization_field = session.find_element_by_name('organization')
    organization_field.send_keys('MOC')
    organization_role_field = session.find_element_by_name('organization_role')
    organization_role_field.send_keys('Testing Automation')
    phone_field = session.find_element_by_name('phone')
    phone_field.send_keys('555-555-5555')
    moc_contact_field = session.find_element_by_name('moc_contact')
    moc_contact_field.send_keys('knikolla')
    time.sleep(1)

    submit = session.find_element_by_xpath('//*[@id="loginBtn"]')
    submit.click()

    # Wait for it to be sent
    time.sleep(10)
