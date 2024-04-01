from src.Command import Command


class AudioVideo(Command):
    """
    Interfaces with Axis IO periphery devices.
    """

    def __init__(self, base_url: str):
        """
        Constructor for the AudioVideo class

        Parameters
        ----------
        base_url : str
            Base URL of Axis IP camera
        """
        self.base_url = base_url
        self.results = {
            'Image Capture': self._check_image_capture(),
            'Change PTZ': self._check_change_video_ptz(),
            'Audio Stream': self._check_audio_stream(),
            'Play audio clip': self._play_audio_clip()
        }
        super().__init__(self.base_url, self.results)

    def _check_image_capture(self):
        """
        Checks for the ability to an image from the
        live feed of an Axis camera.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        endpoint = '/axis-cgi/jpg/image.cgi'
        params = {'resolution': '640x480', 'camera': '1'}

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to capture screenshot from camera. Access Denied.'
        elif resp.status_code == 200:
            msg = 'Image Capture successful'
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _check_change_video_ptz(self):
        """
        Checks for the ability to change the PTZ
        of an Axis camera.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        endpoint = '/axis-cgi/com/ptz.cgi'
        params = {'move': 'home'}

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to change PTZ. Access Denied.'
        elif resp.status_code == 200:
            msg = 'PTZ modification successful.'
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _check_audio_stream(self):
        """
        Checks for the ability to download a
        real-time audio stream from an Axis camera.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        endpoint = '/axis-cgi/audio/receive.cgi'

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint)

        if resp.status_code == 401:
            msg = 'Unable to download audio. Access Denied.'
        elif resp.status_code == 200:
            msg = 'Audio stream download successful.'
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg

    def _play_audio_clip(self):
        """
        Checks for the ability to execute an audio clip
        on an Axis camera.

        Returns
        -------
        msg : str
            Formatted Axis CGI response body.
        """
        endpoint = '/axis-cgi/playclip.cgi'
        params = {'clip': '7'}

        # Make API call.
        resp = self.make_network_call(endpoint=endpoint, params=params)

        if resp.status_code == 401:
            msg = 'Unable to play audio clip. Access Denied.'
        elif resp.status_code == 200:
            msg = f'Execution of audio clip successful. `{resp.text}`'
        else:
            msg = f'Axis API error encountered with status code {resp.status_code}'

        return msg
