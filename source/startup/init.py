def CloseViewPresets():

	op.LM.store('VIEW_PRESET_CONTROLS', 0)
	op.PRESET_CONTROLS_VIEW.op('window').par.winclose.pulse()
	op.PRESET_CONTROLS_VIEW.par.display = 0

def InitClipLanes():

	op.CLIP_LANES_UI.store('PrevPlugin', tdu.Dependency(op.NO_CLIP.op('plugin')))

	curSelClip = op.CLIP_LANES_UI.fetch('CurSelClip')
	clip = op.CLIP_LANES_UI.op('clipLane' + str(curSelClip[1])).op('clip' + str(curSelClip[0]))		
	
	select = clip.op('select')
	if select.panel.state.val == 1:
		
		clip.AssignNoClipCtrls()

		select.panel.state = 0
		clip.parent().panel.radio = -1
		
def TrigNoClip():

	op.CLIP_CHAN_VID.op('stopList').clear()

	for i in range(op.CLIP_CHAN_VID.op('channels').numRows - 1):	
		strVal = str(i)
		dataClipPath = me.fetch('CLIP_DATA') +'/'+ me.fetch('CUR_BANK') +'/clipLane' + strVal +'/clip1001'
		
		chan = op.CLIP_CHAN_VID.op('channel' + strVal)
		chan.Trigger(dataClipPath)
		#run("args[0].Trigger(args[1])", chan, dataClipPath, delayFrames = 4, fromOP = me)
		
		noClipPath = op.NO_CLIP.path
		run("args[0].Trigger(args[1])", chan, noClipPath, delayFrames = 30, fromOP = me)
				
	for index in range(op.DATABASE.fetch('NUM_CLIP_LANES')):
		#op(me.fetch('MASTER') + '/ui/clipLanes/laneStop/stop' + str(index)).click([.5, .5])

		strIndex = str(index)
	
		stop = op(me.fetch('MASTER') + '/ui/clipLanes/laneStop/stop' + str(index))
		dataClipPath = me.fetch('CLIP_DATA') +'/'+ me.fetch('CUR_BANK') +'/clipLane' + strIndex +'/clip1001'
		channel = op(me.fetch('UI') + '/clipLanes/clipLane' + strIndex)	
		stop.Stop(dataClipPath, channel, index)
	

	op.UI.op('clipControls/previewClip/viewTOP').par.top = ''

def CookToNodes():

	op.TO_NODES.cook(force = True, recurse = True)
	
def CommandProcSetAddresses():

	address = op.LM.fetch('MASTER_IP')
	OPs = ['auxChannelCtrls', 'masterCtrls', 'clipTrigger', 'midiTrig']
	
	for OP in OPs:
		OP = op.COMMAND_PROC.op(OP).op('touchIn')	
		OP.par.address = address

def InitBrowser():

	op.BROWSER.op('contents/build_storage').run()
	op.BROWSER.op('contents/initialize').run()
	

def InitCuePlayer():

	if me.fetch('NODE') != 'master':
		#op.CUE_PLAYER.op('midiOut').destroy()
		op.CUE_PLAYER.par.extension1 = ''
		op.CUE_PLAYER.par.reinitextensions.pulse()
		op.CUE_PLAYER.allowCooking = False
		
	
def Init():

	op.ANIM_EDITOR.CloseAnimEditor()
	CloseViewPresets()
	InitClipLanes()
	CookToNodes()
	CommandProcSetAddresses()
	op.CUE_PLAYER.EditMode = False
	op.LM.store('VIEW_PRESET_CONTROLS', 0)
	InitBrowser()
	
	if me.fetch('MASTER_MODE') == 0 or op.DATABASE.fetch('PREVIEW_ON'):
	
		TrigNoClip()
		pass
	#print('Init')
	pass

#Init()	