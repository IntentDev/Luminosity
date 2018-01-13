"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""

from pprint import pprint
import copy
LM = op.LM
TC = op.LM.Timecode()
DB = op.DATABASE
TIME = op.TIME

class CuePlayerExt:
	"""
	CuePlayerExt description
	"""
	def __init__(self, ownerComp):
		
		print('Init CuePlayerExt')

		self.ownerComp = ownerComp
		self.CueList = self.ownerComp.op('cueList')
		self.CuePlugin = self.CueList.op('plugin')
		self.CueParsOP = self.CuePlugin.op('parameters')
		self.Presets = self.CuePlugin.op('presets')
		self.AutoUpdateCOMP = self.CuePlugin.op('autoUpdate')
		self.AutoUpdateGetNumPresetsDAT = self.AutoUpdateCOMP.op('getNumPresets')
		self.AutoUpdateGetNumClipsDAT = self.AutoUpdateCOMP.op('getNumClips')

		self.ExecUpdateCueSettings = self.CuePlugin.op('execUpdateCueSettings')
		self.PresetControls = self.CueList.op('presetControls')
		self.PresetList = self.CueList.op('presetControls/presetList')
		self.CueListCtrls = self.CueList.op('controls')
		self.CuePresetsComp = self.CueList.op('plugin/presets')
		self.ClipList = self.CueList.op('clipList')
		self.EnabledListOP = self.CueList.op('enabledList')
		self.PresetControls = self.CueList.op('selPluginPresetControls')
		self.PresetsTypeTabs = self.CueList.op('tabs')
		self.EnabledParsList = self.PresetControls.op('enabledParsList')

		self.UI = self.ownerComp.op('ui')
		self.Controls = self.UI.op('controls')
		self.Transport = self.Controls.op('transport')
		self.TimeBar = self.Controls.op('timeBar')
		self.Timecode = self.Controls.op('timecode')
		self.TimecodeCurrent = self.Timecode.op('timecodeCurrent')
		self.TimecodeCurrentDAT = self.TimecodeCurrent.op('string')
		self.TimecodeTotal = self.Timecode.op('timecodeTotal')
		self.TimecodeTotalDAT = self.TimecodeTotal.op('string')
		self.ScrubSlider = self.TimeBar.op('scrubSlider')
		self.ScrubExport = self.ScrubSlider.op('scrubExport')
		self.Timer = self.ownerComp.op('timer')
		self.SegDAT = self.ownerComp.op('segments')

		self.ClipOut = op.CLIP_TRIGGER_MASTER.op('clipOut')
		self.TrigOut = op.CLIP_TRIGGER_MASTER.op('trigOut')

		self.Node = me.fetch('NODE')

		self.GetFollowTimerActions()
		self.GetSelectCueFuncs()
		self.GetTransportFuncs()

		# modes - some need UI
		self.Initialize = False	

		self.EnableTimeParms()
		self.FollowOn = True
		self.CuePresetIndex = 0
		self.PresetsTypeIndex = int(self.PresetsTypeTabs.op('value')[0].eval())

		pars = self.CuePlugin.fetch('CompPar')['values']
		duration = pars['Duration']['value']
		duration = TC.TimecodeToSeconds(duration)
		
		self.FollowActionVal = pars['FollowAction']['value']
		self.Cycles = pars['NumCycles']['value']	
		durationBarsToSecs = float(pars['DurationBars']['value']) * 4.0 * op.LM.fetch('SPB').val
		self.Duration = [durationBarsToSecs, duration][self.TimeUnitSwitch]

		self.CuePresetIndex = self.PresetList.fetch('CurrentItem')
		self.SelectState = False

		self.CueClips = []
		self.CueClipLanes = []
		self.StoreCueStartTime = 0.0
		self.StoreCueDuration = 30.0

		self.PrevClipTrigger = None

		self.UDT_Out = self.ownerComp.op('udtOut')
		#self.UDP_Out = self.ownerComp.op('udpOut')
		#self.MIDI_Out = self.ownerComp.op('midiOut')

	def StoreCue(self, cueIndex, cueName, update = False):

		self.CueIndex = cueIndex
		self.CueName = cueName

		clipCrossFadeTime = op.CLIP_CROSSFADE_TIME.op('out1')['value'].eval()
		bpm = me.time.tempo

		i = 0
		delayFrames = 0

		if update:

			startTime = self.CuePlugin.fetch('CompPar')['values']['StartTime']['value']
			duration = self.CuePlugin.fetch('CompPar')['values']['Duration']['value']
			self.StoreCueStartTime = TC.TimecodeToSeconds(startTime)
			self.StoreCueDuration = TC.TimecodeToSeconds(duration)	

			clips = self.Presets.Presets[cueIndex]['customData'][2]

			i = 0
			for clipData in clips[0]:

				clip = clipData[0]
				presetState = clipData[1]
				presets = clip.op('plugin/presets')

				if presets and presetState:

					preset = self.GetPreset(presets)
					blendTime = presets.par.Blendtime.eval()

					self.Presets.Presets[cueIndex]['customData'][2][0][i][2] = preset
					self.Presets.Presets[cueIndex]['customData'][2][0][i][3] = blendTime

			i += 1

				#self.CueClips[0] =  [clip, clipPresetOn, preset, 
				#									blendTime, clipName, laneIndex, 
				#									clipLocation]

		else:

			self.CueClips = []
			self.CueClipLanes = []
			clips = [[], []]

		cue = 	[	
					[], 
					copy.deepcopy(self.PresetsDict.val), #copy.deepcopy(self.PresetsList.val), 
					clips, 
					self.StoreCueStartTime, 
					self.StoreCueDuration, 
					clipCrossFadeTime,
					bpm
				]

		for presetsName in self.RecallList:

			presetsData = self.PresetsDict.val[presetsName]

			presets = presetsData['presets']

			if presets:
				
				presetsDelay = presetsData['presetsDelay']
				preset = self.GetPreset(presets)
				blendTime = presets.par.Blendtime.eval()

				cue[0].append(	[
									copy.deepcopy(presets), 
									copy.deepcopy(preset), 
									copy.deepcopy(presetsDelay), 
									blendTime, True
								])

		self.PresetControls.UpdateControls()


		LM.Delay(delayFrames = 1, fromOP = self.ownerComp).Call(self.ownerComp, 'MakeSegmentsTbl')
		#pprint(cue)

		self.Cue = cue
		self.UpdateUI()

		return cue

	def GetPreset(self, presets):

		if self.Settings['SaveLocalPreset'] == 1:

			curBankName = presets.BankName
			presets.SetBank(self.CuePresetsComp.BankName)
			
			if self.CueIndex >= len(presets.Presets) or presets.Preset['name'] != self.CueName:
				preset = presets.StorePreset(self.CueName)
			else:
				preset = presets.UpdatePreset(self.CueIndex)

			presets.SetBank(curBankName)
			presets.UpdateControls()

		else:

			preset = presets.GetPreset(self.CueName)

		return preset

	def RecallCue(self, cuePreset):

		
		if self.AutoUpdate:	

			self.AutoUpdateSetState(False)

			for run in runs:
				if run.group == 'AutoUpdate':
					run.kill()

			delay = LM.Delay(delayFrames = 15, fromOP = me, group = 'AutoUpdate')
			delay.Call(	self.ownerComp, 'AutoUpdateSetState', True)
		
	
		self.ScrubSlider.panel.u = 0

		self.CuePresetIndex = self.PresetList.fetch('CurrentItem')
		self.CueIndex = self.CuePresetIndex
		self.CueName = cuePreset['name']

		cue = cuePreset['customData']
		cueData = cue[0]
		presetsDict = cue[1]
		clips = cue[2][0]
		clipLanes = cue[2][1]
		startTime = cue[3]
		duration = cue[4]
		clipCrossFadeTime = cue[5]
		bpm = cue[6]

		#pprint(presetsDict)
		self.CuePreset = cuePreset
		self.Cue = cue
		self.CueClips = clips
		self.CueClipLanes = clipLanes
		#self.CueClips = copy.deepcopy(clips)
		#self.CueClipLanes = copy.deepcopy(clipLanes)

		i = 0
		for presetsData in cueData:

			presets = presetsData[0]
			presetState = presetsData[4]
			
			#print(presets, presetState)
			if presets and presetState:

				preset = presetsData[1]
				presetsDelay = presetsData[2]
				presetsBlendTime = presetsData[3]


				presets.par.Blendtime = presetsBlendTime
				try:
					#print(presets.path)
					presets.Preset = preset
					presets.Recall(delayFrame = [0, presetsDelay][self.Settings['DelayUIRecall']], playAnim = self.PlayState)
				except:
					#print(e)
					print('Presets Component:', presets.path)
					print('	Is different than Presets Component saved in Cue. Please Update Cue.')

			i += 1

		if self.Settings['RecallClipCrossfade'] == 1:

			op.CLIP_CROSSFADE_TIME.SetPar(clipCrossFadeTime)
			op.CLIP_CROSSFADE_TIME.SetValue(clipCrossFadeTime)

		self.RecallClips(clips)

		if self.Settings['RecallBPM'] == 1:
			TIME.SetTempo(bpm)
			TIME.Sync()


		if self.Settings['CueMode'] == 0 and self.FollowOn:
			pars = cuePreset['lmParameters'][0]['values']
			self.FollowActionVal = pars['FollowAction']['value']
			self.Cycles = pars['NumCycles']['value']			
			durationBarsToSecs = float(pars['DurationBars']['value']) * 4.0 * op.LM.fetch('SPB').val
			self.Duration = [durationBarsToSecs, duration][self.TimeUnitSwitch]
			
			self.SetTimerActions[self.FollowActionVal]()

		
		if self.EditMode:	

			for key, val in presetsDict.items():

				if key in self.PresetsDict.val.keys():
					self.PresetsDict[key]['state'] = val['state']
		
			self.UpdateUI()


		'''
		if me.fetch('NODE') == 'master':	

			firstChar = self.CueName[:1]	
			if firstChar in ['M', 'P', 'I', 'D']:

				msgID = firstChar.replace('D', 'M')

				message = msgID + '/' + str(duration) 
				print('Sending Message: ', message)
			
				self.UDP_Out.send(message, terminator = '\r\n')
				self.UDP_Out.send(message, terminator = '\r\n')
				

				try:

					if firstChar == 'I':
						self.MIDI_Out.sendProgram(1, 100)

					elif firstChar == 'M':
						self.MIDI_Out.sendProgram(1, 0)	

					elif firstChar == 'D':
						self.MIDI_Out.sendProgram(1, 101)	

					else:

						self.MIDI_Out.sendProgram(1, self.CueIndex)

				except:

					pass
			'''

	def RecallNextCue(self):
		i = self.CuePresetIndex + 1
		if i < len(self.Presets.Presets):
			self.PresetList.SelectCell(i, 1)
			self.Presets.RecallPreset(i)
		else:
			self.PresetList.SelectCell(0, 1)
			self.Presets.RecallPreset(0)

	def RecallAgain(self, setList = False):
		self.FollowOn = False
		self.Presets.RecallPreset(self.CuePresetIndex)
		self.FollowOn = True

	def RecallByIndex(self, index):

		self.CuePresetIndex = index
		self.PresetList.SelectCell(self.CuePresetIndex, 1)
		self.Presets.RecallPreset(self.CuePresetIndex)
		self.FollowOn = True

	def RecallClips(self, clips):

		curBank = op.LM.fetch('CUR_BANK')
		triggerClip = me.fetch('NODE') != 'master' or DB.fetch('PREVIEW_ON') == 1
		clipTrigMode = DB.fetch('CLIP_TRIG_MODE')
		isMaster = me.fetch('NODE') == 'master'

		
		for clipData in clips:

			clip = clipData[0]
			presetState = clipData[1]
			preset = clipData[2]
			blendTime = clipData[3]
			laneIndex = clipData[5]
			presetsDelay = 0 
			
			if clip:

				if triggerClip:
					#print('Direct')
					
					if clipTrigMode == 0:
						channel = op.CLIP_CHAN_VID.op('channel' + str(laneIndex))
						channel.Trigger(clip.path)

					else:
						channel = op.CLIP_CHAN_VID.op('channel0')
						channel.Trigger(clip.path)

						
					'''
					# Through Command Proc needs update to set bank... 
					self.ClipOut[laneIndex, 1] = clip.digits
					self.TrigOut[laneIndex, 1] = 1
					run("args[0][args[1], 1] = 0", self.TrigOut, laneIndex, delayFrames = 3, fromOP = self.ownerComp)
					'''
				

				plugin = clip.op('plugin')
				presets = plugin.op('presets')
				isPlayer = plugin.Type == 'movie'

				if isPlayer:
					plugin.par.Play = self.PlayState

				#print(presetState, presets, clip)
				if presetState and presets:
					
					presets.Preset = preset
					presets.par.Blendtime = blendTime
					presets.Recall(delayFrame = [	0, 
													presetsDelay][self.Settings['DelayUIRecall']], 
													playAnim = self.PlayState,
													remote = False)

					plugin.CuePreset = True

				if isMaster:	

					bank = clip.parent(2).name

					if clip.name != 'clip1001' and clip.name != 'noClip':
						clipDigits = clip.digits
						noClip = False
					else: 
						clipDigits = -1	
						noClip = True
					
					#print(clip)

					uiLane = op.CLIP_LANES_UI.op('clipLane' + str(laneIndex))
					prevTrigClip = uiLane.fetch('CurTrigClip')
					trigClip = op.CLIP_LANES_UI.op('clipLane'+ str(prevTrigClip[1]) +'/clip'+ str(prevTrigClip[0]) +'/trigger')

					if trigClip != None:
						trigClip.panel.state = 0

					uiLane.store('CurTrigClip', [clipDigits, laneIndex, bank])
					uiLane.panel.radio = clipDigits

					clipName = clip.name

					

					if self.PrevClipTrigger and clipTrigMode == 2:
						self.PrevClipTrigger.panel.state = 0

					#if clipTrigMode == 0:	
					if not noClip:

						clipTrigger = uiLane.op(clipName).op('trigger')
						clipTrigger.panel.state = [0, 1][curBank == bank]		
						self.PrevClipTrigger = clipTrigger

					else:
						self.PrevClipTrigger = None

	def SetCue(self, cueIndex):

		self.CueIndex = cueIndex
		self.CuePreset = self.Presets.Preset
		self.Cue = self.CuePreset['customData']
		self.CueName = self.CuePreset['name']
	
		PresetsList = self.Cue[1]
		self.CueClips = self.Cue[2][0]
		self.CueClipLanes = self.Cue[2][1]


		for presetsData in PresetsList:
			name = presetsData[0]
			state = presetsData[1]

			if name in self.PresetsDict.val.keys():
				self.PresetsDict[name]['state'] = state

		if self.EditMode:
			self.UpdateUI()

	def MoveCue(self, preset, startIndex, endIndex):

		#print('Move Preset from', startIndex, 'to', endIndex)

		if endIndex > 0 and endIndex < len(self.Presets.Presets) - 1:

			presetBefore = self.Presets.Presets[endIndex - 1]
			presetAfter = self.Presets.Presets[endIndex + 1]
			startTimeBefore = presetBefore['customData'][3]
			startTimeAfter = presetAfter['customData'][3]

			startTime = startTimeBefore + (startTimeAfter - startTimeBefore) * .5

			preset['customData'][3] = startTime
			timecode = TC.SecondsToTimecode(startTime)
			preset['lmParameters'][0]['values']['StartTime']['value'] = timecode

		elif endIndex == 0:

			preset['customData'][3] = 0.0
			preset['lmParameters'][0]['values']['StartTime']['value'] = '00:00:00.00'

			presetAfter = self.Presets.Presets[endIndex + 1]
			presetAfter2 = self.Presets.Presets[endIndex + 2]
			startTimeAfter2 = presetAfter2['customData'][3]

			startTimeAfter = startTimeAfter2 * .5
			self.Presets.Presets[endIndex + 1]['customData'][3] = startTimeAfter
			timecode = TC.SecondsToTimecode(startTimeAfter)
			presetAfter['lmParameters'][0]['values']['StartTime']['value'] = timecode

		else:

			presetBefore = self.Presets.Presets[endIndex - 1]
			startTimeBefore = presetBefore['customData'][3]

			startTime = startTimeBefore + 30

			preset['customData'][3] = startTime
			timecode = TC.SecondsToTimecode(startTime)
			preset['lmParameters'][0]['values']['StartTime']['value'] = timecode

		if startIndex == 0:

			self.Presets.Presets[0]['customData'][3] = 0.0
			self.Presets.Presets[0]['lmParameters'][0]['values']['StartTime']['value'] = timecode





		self.MakeSegmentsTbl()

	#######################################################################

	def SelectCue(self, cueIndex):

		self.CueIndex = cueIndex
		self.Cue = self.Presets.Presets[cueIndex]['customData']

		if not self.PlayState:

			presetsDict = self.Cue[1] 

			for key, val in presetsDict.items():

				if key in self.PresetsDict.val.keys():
					self.PresetsDict[key]['state'] = val['state']

		self.selectCueFuncs[self.TransportState](cueIndex)

		if me.fetch('NODE') == 'master' and DB.fetch('REMOTE_MODE') != 0 and hasattr(op.CONTROL_OUT, 'GetAttrRemote'):

			op.CONTROL_OUT.GetAttrRemote(self.ownerComp, 'SelectCue', cueIndex)

	def SelectCueManualStop(self, cueIndex):	
		self.ScrubSlider.panel.u = 0	
		self.SelectState = True
		self.CuePresetIndex = cueIndex
		self.Presets.RecallPreset(cueIndex)

		self.SetCue(cueIndex)

	def SelectCueManualPause(self, cueIndex):	
		self.ScrubSlider.panel.u = 0		
		self.SelectState = False
		self.CuePresetIndex = cueIndex
		self.Timer.goTo(segment = cueIndex) 
		self.Presets.RecallPreset(cueIndex)

	def SelectCueManualPlay(self, cueIndex):
		self.SelectState = False
		self.CuePresetIndex = cueIndex
		self.Presets.RecallPreset(cueIndex)

	def SelectCueTimelineStop(self, cueIndex):	
		self.ScrubSlider.panel.u = 0	
		self.SelectState = True
		self.CuePresetIndex = cueIndex
		self.Presets.RecallPreset(cueIndex)

		self.SetCue(cueIndex)

	def SelectCueTimelinePause(self, cueIndex):	
		self.ScrubSlider.panel.u = 0		
		self.SelectState = False
		self.CuePresetIndex = cueIndex
		self.Timer.goTo(segment = cueIndex) 
		self.Presets.RecallPreset(cueIndex)

	def SelectCueTimelinePlay(self, cueIndex):	
		self.SelectState = False
		self.CuePresetIndex = cueIndex
		self.Timer.goTo(segment = cueIndex) 

	def GetSelectCueFuncs(self):
		self.selectCueFuncsManual = [	self.SelectCueManualStop, 
										self.SelectCueManualPause, 
										self.SelectCueManualPlay]

		self.selectCueFuncsTimeline = [	self.SelectCueTimelineStop, 
										self.SelectCueTimelinePause, 
										self.SelectCueTimelinePlay]

		self.selectCueFuncs = [self.selectCueFuncsManual, self.selectCueFuncsTimeline][self.Settings['CueMode']]

	def SelectPresets(self, presetsIndex, clipPresets = False):


		select = False

		if not clipPresets:
			presetsName = self.PresetsList[presetsIndex][0]
			allPresets = self.PresetsDict[presetsName]
			if presetsIndex < len(self.PresetsList):
				presetsOP = allPresets['presets']
				select = True

		else:
			clips = self.Cue[2]
			allPresets = clips[0]
			if presetsIndex < len(allPresets):
				presetsOP = allPresets[presetsIndex][0].op('plugin/presets')
				select = True



		if select:
			self.SelectedPresets = presetsOP
			self.PresetControls.UpdateControls()
			self.EnabledParsList.par.reset.pulse()

	def SwitchSelectPresets(self, val):

		if val == 0:
			presetsIndex = self.ClipList.fetch('SelectRow', 1) - 1
			self.SelectPresets(presetsIndex, clipPresets = True)

		elif val == 1:
			presetsIndex = self.EnabledListOP.fetch('SelectRow', 1) - 1
			self.SelectPresets(presetsIndex)

		self.PresetsTypeIndex = val	

	#######################################################################

	def FollowHold(self): pass
	def FollowPlayNext(self): self.RecallNextCue()
	def FollowCycle(self): pass
	def FollowCycleHold(self): pass
	def FollowCycleNext(self): self.RecallNextCue()
	def FollowStop(self): 
		op.STOP_ALL.StopAll()
		self.Timer.par.initialize.pulse()

	# called by timerCallbacks
	def FollowAction(self): self.FollowActions[self.FollowActionVal]()

	def SetTimerHold(self): 

		#self.Timer.par.initialize.pulse()
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = False
		self.Timer.par.cyclelimit = False
		self.Timer.par.start.pulse()

	def SetTimerPlayNext(self):
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = False
		self.Timer.par.cyclelimit = False
		self.Timer.par.start.pulse()
		
	def SetTimerCycle(self):
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = True
		self.Timer.par.cyclelimit = False
		self.Timer.par.start.pulse()
	
	def SetTimerCycleHold(self):
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = True
		self.Timer.par.cyclelimit = True
		self.Timer.par.maxcycles = self.Cycles
		self.Timer.par.start.pulse()

	def SetTimerCycleNext(self):
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = True
		self.Timer.par.cyclelimit = True
		self.Timer.par.maxcycles = self.Cycles
		self.Timer.par.start.pulse()

	def SetTimerStop(self):
		self.Timer.par.length = self.Duration
		self.Timer.par.cycle = False
		self.Timer.par.cyclelimit = False
		self.Timer.par.start.pulse()

	def GetFollowTimerActions(self):

		self.FollowActions = [	self.FollowHold, self.FollowPlayNext, self.FollowCycle, 
								self.FollowCycleHold, self.FollowCycleNext, self.FollowStop]

		self.SetTimerActions = [self.SetTimerHold, self.SetTimerPlayNext, self.SetTimerCycle, 
								self.SetTimerCycleHold, self.SetTimerCycleNext, self.SetTimerStop]

	#######################################################################	

	def MakeSegmentsTbl(self):
		#print('MakeSegmentsTbl')

		#if self.Presets.extensionsReady: # 099 only.... use try for now (need for when PresetsExt compilese
											# when there are no presets (cues))

		try:

			self.SegDAT.clear(keepFirstRow = True)

			i = 0
			numPresets = len(self.Presets.Presets)
			maxPresets = numPresets - 1
			segDurations = []
			segStartTimes = []

			for cuePreset in self.Presets.Presets:

				cue = cuePreset['customData']
				pars = cuePreset['lmParameters'][0]['values']
				startTime = cue[3]
				duration = cue[4]
				
				followActionVal = pars['FollowAction']['value']
				cycles = pars['NumCycles']['value']		
				cycleState = pars['CycleState']['value']	
				durationBarsToSecs = float(pars['DurationBars']['value']) * 4.0 * op.LM.fetch('SPB').val
				duration = [durationBarsToSecs, duration][self.TimeUnitSwitch]
				cycle = int(cycleState > 0)
				cycleLimit = cycle



				if i < maxPresets:
					nextStartTime = self.Presets.Presets[i + 1]['customData'][3]
					trueDuration = abs(nextStartTime - startTime)

					# if updates to timerCHOP are implemented then cycles can be used in timeline mode
					#if cycleState == 0:
					#	duration = trueDuration
					duration = trueDuration


				if i == maxPresets:
					trueDuration = duration

				# if updates to timerCHOP are implemented then cycles can be used in timeline mode
				#self.SegDAT.appendRow([startTime, duration, cycle, cycleLimit, cycles])
				self.SegDAT.appendRow([startTime, duration, 0, cycleLimit, cycles])

				segStartTimes.append(startTime)
				segDurations.append(trueDuration)

				i += 1
			self.SegStartTimes = segStartTimes
			self.SegDurations = segDurations



		except:

			pass

	def UpdateUI(self):

		self.SetLists()
		self.EnabledListOP.par.reset.pulse()
		self.ClipList.par.reset.pulse()

		self.SwitchSelectPresets(self.PresetsTypeIndex)
		
	def SetLists(self):

		recallList = []
		i = 0
		delayFrames = 0
		for presetsListData in self.PresetsList.val:

			presetsDictData = self.PresetsDict.val[presetsListData[0]]
			state = copy.copy(presetsDictData['state'])
			presetsListData[1] = state

			if state:
			
				if i  == 0: delayFrames = 0
				else:
					delayFrames += presetsDictData['presets'].NumPars

				presetsDictData['presetsDelay'] = delayFrames

				i += 1
				
				recallList.append(presetsListData[0])

		self.RecallList = recallList	

	def GetAllPresets(self, *args):
		#print('GetAllPresets', args)

		if len(args) == 0 or args[0] == 1:

			clipChannels = self.GetChannelPresets('clipChannels', 'Clip Chan ')
			auxChannels = self.GetChannelPresets('auxChannels', 'Aux Chan ')
			masterChannels = self.GetChannelPresets('masterChannels', 'Master Chan ')
			compsPresets = self.GetCOMPsPresets([op.COLORS, op.GLOBAL_MODS, op.SCENES])
		
			#print(compsPresets)

			allChannelsList = (clipChannels[0] + auxChannels[0] 
							+ masterChannels[0] + compsPresets[0])
							#

			allChannelsDict = self.mergeDicts(clipChannels[1], auxChannels[1],
							 masterChannels[1], compsPresets[1])

			self.PresetsList.val = allChannelsList
			self.PresetsDict.val = allChannelsDict

			self.PresetsList.modified()
			self.PresetsDict.modified()

			self.SetLists()

		self.MakeSegmentsTbl()
		self.UpdateCuePresetsDicts()

	def UpdateCuePresetsDicts(self):

		for bank, bankData in self.CuePlugin.fetch('CompPresets').items():

			for preset in bankData:
				
				cue = preset['customData']
				#print(bank, preset['name'])
				cuePresetsDict = cue[1]

				for key, val in self.PresetsDict.val.items():

					if key not in cuePresetsDict.keys():

						valCopy = copy.deepcopy(val)
						valCopy['state'] = False

						cuePresetsDict[key] = valCopy	
						#print (key, valCopy)

	def GetCOMPsPresets(self, comps, prependName = ''):

		presetsList = []
		presetsDict = {}
		#print(comps)
		for comp in comps:

			if comp:
				compPresets = comp.findChildren(tags = ['presetsCOMP'])

				for presets in compPresets:

					name = prependName + presets.parent.plugin.Attr['name']
					#print(name)
					presetsList, presetsDict = self.AppendPresetsCOMP(presets, name, 
																	presetsList, presetsDict)

		return presetsList, presetsDict

	def GetChannelPresets(self, chanType, chanName):

		channels = op.CHAN_DATA.op(chanType)
		chansTbl = channels.op('channels')
		chanPresetsList = []
		chanPresetsDict = {}

		for r in chansTbl.rows()[1:]:

			chan = channels.op(r[0].val)

			if chan.HasPresets:

				presets = chan.op('presets')
				channelName = chanName + str(chan.digits + 1)

				chanPresetsList, chanPresetsDict = self.AppendPresetsCOMP(presets, channelName, 
																				chanPresetsList, chanPresetsDict)

			for i in range(6):
				fxPlugin = chan.op('effects/slot' + str(i)).op('plugin')

				if fxPlugin.HasPresets:
					presets = fxPlugin.op('presets')
					name = channelName + ': FX ' + str(fxPlugin.parent().digits + 1) + ': ' + fxPlugin.Attr['name']

					chanPresetsList, chanPresetsDict = self.AppendPresetsCOMP(presets, name, 
																				chanPresetsList, chanPresetsDict)
		return chanPresetsList, chanPresetsDict

	def AppendPresetsCOMP(self, presets, name, presetsList, presetsDict):

		if self.Initialize: state = False

		elif name in self.PresetsDict.val.keys(): 

			state = self.PresetsDict.val[name]['state']

		else: state = False

		#print(name, state)
		presetsList.append([name, state])
		presetsDict[name] = {'name': name, 'state': state, 'presets': presets, 'presetsDelay': 0}

		return presetsList, presetsDict

	#######################################################################	

	def CueDropClip(self, dragItems):
		#print(dragItems)

		if type(dragItems[0]) == buttonCOMP:


			if 'uiClip' in dragItems[0].parent().tags or 'uiClip' in dragItems[0].tags:

				stopClip = False
				
				if 'uiClip' in dragItems[0].parent().tags:

					uiClip = dragItems[0].parent()
					clip = op(uiClip.DataClipPath.val)

				else:

					uiClip = dragItems[0]
					clipPath = op.LM.fetch('CUR_BANK') +'/clipLane'+ str(uiClip.digits) +'/clip1001'
					clip = op.CLIP_DATA.op(clipPath)
					stopClip = True

				stopClipSwitch = int(stopClip)
				stopClipSwitchInv = -1 * stopClipSwitch + 1

				lane = clip.parent()
				bank = clip.parent(2)

				plugin = clip.op('plugin')
				attr = plugin.fetch('CompAttr')['attr']
				clipName = [attr['name'], 'Stop Clip: ClipLane ' + str(lane.digits + 1)][stopClipSwitch]

				if plugin.HasPresets:
					
					presets = plugin.op('presets')
					preset = self.GetPreset(presets)
					blendTime = presets.par.Blendtime.eval()

				else:
					#return
					preset = None
					blendTime = 0.0


				bankIndex = int(me.fetch('CUR_BANK').replace('bank', ''))
				bankLabel = op.CLIP_LANES_UI.op('bankSelectContainer/bankSelect/labels')[bankIndex, 0]

				clipLocation = (bankLabel + '/Lane ' + str(lane.digits + 1) +
								['/Clip ' + str(clip.digits + 1), '/Stop Clip'][stopClipSwitch])
		
				laneIndex = lane.digits
			
	
				clipTrigMode = op.DATABASE.fetch('CLIP_TRIG_MODE')
				clipPresetOn = bool(self.Settings['StoreClipPresetOnDrop'] * stopClipSwitchInv)


				if clipTrigMode == 0:

					if lane.name not in self.CueClipLanes:
						self.CueClipLanes.append(lane.name)
						self.CueClips.append([	clip, clipPresetOn, preset, 
												blendTime, clipName, laneIndex, 
												clipLocation])
					
					else:
						self.CueClips[self.CueClipLanes.index(lane.name)] =  [	clip, clipPresetOn, preset, 
																				0.0, clipName, laneIndex, 
																				clipLocation]

				else:	
					if len(self.CueClips) == 0:
						self.CueClipLanes.append(lane.name)
						self.CueClips.append([	clip, clipPresetOn, preset, 
												blendTime, clipName, laneIndex, 
												clipLocation])
						

					else:
						self.CueClipLanes[0] = lane.name
						self.CueClips[0] =  [	clip, clipPresetOn, preset, 
												blendTime, clipName, laneIndex, 
												clipLocation]


				self.CueClipLanes.sort()

				a = self.CueClips
				b = self.CueClipLanes

				self.CueClips = [a for a, b in sorted(zip(a, b), key = lambda pair: pair[0])]

				self.Presets.Preset['customData'][2][0] = copy.deepcopy(self.CueClips)
				self.Presets.Preset['customData'][2][1] = copy.deepcopy(self.CueClipLanes)

				if self.Settings['SetDurationFromClipOnDrop'] and attr['type'] == 'movie':

					rateRatio = LM.time.rate / attr['sampleRate']
					durationFrames = attr['trueLength'] * rateRatio
					timecode = TC.FramesToTimecode(durationFrames)

					DurationGadget = self.CueListCtrls.op('Duration')
					durationFieldString = DurationGadget.op('timecodeField/string')
					
					DurationGadget.FocusOff(DurationGadget, timecode)
					durationFieldString[0, 0] = timecode


				self.ClipList.par.reset.pulse()
				self.SelectPresets(self.ClipList.fetch('SelectRow') - 1, clipPresets = True)

				if self.AutoUpdateCOMP:

					self.AutoUpdateGetNumPresetsDAT.cook(force = True)
					self.AutoUpdateGetNumClipsDAT.cook(force = True)

	def DropClipCueList(self, dragItems):

		#print(dragItems)

		if type(dragItems[0]) == buttonCOMP:

			if self.PlayState:
				self.Transport.panel.radio = 0


			if self.AutoUpdate:	

				self.AutoUpdateSetState(False)

				for run in runs:
					if run.group == 'AutoUpdate':
						run.kill()

				delay = LM.Delay(delayFrames = 15, fromOP = me, group = 'AutoUpdate')
				delay.Call(	self.ownerComp, 'AutoUpdateSetState', True)


			if 'uiClip' in dragItems[0].parent().tags or 'uiClip' in dragItems[0].tags:

				stopClip = False
				
				if 'uiClip' in dragItems[0].parent().tags:

					uiClip = dragItems[0].parent()
					clip = op(uiClip.DataClipPath.val)

				else:

					uiClip = dragItems[0]
					clipPath = op.LM.fetch('CUR_BANK') +'/clipLane'+ str(uiClip.digits) +'/clip1001'
					clip = op.CLIP_DATA.op(clipPath)
					stopClip = True

				#if not clip.op('plugin').HasPresets:
				#	return

				stopClipSwitch = int(stopClip)
				stopClipSwitchInv = -1 * stopClipSwitch + 1

				lane = clip.parent()
				plugin = clip.op('plugin')
				attr = plugin.fetch('CompAttr')['attr']
				clipName = [attr['name'], 'Stop Clip: ClipLane ' + str(lane.digits + 1)][stopClipSwitch]


				self.SetNewCueSettings()

				self.Presets.StorePreset(clipName)
				cueIndex = len(self.Presets.Presets) - 1
				self.SelectCue(cueIndex)
				#self.PresetList.store('CurrentItem', cueIndex + 1)
				self.PresetList.par.reset.pulse()

				#self.CueDropClip(dragItems)
				op.LM.Delay(delayFrames = 20, fromOP = self.ownerComp).Call(self.ownerComp, 'CueDropClip', dragItems)
				op.LM.Delay(delayFrames = 22, fromOP = self.ownerComp).Call(self.Presets, 'SendPresets')

	def CueDeleteClip(self, clipIndex):

		self.CueClips.pop(clipIndex)
		self.CueClipLanes.pop(clipIndex)
		self.ClipList.par.reset.pulse()

	def CueUpdateClipPreset(self, clipIndex):

		self.CueClips = self.Presets.Presets[self.CueIndex]['customData'][2][0]

		clipData = self.CueClips[clipIndex]
		clip = clipData[0]
		presetState = clipData[1]
		preset = clipData[2]
		name = clipData[4]
		plugin = clip.op('plugin')

		if presetState:

			clipData[1] = False

		elif not preset:

			if clip:
				
				if plugin.HasPresets:
					
					presets = plugin.op('presets')
					preset = self.GetPreset(presets)
					blendTime = presets.par.Blendtime.eval()

					clipData[1] = True
					clipData[2] = preset
					clipData[3] = blendTime

		else:

			updatePreset = ui.messageBox('Update Preset', 
							'Keep Current Preset or Update Preset for Clip: ' + name, 
							buttons = ['Keep Current', 'Update'])

			if updatePreset == 1:

				if clip:
				
					if plugin.HasPresets:
						
						presets = plugin.op('presets')
						preset = self.GetPreset(presets)
						blendTime = presets.par.Blendtime.eval()

						clipData[1] = True
						clipData[2] = preset
						clipData[3] = blendTime

			elif updatePreset == 0:

				clipData[1] = True

		if self.AutoUpdateCOMP:

			self.AutoUpdateGetNumPresetsDAT.cook(force = True)
			self.AutoUpdateGetNumClipsDAT.cook(force = True)



		
		#print(self.CueClips[clipIndex])

		self.ClipList.par.reset.pulse()

	def CueUpdatePresetsState(self, presetsIndex, state):

		#print(self.RecallList)

		presetsName = self.PresetsList.val[presetsIndex][0]

		self.PresetsList.val[presetsIndex][1] = state
		self.Presets.Preset['customData'][1][presetsName]['state'] = state


		presets = self.PresetsDict.val[presetsName]['presets']
		presetsData = self.PresetsDict.val[presetsName]

		hasStoredPreset = False

		i = 0
		for storedPresets in self.Cue[0]:
			if presets == storedPresets[0]:
				hasStoredPreset = True

				break
			i += 1

		if state:

			#print(hasStoredPreset)

			if hasStoredPreset:

				updatePreset = ui.messageBox(

									'Update Preset', 
									'Keep Current Preset or Update Preset for : ' + presetsName, 
									buttons = ['Keep Current', 'Update'])

				if updatePreset == 1:

					if presets:
				
						presetsDelay = presetsData['presetsDelay']
						preset = self.GetPreset(presets)
						blendTime = presets.par.Blendtime.eval()
						#self.Presets.Preset['customData'][0][i]
						self.Cue[0][i] = [	copy.deepcopy(presets), 
											copy.deepcopy(preset), 
											copy.deepcopy(presetsDelay), 
											blendTime, state]

				else:

					self.Cue[0][i][4] = state

			else:

				if presets:
			
					presetsDelay = presetsData['presetsDelay']
					preset = self.GetPreset(presets)
					blendTime = presets.par.Blendtime.eval()

					self.Cue[0].append([	copy.deepcopy(presets), 
											copy.deepcopy(preset), 
											copy.deepcopy(presetsDelay), 
											blendTime, state])

		else:

			if hasStoredPreset:

				self.Cue[0][i][4] = state


		if self.AutoUpdateCOMP:

			self.AutoUpdateGetNumPresetsDAT.cook(force = True)
			self.AutoUpdateGetNumClipsDAT.cook(force = True)

	def CueUpdateSettings(self):

		compPar = copy.deepcopy(self.CuePlugin.fetch('CompPar'))
		self.Presets.Preset['lmParameters'] = [	compPar, self.CueParsOP.text]


		startTime = compPar['values']['StartTime']['value']
		startTime = TC.TimecodeToSeconds(startTime)
		duration = compPar['values']['Duration']['value']
		duration = TC.TimecodeToSeconds(duration)

		self.Presets.Preset['customData'][3] = startTime
		self.Presets.Preset['customData'][4] = duration

		self.MakeSegmentsTbl()

	#######################################################################

	def GetSettings(self):
		settings = {key: val['value'] for key, val in 
						self.ownerComp.op('cuePlayerSettings/plugin').fetch('CompPar')['values'].items()}
		#pprint(settings)

		self.AutoUpdate = bool(settings['AutoUpdate'] * self.EditMode)
		self.Settings = settings

	def AutoUpdateSetState(self, state):

		execDATs = self.AutoUpdateCOMP.findChildren(tags = ['execUpdatePreset'])

		for execDAT in execDATs:

			execDAT.par.active = state

		self.ExecUpdateCueSettings.par.active = state

	def mergeDicts(self, *dict_args):
		result = {}
		for dictionary in dict_args:
			result.update(dictionary)
		return result

	def CueMode(self, val):
		#print('CueMode', val)
		self.EnableTimeParms()

		self.Timer.par.segdat = ['', 'segments'][val]
		self.selectCueFuncs = [self.selectCueFuncsManual, self.selectCueFuncsTimeline][val]
		self.transportFunc = [self.TransportManual, self.TransportTimeline][self.Settings['CueMode']]

	def SetPars(self, controls, pars):
	
		for par in pars:
			controls.SetPar(controls.op(par[0]), 'value', par[1])	

	def SetNewCueSettings(self):

		self.AutoUpdateSetState(False)
		
		for run in runs:
			if run.group == 'AutoUpdate':
				run.kill()

		delay = LM.Delay(delayFrames = 15, fromOP = me, group = 'AutoUpdate')
		delay.Call(	self.ownerComp, 'AutoUpdateSetState', True)

		if len(self.Presets.Presets) > 0:
			prevCueIndex = len(self.Presets.Presets) - 1
			startTime = self.Presets.Presets[prevCueIndex]['lmParameters'][0]['values']['StartTime']['value']
			startTime = TC.TimecodeToSeconds(startTime) + 30

		else:
			startTime = 0.0


		self.StoreCueStartTime = startTime
		self.StoreCueDuration = 30

		cueSettings = 	[	
							['StartTime', TC.SecondsToTimecode(startTime)],
							['Duration', '00:00:30.00'],
							['DurationBars', 4],
							['CycleState', 0],
							['NumCycles', 4]	
						]

		self.SetPars(self.CueListCtrls, cueSettings)

	def EnableTimeParms(self):
		self.GetSettings()
		#print('Enable', self.Settings['CueMode'])

		StartTime = self.CueListCtrls.op('StartTime')
		Duration = self.CueListCtrls.op('Duration')
		DurationBars = self.CueListCtrls.op('DurationBars')
		FollowAction = self.CueListCtrls.op('FollowAction')
		CycleState = self.CueListCtrls.op('CycleState')
		NumCycles = self.CueListCtrls.op('NumCycles')

		timeUnits = op.DATABASE.fetch('TIME_UNITS').val

		self.TimeUnits = timeUnits

		if self.Settings['CueMode'] == 0 and timeUnits == 0:
			#StartTime.par.display = False
			Duration.par.display = False
			DurationBars.par.display = True
			CycleState.par.display = False
			FollowAction.par.display = True
			NumCycles.par.display = True

			self.TimeUnits = 'beats'

		elif self.Settings['CueMode'] == 0 and timeUnits == 1:
			#StartTime.par.display = False
			Duration.par.display = True
			DurationBars.par.display = False
			CycleState.par.display = False
			FollowAction.par.display = True
			NumCycles.par.display = True

			self.TimeUnits = 'seconds'

		elif self.Settings['CueMode'] == 1:
			#StartTime.par.display = True

			# if timerCHOP is updated then cycles can be implemented in timeline mode
			# Duration, CycleState and NumCycles will need to be displayed
			Duration.par.display = False
			DurationBars.par.display = False
			CycleState.par.display = False
			FollowAction.par.display = True
			NumCycles.par.display = False
			self.TimeUnits = 'seconds'

		self.TimeUnitSwitch = ['beats', 'seconds'].index(self.TimeUnits)

	def CleanUpCues(self, *args):

		if len(args) == 0 or args[0] == 1:

			#pprint(self.PresetsDict.val)

			for key, playlist in self.Presets.StoreComp.fetch('CompPresets').items():

				#for cueIndex in range(len(self.Presets.Presets)):
				for cueIndex in range(len(playlist)):

					#cue = self.Presets.Presets[cueIndex]['customData']
					cue = playlist[cueIndex]['customData']
					cueData = cue[0]
					presetsDict = cue[1]
					clips = cue[2][0]
					clipLanes = cue[2][1]

					pprint(presetsDict)

					noneKeys = []

					for key in presetsDict.keys():
						if key not in self.PresetsDict.val.keys():

							#print(presetsDict[key])
							noneKeys.append(key)


					#pprint(presetsDict)
					nonePresetsData = []

					for key in noneKeys:
						i = 0
						for presetsData in cueData:

							presets = presetsData[0]

							if presets == presetsDict[key]['presets']:

								#pprint(presetsData)
								nonePresetsData.append(i)


							i += 1

					for key in noneKeys:

						print(key)
						#self.Presets.Presets[cueIndex]['customData'][1].pop(key)
						playlist[cueIndex]['customData'][1].pop(key)

					nonePresetsData.sort()
					for presetsIndex in reversed(nonePresetsData):

						print(nonePresetsData)
						#self.Presets.Presets[cueIndex]['customData'][0].pop(presetsIndex)
						playlist[cueIndex]['customData'][0].pop(presetsIndex)


			self.Presets.par.reinitextensions.pulse()

				

	#######################################################################

	def PlayScrubOn(self, u, state):
		if self.TransportState == 2:
		
			#u = self.ScrubSlider.panel.u
			offset = u * .0001 + u
			run("args[0].panel.u = args[1]", self.ScrubSlider, 
				offset, delayFrames = 1, fromOP = me)
			
			self.TransportState = 1
			self.TransportStatePrev = 2
			self.PlayScrubActive = True

		self.PresetsAnimClipsScrubSetState(state)

		if me.fetch('NODE') == 'master' and DB.fetch('REMOTE_MODE') != 0 and hasattr(op.CONTROL_OUT, 'GetAttrRemote'):
			op.CONTROL_OUT.GetAttrRemote(self.ownerComp, 'PlayScrubOn', u, state)

	def PlayScrubOff(self, state):

		if self.PlayScrubActive:
			self.TransportState = 2
			self.PlayScrubActive = False	

		self.PresetsAnimClipsScrubSetState(state)

		if me.fetch('NODE') == 'master' and DB.fetch('REMOTE_MODE') != 0 and hasattr(op.CONTROL_OUT, 'GetAttrRemote'):
			op.CONTROL_OUT.GetAttrRemote(self.ownerComp, 'PlayScrubOff', state)

	def SetSecondsCurrent(self, seconds):

		if self.TransportState == 0:
			self.SetScrubWithSeconds(0)
			self.TimecodeCurrentDAT[0, 0] = '00:00:00.00'

		elif self.TransportState == 1:
			self.SetScrubWithSeconds(seconds)
			
		elif self.TransportState == 2:
			self.Transport.panel.radio = 1
			self.SetScrubWithSeconds(seconds)
			run("args[0].panel.radio = 2", self.Transport, delayFrames = 1, fromOP = me)

	def SetScrubWithSeconds(self, seconds):

		duration = self.SegDurations[self.CuePresetIndex]
		fraction =  seconds / duration
		self.ScrubSlider.click(fraction)

	def PresetsAnimationSetPar(self, cueData, par, value):

		for presetsData in cueData:

			presets = presetsData[0]
			if presets:
				#if presets.HasAnimation:
				anim = presets.Animation.CurAnim
				setattr(anim.par, par, value)

	def ClipSetPar(self, clips, par, value):

		for clipData in clips:

			clip = clipData[0]
			presetState = clipData[1]

			if clip:
				plugin = clip.op('plugin')
				presets = plugin.op('presets')

				isPlayer = plugin.Type == 'movie'
				#print(plugin, isPlayer)
				if isPlayer:
					if par == 'cue':
						plugin.par.Cuescrubactive = value
						
					elif par == 'cuepoint':
						plugin.par.Cuescrub = value
						
					elif par == 'play':
						plugin.par.Play = value

				if plugin.HasAnimation:		
				#if presetState and plugin.HasAnimation:
					anim = presets.Animation.CurAnim
					setattr(anim.par, par, value)			

	def PresetsAnimClipsScrub(self, fraction):
		#print(fraction)
		if self.TransportState > 0:
			cueData = self.Cue[0]
			clips = self.Cue[2][0]
			duration = self.Cue[4]

			frame = fraction * duration * op.LM.time.rate + 1

			self.PresetsAnimationSetPar(cueData, 'cuepoint', frame)
			self.ClipSetPar(clips, 'cuepoint', frame)

		if me.fetch('NODE') == 'master' and DB.fetch('REMOTE_MODE') != 0 and hasattr(op.CONTROL_OUT, 'GetAttrRemote'):
			op.CONTROL_OUT.GetAttrRemote(self.ownerComp, 'PresetsAnimClipsScrub', fraction)

	def PresetsAnimClipsScrubSetState(self, state):

		cueData = self.Cue[0]
		clips = self.Cue[2][0]

		self.PresetsAnimationSetPar(cueData, 'cue', state)
		self.ClipSetPar(clips, 'cue', state)

	def PresetsAnimClipsPlaySetState(self, state):

		cueData = self.Cue[0]
		clips = self.Cue[2][0]

		self.PresetsAnimationSetPar(cueData, 'play', state)
		self.ClipSetPar(clips, 'play', state)

	#######################################################################	

	def TransportManual(self, value):
		self.transportFuncsManual[value]()

	def TransportTimeline(self, value):
		self.transportFuncsTimeline[value]()

	def TransportManualStop(self):
		self.TimelineStop()	

	def TransportManualPause(self):
		self.ScrubSlider.panel.u = self.Timer['timer_fraction'].eval()
		self.PresetsAnimClipsPlaySetState(False)

		if self.TransportState == 0:
			self.Presets.RecallPreset(self.CuePresetIndex)

	def TransportManualPlay(self):

		if self.TransportState == 0 or self.TransportStatePrev == 0:
			#print('Stop to Play', self.CuePresetIndex)
			self.SelectState = False

			if self.Settings['TimecodeSlave'] == 0:
				self.Presets.RecallPreset(self.CuePresetIndex)
				self.Timer.par.start.pulse()

		self.PresetsAnimClipsPlaySetState(True)

	def TransportTimelineStop(self):
		self.TimelineStop()	

	def TransportTimelinePause(self):
		self.ScrubSlider.panel.u = self.Timer['timer_fraction'].eval()
		self.PresetsAnimClipsPlaySetState(False)

		if self.TransportState == 0:
			self.Presets.RecallPreset(self.CuePresetIndex)

	def TransportTimelinePlay(self):
		if self.TransportState == 0 or self.TransportStatePrev == 0:
		
			#print('Stop to Play')
			self.SelectState = False
			self.Timer.goTo(segment = self.CuePresetIndex)
			#self.Timer.par.start.pulse()

		'''
		# don't trigger while paused after stop
		elif self.TransportState == 1 and self.TransportStatePrev == 0:
			print('Pause to Play')
			self.Timer.goTo(segment = self.CuePresetIndex)
			self.Timer.par.start.pulse()
		'''
		self.PresetsAnimClipsPlaySetState(True)

	def GetTransportFuncs(self):

		self.transportFuncsManual = [ 	self.TransportManualStop,
										self.TransportManualPause,
										self.TransportManualPlay]

		self.transportFuncsTimeline = [ self.TransportTimelineStop,
										self.TransportTimelinePause,
										self.TransportTimelinePlay]	

		self.transportFunc = [self.TransportManual, self.TransportTimeline][self.Settings['CueMode']]							

	def TimelineStop(self):
		#print('timelineStop')
		self.AutoUpdateSetState(False)
	
		self.ScrubSlider.panel.u = 0	
		self.Timer.par.initialize.pulse()
		self.Timer.par.cue = 0

		self.SelectState = True
		self.PresetList.SelectCell(0, 1)
		self.Presets.RecallPreset(0)
		self.CuePresetIndex = 0

		self.Transport.panel.radio = 0
		self.Transport.panel.lradio = 0
		self.Transport.op('play').panel.state = 0
		self.Transport.op('pause').panel.state = 0
		self.Transport.op('stop').panel.state = 1

		self.PresetsAnimClipsPlaySetState(False)



		self.SetCue(0)

		op.STOP_ALL.StopAll()

	#######################################################################	
	@property
	def Settings(self):
		return self.ownerComp.fetch('Settings', tdu.Dependency({})).val

	@Settings.setter
	def Settings(self, value):
		self.ownerComp.store('Settings', tdu.Dependency(value))

	@property
	def PresetsList(self):
		return self.ownerComp.fetch('PresetsList', tdu.Dependency([]))

	@PresetsList.setter
	def PresetsList(self, value):
		self.ownerComp.store('PresetsList', tdu.Dependency(value))

	@property
	def PresetsDict(self):
		return self.ownerComp.fetch('PresetsDict', tdu.Dependency({}))

	@PresetsDict.setter
	def PresetsDict(self, value):
		self.ownerComp.store('PresetsDict', tdu.Dependency(value))

	@property
	def RecallList(self):
		return self.ownerComp.fetch('RecallList', [])

	@RecallList.setter
	def RecallList(self, value):
		self.ownerComp.store('RecallList', value)

	@property
	def SelectedPresets(self):
		return self.ownerComp.fetch('SelectedPresets', tdu.Dependency(None))

	@SelectedPresets.setter
	def SelectedPresets(self, value):
		self.ownerComp.store('SelectedPresets', tdu.Dependency(value))
		self.PresetControls.Presets = value

	@property
	def Cue(self):
		return self.ownerComp.fetch('Cue', tdu.Dependency([])).val

	@Cue.setter
	def Cue(self, value):
		self.ownerComp.store('Cue', tdu.Dependency(value))

	@property
	def EditMode(self):
		return self.ownerComp.fetch('EditMode', tdu.Dependency(True)).val

	@EditMode.setter
	def EditMode(self, value):

		self.UI.op('editMode').panel.state = value
		
		self.AutoUpdate = bool(value * self.Settings['AutoUpdate'] * min(1, self.TransportState))
		self.ownerComp.store('EditMode', tdu.Dependency(value))

		self.UpdateUI()
		if value:
			#self.CueListCtrls.Display()
			self.CueListCtrls.store('IsDisplayed', 1)
		else:
			self.CueListCtrls.store('IsDisplayed', 0)

	@property
	def TransportState(self):
		return self.ownerComp.fetch('TransportState', 0)

	@TransportState.setter
	def TransportState(self, value):
		#print(value)
		active = min(1, value)
		self.Timer.par.play = active
		cue = -1 * (max(0, value - 1)) + 1
		self.Timer.par.cue = cue

		self.transportFunc(value)	
			
		if self.TransportState == 0 and value == 1:
			self.TransportStatePrev = 0
		
		else:
			self.TransportStatePrev = self.TransportState		

		self.ScrubExport.export = min(1, value)
		self.ownerComp.store('TransportState', value)
		self.PlayState = bool(max(0, value - 1))

		self.AutoUpdate = bool(active * self.Settings['AutoUpdate'] * int(self.EditMode))

		if me.fetch('NODE') == 'master' and DB.fetch('REMOTE_MODE') != 0 and hasattr(op.CONTROL_OUT, 'SetAttrRemote'):
			op.CONTROL_OUT.SetAttrRemote(self.ownerComp, 'TransportState', value)

	@property
	def PlayState(self):
		return self.ownerComp.fetch('PlayState', False)

	@PlayState.setter
	def PlayState(self, value):

		self.ownerComp.store('PlayState', value)

	@property
	def TransportStatePrev(self):
		return self.ownerComp.fetch('TransportStatePrev', 0)

	@TransportStatePrev.setter
	def TransportStatePrev(self, value):
		self.ownerComp.store('TransportStatePrev', value)
		
	@property
	def PlayScrubActive(self):
		return self.ownerComp.fetch('PlayScrubActive', False)

	@PlayScrubActive.setter
	def PlayScrubActive(self, value):
		self.ownerComp.store('PlayScrubActive', value)

	@property
	def SegDurations(self):
		return self.ownerComp.fetch('SegDurations', [])

	@SegDurations.setter
	def SegDurations(self, value):
		self.ownerComp.store('SegDurations', value)


	@property
	def SegStartTimes(self):
		return self.ownerComp.fetch('SegStartTimes', [])

	@SegStartTimes.setter
	def SegStartTimes(self, value):
		self.ownerComp.store('SegStartTimes', value)

	@property
	def AutoUpdate(self):
		return self.ownerComp.fetch('AutoUpdate', tdu.Dependency(True)).val

	@AutoUpdate.setter
	def AutoUpdate(self, value):

		self.AutoUpdateSetState(value)
		self.ownerComp.store('AutoUpdate', tdu.Dependency(value))
		




