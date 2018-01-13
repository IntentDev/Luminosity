import copy

class PFMClips(object):

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp

		clip = 	op(self.ownerComp.fetch('CLIP_DATA') +'/'+ 
				self.ownerComp.fetch('CUR_BANK') +'/'+ 
				self.ownerComp.parent().name +'/'+ 
				self.ownerComp.name)

		if clip:

			self.DataClipPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +'/'+ 
												self.ownerComp.fetch('CUR_BANK') +'/'+ 
												self.ownerComp.parent().name +'/'+ 
												self.ownerComp.name)

			self.LabelPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +'/'+ 
												self.ownerComp.fetch('CUR_BANK') +'/'+ 
												self.ownerComp.parent().name +'/'+ 
												self.ownerComp.name +'/label')

			self.ThumbPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +'/'+ 
												self.ownerComp.fetch('CUR_BANK') +'/'+ 
												self.ownerComp.parent().name +'/'+ 
												self.ownerComp.name +'/plugin/config/thumb')

		else:

			self.DataClipPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +
												'/masterClipLane1/' + 
												self.ownerComp.name)

			self.LabelPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +
												'/masterClipLane1/' + 
												self.ownerComp.name +'/label')

			self.ThumbPath = tdu.Dependency(	self.ownerComp.fetch('CLIP_DATA') +
												'/masterClipLane1/' + 
												self.ownerComp.name +'/plugin/config/thumb')



		self.PrevPluginOP = self.ownerComp.fetch('PrevPlugin')
		self.clipCtrlsHeaderText = op.UI.op('clipControls/clipHeader/text')
		self.DB = op.DATABASE
		self.ClipLanes = op.CLIP_LANES_UI
		self.TriggerGroup = self.ClipLanes.op('triggerGroup')

		self.ClipOut = op.CLIP_TRIGGER_MASTER.op('clipOut')
		self.TrigOut = op.CLIP_TRIGGER_MASTER.op('trigOut')

		try:
			self.ClipOP = op(self.DataClipPath.val)
			self.PluginOP = self.ClipOP.op('plugin')
			self.CompAttr = self.PluginOP.fetch('CompAttr')
		except:
			pass

	def AssignClipCtrls(self, dataClipPath, clip, select = False):
		#print('AssignClipCtrls', dataClipPath, clip, select )
		self.ClipOP = op(self.DataClipPath.val)
		self.PluginOP = self.ClipOP.op('plugin')
		self.CompAttr = self.PluginOP.fetch('CompAttr')
	
		prevUIPath = self.ownerComp.fetch('CurUIPath')
		curUIPath = self.CompAttr['attr']['uiPath']
		self.ownerComp.parent(2).store('CurUIPath', curUIPath)
	
		prevCtrls = op(prevUIPath)
		curCtrls = op(curUIPath)

		self.PluginOP.ControlsSelected.val = True
		self.PrevPluginOP.val.ControlsSelected.val = False


		if not self.PluginOP.IsPlaying:
			self.PluginOP.Active = True
		
		if not self.PrevPluginOP.val.IsPlaying and self.PrevPluginOP.val != self.PluginOP:
			self.PrevPluginOP.val.Active = False
		self.PrevPluginOP.val = self.PluginOP

		
		prevPreviewClip = copy.copy(self.ownerComp.fetch('CurPreviewClip'))
		curPreviewClip = self.PluginOP
		self.ownerComp.parent(2).store('CurPreviewClip', curPreviewClip)

		curCtrls.store('CompAttr', self.CompAttr['attr'])
		curCtrls.store('UIAttr', self.CompAttr['uiAttr'])

		curCtrls.store('StoreComp', self.PluginOP)
		curCtrls.store('Parameters', self.PluginOP.op('parameters'))

		if curCtrls.par.Haspresets.eval():
			presets = self.PluginOP.op('presets')
			presetControls = self.CompAttr['attr']['presetControls']
			presetControls.Presets = presets
			curCtrls.op('presets').Presets = presets

			if op.LM.fetch('VIEW_PRESET_CONTROLS') != 0:
				op.PRESET_CONTROLS_VIEW.op('controls').par.selectpanel = presetControls
				#presetControls.UpdateControls()
				presetControls.IsDisplayed = True

			if self.ownerComp.fetch('VIEW_ANIM_EDIT') != 0:
				presetControls.ViewAnimEditor()

		if curUIPath == prevUIPath:
			op(me.fetch('CLIP_CTRLS_UI') +'/selectControls').par.selectpanel = curUIPath

		else:
			if prevCtrls:			
				prevCtrls.store('IsDisplayed', 0)
				prevCtrls.Hide()
				prevCtrls.Linkcompui()

			op(me.fetch('CLIP_CTRLS_UI') +'/selectControls').par.selectpanel = curUIPath
			#curCtrls.Display()

		if op.DATABASE.fetch('CLIP_TRIG_UI') != 1 or select == True:	
			self.PluginOP.PreviewClip()

		else: self.PluginOP.SetViewPreview()

		curCtrls.Display()

		clipCtrlsHeaderText = op.UI.op('clipControls/clipHeader/text')
		#text = 'Clip ' + str(int(clip) + 1) + ' Lane ' + str(self.ClipOP.parent().digits + 1) + ':  ' + self.ClipOP.op('label').par.text.val
		
		bankLabel = op.CLIP_LANES_UI.op('bankSelectContainer/bankSelect/labels')[int(me.fetch('CUR_BANK').replace('bank', '')), 0]

		text = bankLabel 
		text += '/Lane ' + str(self.ClipOP.parent().digits + 1)
		text += '/' + 'Clip ' + str(int(clip) + 1) 
		text += ':  ' + self.ClipOP.op('label').par.text.val


		clipCtrlsHeaderText.par.text = text

	def TriggerLC(self, triggerClip):

		triggerPath = triggerClip.fetch('TriggerPath')
		channel = triggerClip.parent().digits
		clip = op(self.DataClipPath.val).digits
		bank = me.fetch('ROOT').fetch('CUR_BANK')

		triggerClip.parent().store('CurTrigClip', [clip, channel, bank])

		self.ClipOut[channel, 1] = clip
		self.TrigOut[channel, 1] = 1
		run("args[0][args[1], 1] = 0", self.TrigOut, channel, delayFrames = 1, fromOP = self.ownerComp)
		#triggerClip.parent(2).op('trigClipOut')[channel,0] = dataClipPath
		
		#multi radio logic
		
		numClips = op.DATABASE.fetch('NUM_CLIP_SCENES')
		channel = triggerClip.parent().digits
		channelPath = triggerClip.fetch('CLIP_CHAN_VID') +'/'+ triggerClip.parent().name
		clip = triggerClip.parent().panel.radio.val
		
		triggerClip.parent(2).op('prevClipAll').appendRow(clip)
		triggerClip.parent(2).op('prevChannel').appendRow(channel)
		
		prevClipAll = triggerClip.parent(2).op('prevClipAll')[0,0]
		prevChannel = triggerClip.parent(2).op('prevChannel')[0,0]
		

		if op.DATABASE.fetch('CLIP_TRIG_UI') == True:

			self.AssignClipCtrls(self.DataClipPath.val, clip)
			triggerClip.parent(2).store('CurSelClip', [clip, channel, bank])
	
			triggerClip.op('select').click()
	

		'''
		node = me.fetch('NODE')
		remoteMode = op.DATABASE.fetch('REMOTE_MODE')
		if node == 'master' and remoteMode != 0:
			self.CompAttr = op(dataClipPath + '/plugin').fetch('CompAttr')
			clipType = self.CompAttr['attr']['type']
			if clipType == 'movie':
				parms = op(dataClipPath + '/plugin/parameters')
				parms['play', 1] = 1
		'''

		#set globals
		
		
		root = triggerClip.fetch('ROOT')
		root.store('CUR_CLIP', self.DataClipPath.val)
		root.store('CUR_CLIP_LANE',channelPath)


	def ClipState(self, gadget, value):

		trigger = gadget.op('trigger')
		select = gadget.op('select')

		trigger.par.borderaalpha = value
		select.par.borderaalpha = value

	def TriggerRoll(self, gadget, value):

		gadget.par.bgalpha = value * .2 + gadget.panel.lselect * .14

	def SelectRoll(self, gadget):

		rollSelect = .17 + gadget.panel.rollover * .14

		gadget.par.bgcolorr = rollSelect
		gadget.par.bgcolorg = rollSelect + gadget.panel.state * .11
		gadget.par.bgcolorb = rollSelect + gadget.panel.state * .23
	
	def SelectLC(self, selectClip):

		#multi radio logic

		numClips = op.DATABASE.fetch('NUM_CLIP_SCENES')
		
		channel = selectClip.parent().digits
		channelPath = me.fetch('CLIP_CHAN_VID') +'/'+ selectClip.parent().name
		clip = str(int(math.fmod(selectClip.parent(2).panel.radio,numClips)))
		bank = me.fetch('ROOT').fetch('CUR_BANK')

		selectClip.parent(2).store('CurSelClip', [int(clip), channel, bank])

		self.AssignClipCtrls(self.DataClipPath.val, clip, select = True)
	
		selectClip.parent(2).op('prevClipAll').appendRow(clip)
		selectClip.parent(2).op('prevChannel').appendRow(channel)

		#set globals
		
		root = selectClip.fetch('ROOT')
		root.store('CUR_CLIP', self.DataClipPath.val)
		root.store('CUR_CLIP_LANE',channelPath)

	def TriggerExt(self, triggerClip):

		triggerPath = triggerClip.fetch('TriggerPath')		
		channel = op(triggerClip).parent().digits		
		clip = op(self.DataClipPath.val).digits

		bank = me.fetch('ROOT').fetch('CUR_BANK')
		triggerClip.parent().store('CurTrigClip', [clip, channel, bank])

		self.ClipOut[channel, 1] = clip
		self.TrigOut[channel, 1] = 1
		run("args[0][args[1], 1] = 0", self.TrigOut, channel, delayFrames = 1, fromOP = self.ownerComp)

		#multi radio logic
	
		channelPath = triggerClip.fetch('CLIP_CHAN_VID') +'/'+ triggerClip.parent().name

		prevClip = triggerClip.parent().panel.radio

		if triggerClip.parent().op('clip' + str(prevClip)+ '/trigger'):

			triggerClip.parent().op('clip' + str(prevClip)+ '/trigger').panel.state = 0
			
		triggerClip.parent().panel.radio = triggerClip.digits


		triggerClip.op('trigger').panel.state = 1

		#set globals
		
		root = triggerClip.fetch('ROOT')
		root.store('CUR_CLIP', self.DataClipPath.val)
		root.store('CUR_CLIP_LANE',channelPath)

	def CtrlMapTrig(self, triggerClip,val):
		if int(val) == 1:
			triggerClip.op('trigger').click(left = True)

	def CtrlMapSel(self, selectClip, val):
		if int(val) == 1:
			selectClip.op('select').click(left = True)


	def Stop(self, dataClipPath, channel, channelDigits):

		clip = 1001
		#channel.parent().op('trigClipOut')[channelDigits,1]  = clip

		self.ClipOut[channelDigits, 1] = clip
		self.TrigOut[channelDigits, 1] = 1
		run("args[0][args[1], 1] = 0", self.TrigOut, channelDigits, delayFrames = 1, fromOP = self.ownerComp)

		if self.DB.fetch('CLIP_TRIG_MODE') == 0:
			prevClip = channel.panel.radio.val

			if prevClip != -1:
				trig = channel.op('clip' + str(prevClip)+ '/trigger')
		
				if trig:
					trig.panel.state = 0

				channel.panel.radio = -1

		else:
			prevClip = self.ClipLanes.panel.radio.val
			#print(prevClip)
			if prevClip != -1:
				trig = self.ClipLanes.op(self.TriggerGroup[prevClip, 0])
		
				if trig:
					trig.panel.state = 0

				#self.ClipLanes.panel.radio = -1



		curTrigClip = channel.fetch('CurTrigClip')	
		curTrigClip[0] = clip
		channel.store('CurTrigClip', curTrigClip)		
	
	def AssignNoClipCtrls(self):
		#print('AssignClipCtrls', dataClipPath, clip, select )
		self.ClipOP = op.NO_CLIP
		self.PluginOP = self.ClipOP.op('plugin')
		self.CompAttr = self.PluginOP.fetch('CompAttr')

		prevUIPath = self.ownerComp.fetch('CurUIPath')
		curUIPath = self.CompAttr['attr']['uiPath']
		self.ownerComp.parent(2).store('CurUIPath', curUIPath)

		prevCtrls = op(prevUIPath)
		curCtrls = op(curUIPath)

		self.PluginOP.ControlsSelected.val = True

		if self.PrevPluginOP.val:
			self.PrevPluginOP.val.ControlsSelected.val = False

			if not self.PrevPluginOP.val.IsPlaying and self.PrevPluginOP.val != self.PluginOP:
				self.PrevPluginOP.val.Active = False

		self.PrevPluginOP.val = self.PluginOP

		
		prevPreviewClip = copy.copy(self.ownerComp.fetch('CurPreviewClip'))
		curPreviewClip = self.PluginOP
		self.ownerComp.parent(2).store('CurPreviewClip', curPreviewClip)

		curCtrls.store('CompAttr', self.CompAttr['attr'])
		curCtrls.store('UIAttr', self.CompAttr['uiAttr'])

		curCtrls.store('StoreComp', self.PluginOP)
		curCtrls.store('Parameters', self.PluginOP.op('parameters'))

		#if curUIPath == prevUIPath:
		#	op(me.fetch('CLIP_CTRLS_UI') +'/selectControls').par.selectpanel = curUIPath

		if prevCtrls:
			prevCtrls.store('IsDisplayed', 0)
			prevCtrls.Hide()
			prevCtrls.Linkcompui()

		op(me.fetch('CLIP_CTRLS_UI') +'/selectControls').par.selectpanel = curUIPath
		#curCtrls.Display()

		self.PluginOP.PreviewClip()

		#else: self.PluginOP.SetViewPreview()
		op.PRESET_CONTROLS_VIEW.CloseAll()

		curCtrls.Display()

		self.clipCtrlsHeaderText.par.text = 'No Clip Selected'


def ClearBank(bank):
	bankPath = me.fetch('CLIP_DATA') +'/'+ bank
	#print(op(bankPath +'/replicator1'))
	op(bankPath +'/replicator1').par.recreateall.pulse(1)

	ClearClipControlsFindClip()

	

	
def ClearLane(lanePath):
	lane = op(lanePath)
	lane.op('replicator1').par.recreateall.pulse(1)

	uiLane = op.CLIP_LANES_UI.op('clipLane' + str(lane.digits))

	clips = uiLane.findChildren(name = 'clip*', depth = 1)
	curTrigClip = uiLane.fetch('CurTrigClip')

	for clip in clips:

		ClearClipControls(clip)

		if curTrigClip[0] == clip.digits:
			clip.Stop(op.NO_CLIP.path, clip.parent(), clip.parent().digits)


def ClearClipControlsFindClip():
	clips = op.CLIP_LANES_UI.findChildren(name = 'clip*', depth = 2, type = COMP)
	
	for clip in clips:
	
		select = clip.op('select')	
		if select and clip.parent().name != 'masterClipLane1':
		
			if select.panel.state.val == 1:
				op.PRESET_CONTROLS_VIEW.CloseAll()
				run("args[0].click()", select, delayFrames = 1)

			if clip.parent().name != 'masterClipLane1':
				curTrigClip = clip.fetch('CurTrigClip')
				if curTrigClip[0] == clip.digits:
					clip.Stop(op.NO_CLIP.path, clip.parent(), clip.parent().digits)




def ClearClipControls(clip):

	select = clip.op('select')		
	if select.panel.state.val == 1:

	
		ctrls = clip.CompAttr['attr']['uiPath']

		if ctrls:

			ctrls.store('IsDisplayed', 0)
			ctrls.Hide()

		op.PRESET_CONTROLS_VIEW.CloseAll()
		run("args[0].click()", select, delayFrames = 1)

