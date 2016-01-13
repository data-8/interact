"""

Authenticator
original from the JupyterHub repository
https://github.com/jupyter/nbgrader/blob/master/nbgrader/auth/hubauth.py

"""
import json
import logging
import os
import requests
from flask import request, redirect, abort, current_app


class HubAuth:
    """Jupyter hub authenticator."""

    def __init__(self):
        self.config = current_app.config
        self.log = logging.getLogger('interact')

        # base url for the website
        self.hub_base_url = self.config['BASE_URL']
        self._hubapi_base_url = self.config['BASE_URL']

        # token for JupyterHub API
        self.hubapi_token = self.config['API_TOKEN']

        # where to send authenticated users
        self.remap_url = self.config['URL']

        # cookie?
        self.hubapi_cookie = self.config['COOKIE']

    def _hubapi_request(self, *args, **kwargs):
        """Makes an API request to the local JupyterHub installation"""
        return self._request('hubapi', *args, **kwargs)

    def _request(self, service, relative_path, method='GET', body=None):
        base_url = getattr(self, '_%s_base_url' % service)
        token = getattr(self, '%s_token' % service)

        data = body
        if isinstance(data, (dict,)):
            data = json.dumps(data)

        return requests.request(method, base_url + relative_path, headers={
            'Authorization': 'token %s' % token
        }, data=data)

    def authenticate(self):
        """Authenticate a request.
        Returns username or flask redirect."""

        if self.config['DEBUG'] or self.config['TESTING']:
            return 'sample_username'

        # If auth cookie doesn't exist, redirect to the login page with
        # next set to redirect back to the this page.
        if self.hubapi_cookie not in request.cookies:
            return redirect(self.hub_base_url + '/hub?next=' + self.remap_url)
        cookie = request.cookies[self.hubapi_cookie]

        # Check with the Hub to see if the auth cookie is valid.
        response = self._hubapi_request('/hub/api/authorizations/cookie/' + self.hubapi_cookie + '/' + cookie)
        if response.status_code == 200:

            #  Auth information recieved.
            data = response.json()
            if 'name' in data:
                return data['name']

            # this shouldn't happen, but possibly might if the JupyterHub API
            # ever changes
            else:
                self.log.warn('Malformed response from the JupyterHub auth API.')
                abort(500, "Failed to check authorization, malformed response from Hub auth.")

        # this will happen if the JPY_API_TOKEN is incorrect
        elif response.status_code == 403:
            self.log.error("I don't have permission to verify cookies, my auth token may have expired: [%i] %s", response.status_code, response.reason)
            abort(403, "Permission failure checking authorization, I may need to be restarted")

        # this will happen if jupyterhub has been restarted but the user cookie
        # is still the old one, in which case we should reauthenticate
        elif response.status_code == 404:
            self.log.warn("Failed to check authorization, this probably means the user's cookie token is invalid or expired: [%i] %s", response.status_code, response.reason)
            return redirect(self.hub_base_url + '/hub?next=' + self.remap_url)

        # generic catch-all for upstream errors
        elif response.status_code >= 500:
            self.log.error("Upstream failure verifying auth token: [%i] %s", response.status_code, response.reason)
            abort(502, "Failed to check authorization (upstream problem)")

        # generic catch-all for internal server errors
        elif response.status_code >= 400:
            self.log.warn("Failed to check authorization: [%i] %s", response.status_code, response.reason)
            abort(500, "Failed to check authorization")

        else:
            # Auth invalid, reauthenticate.
            return redirect(self.hub_base_url + '/hub?next=' + self.remap_url)

        assert False, 'Something went wrong.'
