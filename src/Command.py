from requests import get, Response  # (python / python3) -m pip install requests


class Command:
    """
    Parent class for all API calls made to
    the Axis CGI API.
    """

    def __init__(self,
                 url: str,
                 results: dict[str, str] | None = None
                 ):
        self.base_url = url
        self.results = results

    def make_network_call(self,
                          endpoint: str,
                          params: dict[str, str] | None = None):
        """
        Executes CGI API call against Axis IP camera.

        Parameters
        ----------
        endpoint : str
            Axis CGI API endpoint.
        params : dict[str, str]
            HTTP parameters to be passed to an API.

        Returns
        -------
        resp : Response
            HTTP Response object.
        """
        if not isinstance(endpoint, str) or len(endpoint) == 0:
            raise ValueError("Endpoint must be a non-empty string.")

        try:
            resp = get(url=self.base_url + endpoint, params=params, stream=True)
        except Exception as e:
            raise RuntimeError(f"Error executing Axis API call: {str(e)}.")

        return resp

    def print_results(self):
        """
        Outputs results from Axis API calls to stdout.
        """
        return '\n'.join([f'[*] {key}: {val}' for (key, val) in self.results.items()])
