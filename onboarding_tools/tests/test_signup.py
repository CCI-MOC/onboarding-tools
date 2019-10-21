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

import time

from selenium import webdriver


def test_signup(sso_session: webdriver.Remote):
    sso_session.get('https://onboarding.massopen.cloud/signup')
    sso_session.implicitly_wait(10)

    # Fill the form
    project_field = sso_session.find_element_by_name('project_name')
    project_field.send_keys('do-not-approve-automated-test')
    description_field = sso_session.find_element_by_name('description')
    description_field.send_keys('testing by onboarding-tools')
    organization_field = sso_session.find_element_by_name('organization')
    organization_field.send_keys('MOC')
    organization_role_field = sso_session.find_element_by_name('organization_role')
    organization_role_field.send_keys('Testing Automation')
    phone_field = sso_session.find_element_by_name('phone')
    phone_field.send_keys('555-555-5555')
    moc_contact_field = sso_session.find_element_by_name('moc_contact')
    moc_contact_field.send_keys('knikolla')
    time.sleep(1)

    submit = sso_session.find_element_by_xpath('//*[@id="loginBtn"]')
    submit.click()

    # Wait for it to be sent
    time.sleep(10)
