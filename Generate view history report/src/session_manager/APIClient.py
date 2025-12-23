# Import libraries
import requests
from requests.adapters import HTTPAdapter, Retry

# Define the APIClient class
class APIClient:
    """A simple HTTP client for interacting with a RESTful API."""
    # Initialise client
    def __init__(self, base_url: str, api_server_url: str, headers: dict, ssl_certificate_verification=True):
        
        # Fix the base URL (ensure trailing slash)
        if not base_url.endswith('/'): base_url = base_url + '/'
        # Fix the API Server URL (ensure no leading slash and presence of trailing slash)
        api_server_url = api_server_url[1:] if api_server_url.startswith('/') else api_server_url
        if api_server_url and not api_server_url.endswith('/'): api_server_url = api_server_url + '/'
        # Compose full base URL
        self.base_url = base_url
        self.api_server_url = api_server_url
        self.full_base_url = self.base_url + self.api_server_url

        # Initialise session
        self.session = requests.Session()

        # Common headers
        #self.session.headers.update({'Content-Type': 'application/json'})
        
        # Header updates from input
        self.session.headers.update(headers)

        # SSL certificate verification
        self.session.verify = ssl_certificate_verification
        
        # Retry strategy
        retry_strategy = Retry(
            total=10,                     # Total number of retries
            backoff_factor=1,             # Wait 1s, 2s, 4s, etc. between retries
            status_forcelist=[428, 429, 500, 502, 503, 504],  # Retry on these HTTP status codes
            #allowed_methods=["HEAD", "GET", "OPTIONS"]   # Retry only on these methods
        )    
        # Create an adapter with the retry strategy
        http_adapter = HTTPAdapter(max_retries=retry_strategy)
        # Mount the adapter
        self.session.mount("https://", http_adapter)
        self.session.mount("http://", http_adapter)

    # Get base URL
    def get_base_url(self):
        return self.base_url
    
    # Get API server URL
    def get_api_server_url(self):
        return self.api_server_url
    
    # Get full API server URL
    def get_full_api_url(self):
        return self.full_base_url
    
    # Get headers
    def get_headers(self):
        return self.session.headers

    # Perform a GET call
    def get(self, endpoint, additional_headers={}, params=None):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.get(url, params=params)
        # Return
        return response
        #return self._handle_response(response)

    # Perform a POST call
    def post(self, endpoint, additional_headers={}, data=None, json=None, files=None):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.post(url, data=data, json=json, files=files)
        # Return
        return response
        #return self._handle_response(response)

    # Perform a PATCH call
    def patch(self, endpoint, additional_headers={}, data=None, json=None, files=None):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.patch(url, data=data, json=json, files=files)
        # Return
        return response
        #return self._handle_response(response)
    
    # Perform a PUT call
    def put(self, endpoint, additional_headers={}, data=None, json=None, files=None):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.put(url, data=data, json=json, files=files)
        # Return
        return response
        #return self._handle_response(response)
    
    # Perform a HEAD call
    def head(self, endpoint, additional_headers={}, data=None, json=None, files=None):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.head(url, data=data, json=json, files=files)
        # Return
        return response
        #return self._handle_response(response)

    # Perform a DELETE call
    def delete(self, endpoint, additional_headers={}):
        # Fix endpoint (ensure no leading slash)
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        # Compose full URL
        url = f"{self.full_base_url}{endpoint}"
        # Further header updates from input
        if additional_headers:
            self.session.headers.update(additional_headers)
        # Get response
        response = self.session.delete(url)
        # Return
        return response
        #return self._handle_response(response)

    """
    # Handle the response
    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e} - {response.text}")
        except ValueError:
            print("Response content is not valid JSON")
        return None
    """

    # Close the session
    def close(self):
        self.session.close()



"""
### Example usage:
client = APIClient('https://api.example.com', auth_token='your_token_here')

# GET request
profile = client.get('/user/profile')

# POST request
update = client.post('/user/update', data={'name': 'Manuel'})

# Close session when done
client.close()
"""
