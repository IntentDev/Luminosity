'''A wrapper for td.run() object, to easily delay both the
calling of functions and setting of members
'''

import inspect
import re

class Delay():
	'''
	A wrapper for td.run() object, to easily delay both the
	calling of functions and setting of members

	Hint:
		fromOP should almost always be set.  

	Call promoted function:

		Delay(delayFrames = 1, fromOP = me).Call(op('myComp'), 'myFuncInExtension', 'arg1ForMyFunc', 'arg2')

	Call and set multiple times with 1 Delay object:

		delay = Delay(delayFrames = 60, fromOP = me)

		delay.Set(op('level1').par, 'opacity', 0.0)
		delay.Call(myObject, 'myFunc', arg1, arg2, keyWordArg1 = 2))
		delay.CallExt(op('myComp', 'myExtensionName', 'myFunc', arg1, arg2, keyWordArg1 = 2))

	'''
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		self.set = "setattr(args[0], args[1], *args[2])" 
		self.call = "getattr(args[0], args[1])(*args[2], **args[3])"
		self.callExt = "getattr(getattr(args[0].ext, args[1]), args[2])(*args[3], **args[4])"

	def Call(self, Object, method, *args, **kwargs):
		
		try:
			#print(Object, method, args, kwargs)
			run(self.call, Object, method, args, kwargs, *self.args, **self.kwargs)
		except:
			#print(Object, method, args, kwargs)
			owner = inspect.currentframe().f_back.f_code.co_name
			print ('Error in: Delay.Call() - called by:', owner, 
				'\n\n\t', 'Delay Args:\n\t\t', self.args, self.kwargs, '\n\n\t', 
				owner, 'Args:\n\t\t', Object, method, *args, **kwargs)		
	
	def Set(self, Object, member, *args, **kwargs):
		try:
			run(self.set, Object, member, args, kwargs, *self.args, **self.kwargs)
		except:
			owner = inspect.currentframe().f_back.f_code.co_name
			print ('Error in: Delay.Set() - called by:', owner, 
				'\n\n\t', 'Delay Args:\n\t\t', self.args, self.kwargs, '\n\n\t', 
				owner, 'Args:\n\t\t', Object, member, *args, **kwargs)

	def CallExt(self, extComp, extName, method, *args, **kwargs):
		# Only needed when an extension isn't promoted or is initializing and doesn't exist yet 
		# but you want to call a method in it. Otherwise Call() will work without the extra 
		# argument. Also the extension object can be directly passed in Call(), in CallExt you 
		# need to specify the ext COMP and the ext name (str) separately
		try:
			run(self.callExt, extComp, extName, method, args, kwargs, *self.args, **self.kwargs)
		except:
			owner = inspect.currentframe().f_back.f_code.co_name
			print ('Error in: Delay.CallExt() - called by:', owner, 
				'\n\n\t', 'Delay Args:\n\t\t', self.args, self.kwargs, '\n\n\t', 
				owner, 'Args:\n\t\t', extComp, extName, method, *args, **kwargs)

class Timecode():

	def TimecodeToSeconds(self, timecode):

		timecode = timecode.split(':')
		hours = int(timecode[0])
		mins = int(timecode[1])
		secs = int(timecode[2][:2])
		frames = int(timecode[2][-2:])
		seconds = hours * 60 * 60 + mins * 60 + secs + frames / me.time.rate

		return seconds

	def SecondsToTimecode(self, Seconds):

		frac, seconds = math.modf(Seconds)
		frames = round(me.time.rate * frac)
		minutes = math.floor(seconds / 60)
		hours = math.floor(minutes / 60)
		minutes = minutes % 60
		seconds = int(seconds) % 60

		l = [hours, minutes, seconds, frames]

		hours = str(hours).zfill(2)
		minutes = str(minutes).zfill(2)
		seconds = str(seconds).zfill(2)
		frames = str(frames).zfill(2)

		s = hours + ':' + minutes + ':' + seconds + '.' + frames

		return s

	def TimecodeToFrames(self, timecode):

		timecode = re.split(r'[:.]', timecode)
		hours = int(timecode[0])
		mins = int(timecode[1])
		#secs = int(timecode[2][:2])
		#frames = int(timecode[2][-2:])
		secs = int(timecode[2])
		frames = int(timecode[3])
		seconds = hours * 60 * 60 + mins * 60 + secs + frames / me.time.rate

		frame = int(seconds * me.time.rate)
	
		return frame


	def ExtTimecodeToFrames(self, timecode, rate):

		timecode = re.split(r'[:.]', timecode)
		hours = int(timecode[0])
		mins = int(timecode[1])
		secs = int(timecode[2])
		frames = int(timecode[3])

		print(hours, mins, secs, frames)
		seconds = hours * 60 * 60 + mins * 60 + secs + frames / rate

		frame = int(seconds * rate)
	
		return frame

	def FramesToTimecode(self, frame):

		frameRate = me.time.rate
		ff = int(frame % frameRate)
		s = int(frame // frameRate)
		l = (s // 3600, s // 60 % 60, s % 60, ff)

		hours = str(l[0]).zfill(2)
		minutes = str(l[1]).zfill(2)
		seconds = str(l[2]).zfill(2)
		frames = str(l[3]).zfill(2)

		s = hours + ':' + minutes + ':' + seconds + '.' + frames

		return s

	def ExtFramesToTimecode(self, frame, rate):

		frameRate = me.time.rate
		ff = int(frame % rate)
		s = int(frame // rate)
		l = (s // 3600, s // 60 % 60, s % 60, ff)

		hours = str(l[0]).zfill(2)
		minutes = str(l[1]).zfill(2)
		seconds = str(l[2]).zfill(2)
		frames = str(l[3]).zfill(2)

		s = hours + ':' + minutes + ':' + seconds + '.' + frames

		return s

	def CheckAllChar(self, string, search = re.compile(r'[^\d:.]').search):
		return not bool(search(string.replace(' ', '')))

	def StringToTimecode(self, string, prevString):

		timecode = prevString		
		setTimecode = self.CheckAllChar(string)
	
		if setTimecode:
			
			frameRate = me.time.rate
			tc = re.split(r'[:.]', string)

			i = 0
			frames = 0
			for val in reversed(tc):

				if val == '': val = 0
				val = int(val)

				if i == 0: frames += val
				elif i == 1: frames += val * frameRate
				elif i == 2: frames += val * 60 * frameRate
				elif i == 3: frames += val * 3600 * frameRate 

				i += 1

			timecode = self.FramesToTimecode(frames)

		#print (timecode)
		return timecode

class SaveFuncs():

	def OnSave():

		pass

	def TrigNoClip(self):

		op.CLIP_CHAN_VID.op('stopList').clear()

		for i in range(op.CLIP_CHAN_VID.op('channels').numRows - 1):	
			strVal = str(i)
			dataClipPath = me.fetch('CLIP_DATA') +'/'+ me.fetch('CUR_BANK') +'/clipLane' + strVal +'/clip1001'
			
			chan = op.CLIP_CHAN_VID.op('channel' + strVal)
			chan.Trigger(dataClipPath)

			noClipPath = op.SYNTHS.op('noClip').path
			run("args[0].Trigger(args[1])", chan, noClipPath, delayFrames = 30, fromOP = chan)
					
		for index in range(op.DATABASE.fetch('NUM_CLIP_LANES')):
			#op(me.fetch('MASTER') + '/ui/clipLanes/laneStop/stop' + str(index)).click([.5, .5])

			strIndex = str(index)
		
			stop = op(me.fetch('MASTER') + '/ui/clipLanes/laneStop/stop' + str(index))
			dataClipPath = me.fetch('CLIP_DATA') +'/'+ me.fetch('CUR_BANK') +'/clipLane' + strIndex +'/clip1001'
			channel = op(me.fetch('UI') + '/clipLanes/clipLane' + strIndex)	
			stop.Stop(dataClipPath, channel, index)
		

		op.UI.op('clipControls/previewClip/viewTOP').par.top = ''



