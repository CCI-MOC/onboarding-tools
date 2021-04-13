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


class TestInvites(base.TestBase):

    def test_invite(self, selenium: webdriver.Remote):
        invitee = self.setup_user()

        dashboard_session = self.get_dashboard_session(selenium)
        dashboard_session.get(f'{settings.HORIZON_URL}/management/project_users/')

        invite_button = dashboard_session.find_element_by_xpath('//*[@id="users__action_invite"]')
        invite_button.click()

        dashboard_session.implicitly_wait(5)
        email = dashboard_session.find_element_by_name('email')
        email.send_keys(invitee)

        role = dashboard_session.find_element_by_xpath('//*[@id="id_roles_0"]')
        role.click()

        submit_button = dashboard_session.find_element_by_xpath('//*[@id="invite_user_form"]/div[2]/button')
        submit_button.click()

        success = dashboard_session.find_element_by_xpath('//*[@id="main_content"]/div[1]/div/p/strong')
        assert 'success' in success.text.lower()
