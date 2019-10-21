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
import os

logging.basicConfig(level=logging.INFO)

KEYCLOAK_TOKEN_URL = os.environ.get('KEYCLOAK_TOKEN_URL')
KEYCLOAK_USERNAME = os.environ.get('KEYCLOAK_USERNAME')
KEYCLOAK_PASSWORD = os.environ.get('KEYCLOAK_PASSWORD')

ONBOARDING_UI_PATH = os.environ.get('ONBOARDING_UI_PATH')
ONBOARDING_UI_VERSION = os.environ.get('ONBOARDING_UI_VERSION')
ONBOARDING_UI_IMAGE = "massopencloud/horizon-onboarding:r%s" % ONBOARDING_UI_VERSION

HORIZON_URL = os.environ.get('HORIZON_URL')
OPENSTACK_KEYSTONE_URL = os.environ.get('OPENSTACK_KEYSTONE_URL')
OPENSTACK_REGISTRATION_URL = os.environ.get('OPENSTACK_REGISTRATION_URL')
OIDC_METADATA_URL = os.environ.get('OIDC_METADATA_URL')
OIDC_CLIENT_ID = os.environ.get('OIDC_CLIENT_ID')
OIDC_CLIENT_SECRET = os.environ.get('OIDC_CLIENT_SECRET')

TEST_IMPERSONATE_USER = os.environ.get('TEST_IMPERSONATE_USER')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
