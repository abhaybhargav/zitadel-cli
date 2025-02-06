import click
import requests
import json
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

ZITADEL_BASE_URL = os.getenv("ZITADEL_BASE_URL")
ZITADEL_ADMIN_TOKEN = os.getenv("ZITADEL_ADMIN_TOKEN")


class ZitadelAPI:
    def __init__(self, base_url: str, admin_token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }

    def create_application(self, name: str, app_type: str = "APPLICATION_TYPE_API") -> dict:
        """Create a new application in Zitadel"""
        endpoint = f"{self.base_url}/management/v1/projects/me/apps"
        payload = {
            "name": name,
            "appType": app_type,
            "authMethodType": "AUTH_METHOD_TYPE_API",
            "accessTokenType": "ACCESS_TOKEN_TYPE_BEARER"
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_service_user(self, username: str, roles: list[str]) -> dict:
        """Create a service user with specified roles"""
        # First create the user
        endpoint = f"{self.base_url}/management/v1/users/machine"
        payload = {
            "userName": username,
            "name": username,
            "description": f"Service user for {username}"
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        user_data = response.json()
        
        # Assign roles to the user
        user_id = user_data['userId']
        for role in roles:
            self._assign_role(user_id, role)
            
        return user_data

    def get_service_user_token(self, user_id: str) -> str:
        """Generate a token for the service user"""
        endpoint = f"{self.base_url}/management/v1/users/{user_id}/token"
        response = requests.post(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()['token']

    def _assign_role(self, user_id: str, role: str) -> None:
        """Assign a role to a user"""
        endpoint = f"{self.base_url}/management/v1/users/{user_id}/roles"
        payload = {
            "roleKey": role,
            "orgId": "me"  # Use current organization
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()

    def create_project(self, name: str) -> dict:
        """Create a new project in Zitadel"""
        endpoint = f"{self.base_url}/management/v1/projects"
        payload = {
            "name": name,
            "projectRoleAssertion": True,
            "projectRoleCheck": True
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_web_application(self, project_id: str, name: str) -> dict:
        """Create a new web application with PKCE in the specified project"""
        endpoint = f"{self.base_url}/management/v1/projects/{project_id}/apps/oidc"
        payload = {
            "name": name,
            "responseTypes": ["OIDC_RESPONSE_TYPE_CODE"],
            "grantTypes": ["OIDC_GRANT_TYPE_AUTHORIZATION_CODE"],
            "appType": "OIDC_APP_TYPE_WEB",
            "authMethodType": "OIDC_AUTH_METHOD_TYPE_NONE",
            "redirectUris": ["http://localhost:8000/users/auth"],
            "postLogoutRedirectUris": ["http://localhost:8000/dashboard"],
            "version": "OIDC_VERSION_1_0",
            "devMode": True,
            "accessTokenType": "OIDC_TOKEN_TYPE_BEARER",
            "idTokenRoleAssertion": True,
            "idTokenUserinfoAssertion": True
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

@click.group()
def cli():
    """CLI tool for Zitadel automation"""
    pass

@cli.command()
@click.option('--name', required=True, help='Application name')
def create_app(name: str):
    """Create a new application in Zitadel"""
    api = ZitadelAPI(ZITADEL_BASE_URL, ZITADEL_ADMIN_TOKEN)
    try:
        result = api.create_application(name)
        click.echo(f"Application created successfully!")
        click.echo(f"Client ID: {result['clientId']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error creating application: {str(e)}", err=True)

@cli.command()
@click.option('--username', required=True, help='Service user username')
@click.option('--roles', required=True, help='Comma-separated list of roles')
def create_service_user(username: str, roles: str):
    """Create a service user with specified roles"""
    api = ZitadelAPI(url, token)
    role_list = [r.strip() for r in roles.split(',')]
    
    try:
        user = api.create_service_user(username, role_list)
        token = api.get_service_user_token(user['userId'])
        
        click.echo(f"Service user created successfully!")
        click.echo(f"User ID: {user['userId']}")
        click.echo(f"Token: {token}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error creating service user: {str(e)}", err=True)

@cli.command()
@click.option('--project-name', required=True, help='Project name')
@click.option('--app-name', required=True, help='Application name')
def setup_web_project(project_name: str, app_name: str):
    """Create a new project and web application with PKCE authentication"""
    api = ZitadelAPI(ZITADEL_BASE_URL, ZITADEL_ADMIN_TOKEN)
    try:
        # Create project
        project = api.create_project(project_name)
        click.echo(f"Project created successfully!")
        click.echo(f"Project ID: {project['id']}")
        
        # Create web application
        app = api.create_web_application(project['id'], app_name)
        click.echo(f"Web application created successfully!")
        click.echo(f"Client ID: {app['clientId']}")
        
    except requests.exceptions.RequestException as e:
        click.echo(f"Error setting up project: {str(e)}", err=True)

if __name__ == '__main__':
    cli()