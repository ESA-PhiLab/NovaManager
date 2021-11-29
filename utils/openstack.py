import os

import keystoneclient.auth.identity as keystone_identity
import keystoneclient.client as keystone_client
import keystoneauth1.session as keystone_session

import glanceclient.client as glance_client
import novaclient.client as nova_client


class OpenstackAuth:
    def __init__(self):
        username = os.getenv("OS_USERNAME")
        password = os.getenv("OS_PASSWORD")
        project_id = os.getenv("OS_PROJECT_ID")
        project_domain_id = os.getenv("OS_PROJECT_DOMAIN_ID")
        project_domain_name = os.getenv("OS_USER_DOMAIN_NAME")
        project_name = os.getenv("OS_PROJECT_NAME")
        # region_name = os.getenv("OS_REGION_NAME")
        user_domain_name = os.getenv("OS_USER_DOMAIN_NAME")
        auth_url = os.getenv("OS_AUTH_URL")

        auth = keystone_identity.v3.Password(
            auth_url=auth_url,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            project_id=project_id,
            project_name=project_name,
            user_domain_name=user_domain_name,
            username=username,
        )

        # establish a keystone session
        self.sess = keystone_session.Session(auth=auth)
        #
        # # get a keystone client
        self.kc = keystone_client.Client(
            "3", session=self.sess, auth_url=self.sess.auth.auth_url
        )
        #
        # # and authenticate it
        self.kc.authenticate(
            token=self.sess.get_auth_headers()["X-Auth-Token"],
            project_id=self.sess.get_project_id(),
            tenant_id=self.sess.get_project_id(),
        )


class AuthenticatedNovaClient:
    def __init__(self, auth: OpenstackAuth = None):
        if not auth:
            auth = OpenstackAuth()
        self.nc = nova_client.Client("2", session=auth.sess)


class AuthenticatedGlanceClient:
    def __init__(self, auth: OpenstackAuth = None):
        if not auth:
            auth = OpenstackAuth()
        self.gc = glance_client.Client(
            "2",
            endpoint=auth.kc.service_catalog.url_for(
                service_type="image", endpoint_type="publicURL"
            ),
            token=auth.sess.get_auth_headers()["X-Auth-Token"],
        )
