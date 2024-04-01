from src.Command import Command


def _configure_ports_msg(msg: str, action: str):
    """
    Adds string formatting to raw text received from
    Axis CGI API endpoints.

    Parameters
    ----------
    msg : str
        Raw text message received from the CGI API response.
    action : str
        Axis I/O characteristic being examined.

    Returns
    -------
    msg : str
        Formatted Axis CGI response body.
    """
    status = {'0': 'Closed Circuit', '1': 'Open Circuit'}

    if action == 'status':
        msg = msg.replace('=0', f'={status["0"]}')
        msg = msg.replace('=1', f'={status["1"]}')

    msg = msg.replace('port', '\tport')
    return ''.join(['\n', msg])


class IO(Command):
    """
    Interfaces with Axis IO periphery devices.
    """

    def __init__(self, base_url: str):
        """
        Constructor for the IO class

        Parameters
        ----------
        base_url : str
            Base URL of Axis IP camera
        """
        self.num_ports = 1
        self.base_url = base_url
        self.results = {
            'Flood Light': self._check_flood_light(),
            'Port Status': self._check_io_port_status(),
            'Active Ports': self._check_io_port_active(),
            'Port Direction': self._check_io_port_direction(),
        }
        super().__init__(self.base_url, self.results)

    def _check_io_port_direction(self):
        """
        Checks whether a given I/O port is
        being used as an input or output.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        params = {'checkdirection': ','.join([str(i) for i in range(1, self.num_ports + 1)])}
        endpoint = '/axis-cgi/io/port.cgi'

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to check direction of ports. Access Denied.'
        elif resp.status_code == 200:
            msg = _configure_ports_msg(msg=resp.text, action='direction')
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _check_io_port_active(self):
        """
        Checks the activity level of an arbitrary
        number of Axis I/O ports.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        params = {'checkactive': ','.join([str(i) for i in range(1, self.num_ports + 1)])}
        endpoint = '/axis-cgi/io/port.cgi'

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to check activity of ports. Access Denied.'
        elif resp.status_code == 200:
            msg = _configure_ports_msg(msg=resp.text, action='active')
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _check_io_port_status(self):
        """
        Checks the status of Axis I/O ports.

        Notes
        -----
        Status of 0: Open circuit.
        Status of 1: Closed circuit.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        params = {'check': '1,2,3,4,5'}
        endpoint = '/axis-cgi/io/port.cgi'

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to check status of ports. Access Denied.'
        elif resp.status_code == 200:
            msg = _configure_ports_msg(msg=resp.text, action='status')
            self.num_ports = len(msg.split(' '))
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _check_flood_light(self):
        """
        Checks if unauthenticated CGI api calls can be
        executed to enable / disable the Axis floodlight.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.

        Notes
        -----
        Floodlight uses pulse width modulation. Brightness of the floodlight can be controlled
        by passing values ranging from [-100, 100] with 100 being the largest (brightest) value.

        Positive values passed to the CGI endpoint result in the brightness of the light being immediately changed.
        Negative values passed to the CGI endpoint result in the brightness of the light being gradually changed.

        Examples
        --------
        /axis-cgi/io/lightcontrol.cgi?action=L1:0: Light is immediately turned off.
        /axis-cgi/io/lightcontrol.cgi?action=L1:-0: Light is gradually turned off.
        /axis-cgi/io/lightcontrol.cgi?action=L1:50: Light is immediately configured to half brightness.
        /axis-cgi/io/lightcontrol.cgi?action=L1:-50: Light is gradually configured to half brightness.
        /axis-cgi/io/lightcontrol.cgi?action=L1:100: Light is immediately configured to full brightness.
        /axis-cgi/io/lightcontrol.cgi?action=L1:-100: Light is gradually configured to full brightness.
        """
        endpoint = '/axis-cgi/io/lightcontrol.cgi'
        params = {'action': 'L1:0'}

        # Attempt to configure floodlight.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to activate flood light. Access Denied.\n'
        elif resp.status_code == 200:
            msg = 'Flood light is configurable. Anonymous viewer login enabled.\n'
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}\n'

        return msg
