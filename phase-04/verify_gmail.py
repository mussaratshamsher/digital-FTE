import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']

def test_gmail_refresh():
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expired, attempting refresh...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"❌ Refresh failed: {e}")
                creds = None
        
        if not creds:
            print("🔑 No valid refresh token found. Starting new login flow...")
            if not os.path.exists(creds_path):
                print(f"❌ Error: {creds_path} not found!")
                return

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            print("✅ New token.json generated with offline access!")

    print("\n--- Diagnostic Results ---")
    token_data = json.load(open(token_path))
    if "refresh_token" in token_data:
        print("✅ REFRESH TOKEN DETECTED: Your token should last for months.")
    else:
        print("⚠️ NO REFRESH TOKEN: This token will expire in 7 days.")
    
    print(f"📅 Expiry: {token_data.get('expiry')}")

if __name__ == "__main__":
    test_gmail_refresh()
