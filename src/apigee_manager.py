import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Configuration
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
APIGEE_ORG = "db-project-450115"
BASE_URL = f"https://apigee.googleapis.com/v1/organizations/{APIGEE_ORG}"

def get_token():
    """Get access token from service account."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def make_request(method, url, json=None):
    """Make API request with authorization."""
    token = get_token()
    if not token:
        print("Failed to get access token")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        else:  
            response = requests.post(url, headers=headers, json=json)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API request failed: {e}")
        return None

def list_all_apps():
    """List all applications."""
    response = make_request("GET", f"{BASE_URL}/apps")
    if response and 'app' in response:
        print("\nAll Applications:")
        for app in response['app']:
            app_id = app.get('appId')
            if app_id:
                app_details = make_request("GET", f"{BASE_URL}/apps/{app_id}")
                if app_details:
                    print(app_details.get('name', 'No name available'))

def list_developer_apps(developer_email):
    """List applications for a specific developer."""
    response = make_request("GET", f"{BASE_URL}/developers/{developer_email}/apps")
    if response and 'app' in response:
        print(f"\nApplications for {developer_email}:")
        for app in response['app']:
            print(app.get('appId', 'No appId available'))
    else:
        print(f"No applications found for {developer_email}")

def create_app(app_name, developer_email):
    """Create a new application."""
    payload = {
        "name": app_name,
        "attributes": [{"name": "displayName", "value": app_name}],
        "apiProducts": ["MyAppAPIProduct"]
    }
    
    response = make_request(
        "POST", 
        f"{BASE_URL}/developers/{developer_email}/apps", 
        json=payload
    )
    
    if response:
        print(f"\nSuccessfully created application: {app_name}")
    else:
        print("Failed to create application")

def main():
    print("Apigee API Manager\n")

    if os.getenv('CI') == 'true':  # Check if running in CI/CD
        choice = '1'  # Automatically choose the option to list all apps
        print("Running in CI/CD environment, automatically selecting option 1.")
        list_all_apps()  # Run the list all apps function directly
        return  # Exit after listing all apps
    else:
        print("\nOptions:")
        print("1. List All Applications")
        print("2. List Applications by Developer")
        print("3. Create a New Application")
        print("4. Exit")
        choice = input("\nEnter your choice: ")

    while True:
        if choice == '1':
            list_all_apps()
        elif choice == '2':
            email = input("Enter developer email: ")
            list_developer_apps(email)
        elif choice == '3':
            name = input("Enter application name: ")
            email = input("Enter developer email: ")
            create_app(name, email)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        if os.getenv('CI') != 'true':  # Only ask for input if not in CI environment
            print("\nOptions:")
            print("1. List All Applications")
            print("2. List Applications by Developer")
            print("3. Create a New Application")
            print("4. Exit")
            choice = input("\nEnter your choice: ")

if __name__ == "__main__":
    main()

