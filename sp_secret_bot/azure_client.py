import logging
from typing import Any, Dict, List, Optional

import requests
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class AzureClient:
    """
    Handles authentication and interaction with the Microsoft Graph API.
    Includes automatic retries and robust error handling.
    """

    GRAPH_API_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self) -> None:
        self.logger = logging.getLogger("SPSecretBot.AzureClient")
        self.credential: Optional[DefaultAzureCredential] = None
        self.token: Optional[Any] = None
        self.session = self._create_retry_session()

    def _create_retry_session(
        self, retries: int = 3, backoff_factor: float = 0.3
    ) -> requests.Session:
        """Creates a requests session with retry logic."""
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def authenticate(self) -> bool:
        """
        Authenticates using DefaultAzureCredential.
        Returns True if successful, False otherwise.
        """
        try:
            self.logger.info("Attempting authentication with DefaultAzureCredential...")
            self.credential = DefaultAzureCredential()
            # Request a token to verify credentials immediately
            self.token = self.credential.get_token("https://graph.microsoft.com/.default")
            self.logger.info("Authentication successful.")
            return True
        except ClientAuthenticationError as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during authentication: {e}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """Returns the authorization headers for Graph API requests."""
        if not self.credential:
            raise RuntimeError("Client not authenticated.")

        # Refresh token if needed (though get_token usually handles caching)
        # We re-fetch to ensure validity
        self.token = self.credential.get_token("https://graph.microsoft.com/.default")
        return {"Authorization": f"Bearer {self.token.token}", "Content-Type": "application/json"}

    def get_all_service_principals(self) -> List[Dict[str, Any]]:
        """
        Retrieves all service principals from the tenant.
        Handles pagination automatically.
        """
        self.logger.info("Fetching Service Principals from Microsoft Graph...")
        service_principals = []
        url = f"{self.GRAPH_API_URL}/servicePrincipals"

        # Select only necessary fields to optimize performance
        params = {"$select": "id,appId,displayName,passwordCredentials,keyCredentials"}

        while url:
            try:
                headers = self.get_headers()
                # Only send params on the first request; nextLink already contains them
                request_params = (
                    params if url == f"{self.GRAPH_API_URL}/servicePrincipals" else None
                )

                response = self.session.get(url, headers=headers, params=request_params, timeout=30)
                response.raise_for_status()
                data = response.json()

                batch = data.get("value", [])
                service_principals.extend(batch)
                self.logger.debug(f"Fetched batch of {len(batch)} service principals.")

                url = data.get("@odata.nextLink")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching service principals: {e}")
                break

        self.logger.info(f"Total Service Principals fetched: {len(service_principals)}")
        return service_principals
