import httplib

"""
cmds = {
"1001" : {"descr": "", "params": {}},
1002 Image Size
1003 Photos space left
1004 Capture Mode
1005 Quality
1006 Sharpness
1007 White balance par=0 -auto,1-Daylight,2-Cloudy,3-Thungsten,4-Fluorescent
1008 Color
1009 ISO
1012
1012 Time laps between fotos par=0-3s,1-5s,2-10s,3-20s
2001 Recording(in mode video,time video) 1-start/0-stop
2002 Video resolution par=0-FHD,1-720p60f,2-720p30f,3-WVGA,4-VGA
2003 Cyclic record par=0-off,1-3min,2-5Min,3-10Min,4..?
2004 WDR (HDR) par=0 off,1 on
2005 Exposure par=3- +1.0,4- +2/3,12- -2,7 -1/3
2006 ?? Motion detection (not in App, not working)
2007 Audio recording par=0 off,1 on
2008 Date stamp par=0 off,1 on
2009 Remaining seconds for video
2010 Live View Size
2013
2014
2015
2016
2019
3001 Set mode par=1 (0-foto,1-video,3-time video, 4-time foto)
3002 get list of all commands XML file
3003 Set wifi name str=YeckelCam
3004 Set wifi password str=123456
3005 Set Date str=2015-01-29 0
3006 Set Time str=11:13:31 0
3007 Turn camera off par=0-never,1-3min,2-5-min,3-10min,4-now
3008 ?? DV Language
3010 Format SD card par=1
3011 Reset to default
3012 FW Version G20141204V01
3013
3014 Dump settings XML File
3015 Media files list XML File
3016 Camera mode 0-video, 1-foto, 3-time videos, 4-time fotos
3017 Free bytes left on card 32093601792
3018
3019 Battery status Values between (min)0..5(max), 5 when on charger
3021
3022
3023
3024
3025 Powerline frequency par=0- 50Hz, 1- 60Hz
3026 Rotate par=0- Normal,1 -upside down
3027 Random number?? 59620468 Value is changing fast without any reason.
3028
3029 Some non working link http://115.29.201.46:8020/download/filedesc.xml
3030 FW Filename(not downloadable) http://192.168.1.254/FW96655A.bin
4001
4002
4003
4004
8001
8002	
}

cmd = {1002 : {"description": "Image Size", "params": {}}}
"""

class sjcamCommandParameter(object):
	"""docstring for sjcamCommandParameter"""
	def __init__(self, id, description, isString=False):
		super(sjcamCommandParameter, self).__init__()
		self.id = id
		self.description = description
		self.isString = isString

	def __repr__(self):
		return r"<%s(id=%d, description=%s, isString=%s)>" % (self.__class__.__name__,
			self.id,
			self.description,
			self.isString)

	def __str__(self):
		return "%d: %s" % (self.id,
			self.description)
			
class sjcamCommand(object):
	"""command for sjcam4000"""
	def __init__(self, id, description="unknown"):
		super(sjcamCommand, self).__init__()
		self.id = id
		self.description = description
		self.parameters = []

	def __repr__(self):
		return r"<%s(id=%d, description=%s)>" % (self.__class__.__name__,
			self.id,
			self.description)

	def __str__(self):
		return "%d: %s" % (self.id,
			self.description)

	def addParameter(self, paramId, paramDescr):
		param = sjcamCommandParameter(paramId, paramDescr)
		self.parameters.append(param)

	def getParameter(self, parameterId):
		param = [p for p in self.parameters if p.id == parameterId]
		if len(param) > 0:
			return param[0]

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
	wb = sjcamCommand(1007, "White balance")
	wb.addParameter(0, "auto")
	wb.addParameter(1, "daylight")
