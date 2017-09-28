"""
SJCAM camera library
Send command to the camera, via WIFI, to configure it and to read parameters

Basic functions are:
- sync camera date/time with the computer
- load presets of settings to the camera
- download media files from camera
"""
import simpleyaml as yaml
import requests


class sjcamCommand(object):
    """command for sjcam4000"""
    def __init__(self, id, description="unknown", parameters=[],
            readOnly=False, format=""):

        super(sjcamCommand, self).__init__()
        self.id = int(id)
        self.description = description
        self.parameters = parameters
        self.readOnly = readOnly
        self.format = format

        fnParts = self.description.split(' ')
        fnParts[0] = fnParts[0].lower()
        fnParts[1:] = [f.capitalize() for f in fnParts[1:]]
        self.fn = ''.join(fnParts)

    def paramInt(self, paramStr):
        """
        Find the ID of a parameter, given the text description
        """
        for p in self.parameters:
            if paramStr.lower() == p.lower():
                return self.parameters.index(p)
        return None

    def paramString(self, paramInt):
        """
        Find the text description of a parameter, given the ID
        """
        if len(self.parameters) > paramInt:
            return self.parameters[paramInt]
        return None

    def __repr__(self):
        return r"<%s(id=%d, description='%s')>" % (self.__class__.__name__,
            self.id,
            self.description)

    def __str__(self):
        return "%d: %s" % (self.id,
            self.description)


class sjcam(object):
    """sjcam connection library"""

    address = "192.168.1.254"
    url = "http://%s/" % address
    cmdUrl = "%s?custom=1&cmd=%%d&par=%%d" % url
    rtsp = "rtsp://%s/sjcam.mov" % address

    def __init__(self):
        super(sjcam, self).__init__()
        self.commands = []
        print "parsing yaml"
        with open('sjcam.yaml', 'r') as yamlFile:
            commands = yaml.load(yamlFile)
            print commands
        for id, values in commands['commands'].items():
            self.commands.append(sjcamCommand(id=id,
                description=values.get('description'),
                parameters=values.get('parameter', []),
                readOnly=values.get('readOnly', False),
                format=values.get('format', '')))

    def getCommand(self, command, parameter=None):
        """
        Prepare a command to execute
        """
        cmd = [c for c in self.commands if c.description == command or c.fn == command]  # NOQA
        if cmd > 0:
            cmd = cmd[0]
            if parameter in cmd.parameters:
                paramId = cmd.parameters.index(parameter)
            else:
                paramId = None

    def httpCall(self, method="GET", cmdId=None, paramId=None):
        """
        Generic method to do an HTTP call
        @cmdId - numeric id of the command to issue
        @parameter - numeric id of the parameter
        """

        if cmdId is not None:
            data = {"custom": 1, "cmd": cmdId}  # , "par": parameter}
        if paramId is not None:
            data["par"] = paramId
        print method, self.url, data
        try:
            r = requests.request(method=method, url=self.url,
                data=data, timeout=5)
        except requests.exceptions.ConnectTimeout:
            return None
        return self.parseResponse(r)

    def httpPing(self):
        """
        Check if camera is available
        """
        r = self.httpCall(method='HEAD')
        print r
        if r is not None:
            return r.ok

    def parseResponse(self, response):
        """
        <?xml version="1.0" encoding="UTF-8" ?>
        <Function>
            <Cmd>2003</Cmd>
            <Status>0</Status>
        </Function>
        returns
        {'Cmd': 2003, 'Status': 0}
        """
        root = ET.fromstring(response)
        response = {}
        for child in root:
            response[child.tag] = child.text
        return response


if __name__ == "__main__":
    print "SJcam lib"
    cam = sjcam()
    # print "Ping"
    # if cam.httpPing():
    #     print "Camera available"
    # else:
    #     print "Check connection to camera"
