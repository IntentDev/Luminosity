import colorsys as color

class AnimateExt(object):
	
	def __init__(self, ownerComp):
		#The component to which this extension is attached
		self.ownerComp = ownerComp
		self.uiAttr = self.ownerComp.fetch('CompAttr')['uiAttr']

		self.anim0 = self.ownerComp.op('animation0')
		self.chansOP0 = self.anim0.op('channels')
		self.keysOP0 = self.anim0.op('keys')
		self.keyframe0 = self.anim0.op('keyframe')

		self.anim1 = self.ownerComp.op('animation1')
		self.chansOP1 = self.anim1.op('channels')
		self.keysOP1 = self.anim1.op('keys')
		self.keyframe1 = self.anim1.op('keyframe')

		self.animList = [self.anim0, self.anim1]
		self.chansOPList = [self.chansOP0, self.chansOP1]
		self.keysOPList = [self.keysOP0, self.keysOP1]
		self.keyframeList = [self.keyframe0, self.keyframe1]

		self.SwitchCross = self.ownerComp.op('switchCross')
		self.TimeMode = op.DATABASE.fetch('TIME_UNITS').val
		self.SetProperties = self.ownerComp.op('setProperties')

		#self.TicksPerBeat = op.LM.fetch('TICKS_PER_BEAT').val
		#self.BeatSpeedRatio = self.TicksPerBeat / 120

		self.CurSpeed = 1.0
	
		self.GetCurAnim()
		self.GetParList()

	def GetCurAnim(self):
		self.CurAnim = self.animList[self.Cross]
		self.CurChansOP = self.chansOPList[self.Cross]
		self.CurKeysOP = self.keysOPList[self.Cross]
		self.CurKeyFrame = self.keyframeList[self.Cross]

	def Cue(self, *args):
		self.CurAnim.par.cuepulse.pulse()
		self.ownerComp.par.Cross = 0

	def GetParList(self):

		self.parsOP = self.ownerComp.parent.plugin.op('parameters')
		self.parNames = [r[0].val for r in self.parsOP.rows()[1:]]
		self.listLength = len(self.parNames)

	def Clearallchannels(self, *args):
		self.ClearAllChannels()

	def ClearAllChannels(self):

		c = ui.messageBox('Clear All Channels', 'Are you sure?', buttons = ['Cancel', 'Clear All Channels'])
		if c == 1:
			self.ClearAll()
			
	def ClearAll(self):
		self.CurChansOP.clear(keepFirstRow = True)
		self.CurKeysOP.clear(keepFirstRow = True)		

	def Createparameterchannels(self, *args):
		self.CreateParameterChannels()

	def CreateParameterChannels(self):
		
		c = ui.messageBox('Create All Channels', 'Are you sure? This will clear existing keyframes.', buttons = ['Cancel', 'Create All Channels'])

		if c == 1:

			self.GetParList()

			self.CurChansOP.clear(keepFirstRow = True)
			self.CurKeysOP.clear(keepFirstRow = True)
			self.uiAttr = self.ownerComp.fetch('CompAttr')['uiAttr']

			for parName in self.parNames:

				if self.uiAttr[parName]['format'] != 'string':
					self.CreateChannel(parName, self.uiAttr[parName]['default'], 
										self.parNames.index(parName) + 1)

	def CreateParameterChannel(self, name):

		curChans = [r[0].val for r in self.CurChansOP.rows()[1:]]
		
		if name not in curChans:

			self.GetParList()

			index = self.parNames.index(name)
			self.uiAttr = self.ownerComp.fetch('CompAttr')['uiAttr']

			if self.uiAttr[name]['format'] != 'string':
				self.CreateChannel(name, self.uiAttr[name]['default'], index + 1)

				#print(name)

	def CreateChannel(self, name, default, index):

		#print(name, default, index)

		hueStep = 1.0 / self.listLength
		hue = (index - 1) * hueStep
		rgb = color.hsv_to_rgb(hue, .6, .8)
		
		self.CurChansOP.appendRow([name, index, 'hold', 'hold', default, 'keys', rgb[0], rgb[1], rgb[2], 1, 1, 0])
		self.CurKeysOP.appendRow([index, 1, default, 0, 0, self.ownerComp.par.Defaultexpr.eval(), 0, 0])
		self.CurKeysOP.appendRow([index, int(self.CurAnim.par.end), default, 0, 0, self.ownerComp.par.Defaultexpr.eval(), 0, 0])

	def PresetGetAnim(self): 

		pars = {}
		pars['end'] = self.CurAnim.par.end.eval() 
		pars['speed'] = self.ownerComp.par.Speed.eval()
		pars['tright'] = self.CurAnim.par.tright.eval()

		return [self.CurChansOP.text, self.CurKeysOP.text, pars]

	def PresetSetAnim(self, animPreset, playAnim = True, enableBlend = 0.0):
		
		self.InvCross = self.Cross
		self.Cross = int(-1 * self.ownerComp.par.Cross + 1)

		self.CurAnim.op('channels').text = animPreset[0]
		self.CurAnim.op('keys').text = animPreset[1]

		self.CurAnim.par.end = animPreset[2]['end']
		self.CurAnim.par.tright = animPreset[2]['tright'] 

		self.SetProperties.par.active = False

		self.CurSpeed = animPreset[2]['speed']
		self.SetSpeed()
		self.Speed = self.CurSpeed
			
		self.SwitchCross.par.index = enableBlend
		self.CuePlayAnim(playAnim = playAnim)

		if enableBlend == 0.0:
			run("args[0].PresetBlendEnd()", self.ownerComp, delayFrames = 1, fromOP = self.ownerComp)
	
	def CuePlayAnim(self, playAnim = True):
		#print(playAnim, self.ownerComp)
		self.CurAnim.par.cuepoint = 1
		self.CurAnim.par.cuepulse.pulse()
		self.CurAnim.par.play = playAnim
			
	def PresetBlendEnd(self):

		self.keyframeList[self.InvCross].lock = True
		self.SetProperties.par.active = True
		self.SwitchCross.par.index = 0

	def GetSpeed(self, val):
		units = op.DATABASE.fetch('TIME_UNITS').val
		return [op.LM.fetch('ANIM_BPM_SCALE').val, op.LM.fetch('ANIM_SECONDS_SCALE').val][units] * val

	def SetSpeed(self):

		self.CurAnim.par.speed = self.GetSpeed(self.CurSpeed)


	#################
	# properties

	@property
	def Cross(self):
		return self.ownerComp.par.Cross.eval()

	@Cross.setter
	def Cross(self, value):
		self.ownerComp.par.Cross = value	
		self.GetCurAnim()	
		self.CurKeyFrame.lock = False

	@property
	def Speed(self):
		return self.ownerComp.par.Speed.eval()

	@Speed.setter
	def Speed(self, value):
		self.ownerComp.par.Speed = value
		self.CurAnim.par.speed = self.GetSpeed(value)

	def Editanimation(self, *args):
		
		op.ANIM_EDITOR.OpenAnimEditor(self.ownerComp, floating = True)

	@property
	def Editanimation(self):
		return None

	@Editanimation.setter
	def Editanimation(self, value):
		op.ANIM_EDITOR.OpenAnimEditor(self.ownerComp, floating = True)


		
 