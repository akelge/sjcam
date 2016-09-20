# import httplib

"""
"""


class sjcamCommand(object):
    """command for sjcam4000"""
    def __init__(self, id, description="unknown", parameters=[],
            readOnly=False, writeOnly=False, format=""):

        super(sjcamCommand, self).__init__()
        self.id = id
        self.description = description
        self.parameters = parameters
        self.readOnly = readOnly
        self.writeOnly = writeOnly
        self.format = format

    @property
    def fn(self):
        fnParts = self.description.split(' ')
        fnParts[0] = fnParts[0].lower()
        fnParts[1:] = [f.capitalize() for f in fnParts[1:]]
        return ''.join(fnParts)

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
    url = "http://%s" % address
    cmdUrl = "%s/?custom=1&cmd=%%d&par=%%d" % url
    rtsp = "rtsp://%s/sjcam.mov" % address

    def __init__(self):
        super(sjcam, self).__init__()


if __name__ == "__main__":
    print "SJcam lib"
    cam = sjcam()
