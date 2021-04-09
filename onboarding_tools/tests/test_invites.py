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

from onboarding_tools import settings


def test_login(dashboard_session: webdriver.Remote):
    dashboard_session.get('%s/management/project_users/' % settings.HORIZON_URL)

    invite_button = dashboard_session.find_element_by_xpath('//*[@id="users__action_invite"]')
    invite_button.click()

    email = dashboard_session.find_element_by_name('email')
    email.send_keys('test_')

    role = dashboard_session.find_element_by_xpath('//*[@id="id_roles_0"]')
    role.click()

    time.sleep(10)
