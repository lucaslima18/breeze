import requests
import base64


def get_auth_token(client_id, client_secret):
    """
        doing an lookup for a token
        this token is for future requests
    """
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    base64.b64decode(client_creds_b64)

    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "client_credentials",
    }
    token_headers = {
        'Authorization': f"Basic {client_creds_b64.decode()}"
    }

    response = requests.post(token_url, data=token_data, headers=token_headers)

    return response.json()
