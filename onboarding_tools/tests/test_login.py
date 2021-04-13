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

from selenium import webdriver

from onboarding_tools.tests import base


class TestLogin(base.TestBase):

    def test_sso_login(self, selenium: webdriver.Remote):
        user = self.setup_user()
        self.get_sso_session(selenium, impersonate_user=user)

    def test_openstack_session(self):
        user = self.setup_user()
        s = self.get_openstack_session(user)
        s.get_token()
