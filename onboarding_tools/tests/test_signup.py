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
import uuid

from selenium import webdriver

from onboarding_tools.tests import base
from onboarding_tools import settings


class TestSignup(base.TestBase):

    def test_signup(self, selenium: webdriver.Remote):
        s = self.get_sso_session(selenium)

        project_name = 'automated-test-%s' % uuid.uuid4().hex

        s.get('%s/signup' % settings.HORIZON_URL)
        s.implicitly_wait(10)

        # Fill the form
        project_field = s.find_element_by_name('project_name')
        project_field.send_keys(project_name)
        description_field = s.find_element_by_name('description')
        description_field.send_keys('testing by onboarding-tools')
        organization_field = s.find_element_by_name('organization')
        organization_field.send_keys('MOC')
        organization_role_field = s.find_element_by_name('organization_role')
        organization_role_field.send_keys('Testing Automation')
        phone_field = s.find_element_by_name('phone')
        phone_field.send_keys('555-555-5555')
        moc_contact_field = s.find_element_by_name('moc_contact')
        moc_contact_field.send_keys('test')
        time.sleep(1)

        submit = s.find_element_by_xpath('//*[@id="loginBtn"]')
        submit.click()

        success = s.find_element_by_class_name('panel-body')
        assert 'Your signup request has been submitted.' in success.text
