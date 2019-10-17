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
import uuid

from onboarding_tools import settings

import docker

DOCKER = docker.client.from_env()
LOG = logging.getLogger()

CONTAINERS = []


def build_ui():
    LOG.info('Onboarding Image Build - Starting')
    DOCKER.images.build(
        path=settings.ONBOARDING_UI_PATH,
        tag=settings.ONBOARDING_UI_IMAGE,
        pull=True,
    )
    LOG.info('Onboarding Image Build - Finished')


def run_ui():
    LOG.info('Pulling Memcached')
    DOCKER.images.pull('memcached:1.5.19')
    LOG.info('Running Memcached')
    memcached = DOCKER.containers.run(
        name='horizon-memcached-%s' % uuid.uuid4().hex,
        image='memcached:1.5.19',
        detach=True,
    )
    CONTAINERS.append(memcached)

    LOG.info('Running %s' % settings.ONBOARDING_UI_IMAGE)
    horizon = DOCKER.containers.run(
        name='horizon-onboarding-%s' % uuid.uuid4().hex,
        image=settings.ONBOARDING_UI_IMAGE,
        environment={
            'HORIZON_URL': settings.HORIZON_URL,
            'OPENSTACK_KEYSTONE_URL': settings.OPENSTACK_KEYSTONE_URL,
            'OPENSTACK_REGISTRATION_URL': settings.OPENSTACK_REGISTRATION_URL,
            'OIDC_METADATA_URL': settings.OIDC_METADATA_URL,
            'OIDC_CLIENT_ID': settings.OIDC_CLIENT_ID,
            'OIDC_CLIENT_SECRET': settings.OIDC_CLIENT_SECRET,
        },
        links={memcached.name: 'horizon-memcached'},
        ports={'8080/tcp': '8080'},
        detach=True,
    )
    CONTAINERS.append(horizon)


def cleanup():
    for container in CONTAINERS:
        LOG.info('Removing %s' % container.name)
        container.remove(force=True)


def setup():
    build_ui()
    run_ui()
    cleanup()


if __name__ == '__main__':
    setup()
