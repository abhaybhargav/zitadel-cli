# ZITADEL CLI Tool

A command-line interface tool for automating ZITADEL operations like creating projects, applications, and service users.

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- A running ZITADEL instance
- ZITADEL admin token with appropriate permissions

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd zitadel-cli
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your ZITADEL configuration:
```bash
ZITADEL_BASE_URL=http://localhost:8080
ZITADEL_ADMIN_TOKEN=your-admin-token
```

> you will need to create a service user with high permissions to generate an admin token

## Usage

The CLI provides several commands for interacting with ZITADEL:

### Create a Project with Web Application

Creates a new project and sets up a web application with OIDC authentication:

```bash
python zitadel-cli.py setup-web-project \
  --project-name "My Project" \
  --app-name "My Web App"
```

This will:
1. Create a new project
2. Create a web application with OIDC configuration
3. Set up the following defaults:
   - Response Type: Code
   - Grant Type: Authorization Code
   - Authentication Method: None
   - Redirect URL: http://localhost:8000/users/auth
   - Post Logout URL: http://localhost:8000/dashboard
   - Dev Mode: Enabled
   - Access Token Type: Bearer
   - ID Token Role Assertion: Enabled
   - ID Token Userinfo Assertion: Enabled

### Create an API Application

Creates a new API application:

```bash
python zitadel-cli.py create-app \
  --name "My API"
```

### Create a Service User

Creates a service user with specified roles:

```bash
python zitadel-cli.py create-service-user \
  --username "my-service-user" \
  --roles "role1,role2,role3"
```

## Environment Variables

The CLI uses the following environment variables that should be defined in your `.env` file:

- `ZITADEL_BASE_URL`: The base URL of your ZITADEL instance (e.g., http://localhost:8080)
- `ZITADEL_ADMIN_TOKEN`: Your ZITADEL admin token with appropriate permissions

## Error Handling

The CLI will display appropriate error messages if:
- The ZITADEL instance is not accessible
- The admin token is invalid or expired
- Required permissions are missing
- API requests fail

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[Add your license information here]
