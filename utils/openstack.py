import abc
import os
import logging

import keystoneclient
import keystoneauth1
import glanceclient
import novaclient


class OpenstackAuthenticator:
    def __init__(self):
        self.auth_url = os.getenv("OS_AUTH_URL")
    
    @abc.abstractmethod
    def authenticate(self):
        self.session = keystoneauth1.session.Session(auth=self._auth())
        keystoneauth1.session.Session

    @abc.abstractmethod
    def _auth(self):
        pass

    @staticmethod
    def get_authenticator():
        authenticator_class_name = __class__.__name__ + os.getenv("OS_AUTHENTICATOR_CLASS")
        try:
            authenticator_class = globals()[authenticator_class_name]
            return authenticator_class()
        except AttributeError:
            logging.error('Authenticator class %s does not exist.' % authenticator_class_name)
            raise


class OpenstackAuthenticatorPassword(OpenstackAuthenticator):
    def __init__(self):
        super().__init__()
        self.username = os.getenv("OS_USERNAME")
        self.password = os.getenv("OS_PASSWORD")
        self.project_id = os.getenv("OS_PROJECT_ID")
        self.project_name = os.getenv("OS_PROJECT_NAME")
        self.project_domain_id = os.getenv("OS_PROJECT_DOMAIN_ID")
        self.project_domain_name = os.getenv("OS_PROJECT_DOMAIN_NAME")
        self.user_domain_name = os.getenv("OS_USER_DOMAIN_NAME")

    def _auth(self):
        return keystoneclient.auth.identity.v3.Password(
            auth_url=self.auth_url,
            username=self.username,
            password=self.password,
            project_id=self.project_id,
            project_name=self.project_name,
            project_domain_id=self.project_domain_id,
            project_domain_name=self.project_domain_name,
            user_domain_name=self.user_domain_name,
        )

    def authenticate(self):
        super().authenticate()

        # get a keystone client
        self.kc = keystoneclient.client.Client("3", session=self.session, auth_url=self.session.auth.auth_url)

        # and authenticate it
        self.kc.authenticate(
            token=self.sess.get_auth_headers()["X-Auth-Token"],
            project_id=self.session.get_project_id(),
            tenant_id=self.session.get_project_id(),
        )


class OpenstackAuthenticatorApplicationCredentials(OpenstackAuthenticator):
    def __init__(self):
        super().__init__()
        self.app_id = os.getenv("OS_APPLICATION_CREDENTIAL_ID")
        self.app_secret = os.getenv("OS_APPLICATION_CREDENTIAL_SECRET")

    def _auth(self):
        application_credential = keystoneauth1.identity.v3.ApplicationCredentialMethod(
                application_credential_id=self.app_id,
                application_credential_secret=self.app_secret,
        )
        return keystoneauth1.identity.v3.Auth(
                auth_url=self.auth_url,
                auth_methods=[application_credential]
        )
    
    def authenticate(self):
        super().authenticate()

        # get a keystone client
        self.kc = keystoneclient.v3.client.Client(session=self.session)        


class AuthenticatedClient():
    def __init__(self, authenticator: OpenstackAuthenticator = None):
        self.authenticator = authenticator or OpenstackAuthenticator.get_authenticator()
        self.authenticator.authenticate()
        self.client = self.create_client()

    @abc.abstractmethod
    def create_client(self):
        pass


class AuthenticatedNovaClient(AuthenticatedClient):
    def create_client(self):
        return novaclient.client.Client("2", session=self.authenticator.session)


class AuthenticatedGlanceClient(AuthenticatedClient):
    def create_client(self):
        return glanceclient.client.Client(
            "2",
            endpoint=self.authenticator.session.get_endpoint(service_type="image", endpoint_type="publicURL"),
            session=self.authenticator.session,
            #token=self.authenticator.session.get_auth_headers()["X-Auth-Token"],
        )
