class SendData(object):

	def __init__(self):

		self.lm = op('/Luminosity')
		self.remote = op('/Luminosity/remote')

		return

	def SendPar(self, comp, par):

		data = par.val	
		args = [comp.path, par.name]		
		extOP = '/Luminosity'	
		className = 'SetData'		
		functionName = 'SetPar' 
			
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		#self.DataOut.send(msg, terminator = '')

		self.remote.SetPar(comp, par.name, par.eval())

	def SendParTable(self, dat):

		import tableFunc as tF

		data = {r[0].val:tF.SetToType(r[1].val) for r in dat.rows()[1:]}	
		args = [dat.path]		
		#extOP = '/Luminosity'	
		#className = 'SetData'		
		#functionName = 'SetParTable' 
			
		#msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		#self.DataOut.send(msg, terminator = '')

		self.remote.GetAttr(self.lm, 'SetParTable', data, dat.path)

	def SendParTablePar(self, dat, cells, prev):

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetParTablePar' 
	
		
		for c in cells:

			self.remote.GetAttr(self.lm, 'SetParTablePar', c.val, dat.path, c.row, c.col)

	def SendDAT(self, dat):

		data = dat.text	

		self.remote.GetAttr(self.lm, 'SetDAT', data, dat.path)

	def SendStorageKey(self, value, name, path):

		#print('SendStorageKey', name, path)

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetStorageKey'
		prepend = extOP +'::'+ className +'::'+ functionName +'::'

		self.remote.GetAttr(self.lm, 'SetStorageKey', value, name, path)

	def SendTDControl(self, value, functionName):

		self.remote.GetAttr(self.lm, functionName, value)

	def SendCue(self, cue):
	
		self.remote.GetAttr(self.lm, 'SetCue', cue)

	def SendRecallPreset(self, preset, path):
		#print(preset, path)

		if path != '/Luminosity/database/cuePlayer/cueList/plugin/presets':

			self.remote.GetAttr(self.lm, 'SetRecallPreset', preset, path)


class SetData(object):

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.remote = ownerComp.op('remote')
		self.setMapData = setMapData(ownerComp)
		
	def Save(self, node):

		#print('Save')
		if node == me.fetch('NODE'):
			project.save()

	def Quit(self, node):

		#print('Quit')
		if node == me.fetch('NODE'):
			project.quit(force = True)

	def Realtime(self, active):

		realTime(active)


	def SetParTable(self, data, tablePath):
	
		table = op(tablePath)

		for key,val in data.items():
		
			table[key, 1] = val
			#print(key, val)

	def SetTable(self, data, path):
	
		table = op(path)
		#print(table)
		table.clear()

		#print(data)

		for n in data:

			table.appendRow(n)
			
	def SetPar(self, data, path, parameter):
		
		setattr(op(path).par, parameter, data)

	def SetParTablePar(self, value, path, row, col):

		op(path)[row, col] = value

	def SetStorageKey(self, value, name, path):

		op(path).store(name, mod.tableFunc.SetToType(value))

	def SetPresets(self, compPresets, path, bankName, curPresets):

		presets = op(path)
		storeComp = presets.StoreComp
		storeComp.store('CompPresets', mod.tableFunc.SetToType(compPresets))
		presets.SetBank(bankName)
		presets.Presets = curPresets
		storeComp.store('CurPresets', curPresets)

	def SetAnimKeys(self, keys, path):

		ParAnimCOMP = op(path)
		animCOMP = ParAnimCOMP.CurAnim
		animCOMP.op('keys').text = mod.tableFunc.SetToType(keys)[0]

	def SetAnimChannels(self, channels, path):

		ParAnimCOMP = op(path)
		animCOMP = ParAnimCOMP.CurAnim
		animCOMP.op('channels').text = mod.tableFunc.SetToType(channels)[0]
	
	def SetRecallPreset(self, data, path):
		#print(data, path)
		presets = op(path)
		#presets.Preset = data
		presets.RecallPreset(data)
		#print('SetRecallPreset')

	def SetCue(self, cue):
		op(me.fetch('CUE_PLAYER')).op('recallCue/list/list/cellId')[0,0] = cue

	def RemoteLoadClip(self, *args):
		data = args[0]
		op.LOAD_CLIPS.RemoteLoadClip(data)


	def SetMapData(self, server, gpu, path, name, mapData):

		gpuPath = self.ownerComp.fetch('GPU_PATH')
	
		if str(self.ownerComp.fetch('SERVER')) == server and str(self.ownerComp.fetch('GPU')) == gpu:		
				
			if path == 'gpu':
				settingsPath = gpuPath + '/settings'
				self.setMapData.gpu(settingsPath, name, mapData)
				
			else:	
				mapDataPath = op(gpuPath +'/'+ path +'/mapData')
				
				#if name in dir(setMapData):
				getattr(self.setMapData, name)(mapDataPath, path, name, mapData)


class setMapData:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

	def gpu(self, path, name, value):
		gpuPath = self.ownerComp.fetch('GPU_PATH')
		settings = op(path)
		settings[name, 1] = value
		
	def setup(self, path, output, name, value):
		settings = self.ownerComp.fetch('GPU_PATH') +'/'+ output +'/settings'
		for key,val in value.items():
			op(settings)[key, 1] = val

	def camSchSetupData(self, path, output, name, value):
		camSch = op(self.ownerComp.fetch('CAMSCHNAPPR'))
		mapData = op(path)
		mapData[name, 1] = value	
		camSch.op('sndRcvRcl/receiveSetupData').run(value)

	def camSchCalData(self, path, output, name, value):
		camSch = op(self.ownerComp.fetch('CAMSCHNAPPR'))
		mapData = op(path)
		mapData[name, 1] = value
		camSch.op('sndRcvRcl/receiveCalData').run(value)

	def camSchRecall(self, path, output, name, value):
		if value == 1:
			camSch = op(self.ownerComp.fetch('CAMSCHNAPPR'))
			mapData = op(path)
			mapData[name, 1] = value
			calData = eval(mapData['camSchCalData',1].val)
			setupData = eval(mapData['camSchSetupData',1].val)
			
			setup = eval(mapData['setup', 1].val)
			mapPrimary = str(setup['mapPrimary'])
			matrix = mapData.parent().op('matrix' + mapPrimary)
			exports = mapData.parent().op('exports' + mapPrimary)
		
			camSch.store('StoreDataOP', matrix.path)
			camSch.store('SendDataOP', mapData.path)
			camSch.store('MatrixPath', matrix.path)
			camSch.store('ExportsPath', exports.path)
			
			camSch.op('sndRcvRcl/receiveSetupData').run(setupData, delayFrames = 1)
			camSch.op('sndRcvRcl/receiveCalData').run(calData, delayFrames = 2)
			camSch.op('sndRcvRcl/remoteRecallInit').run(calData, delayFrames = 3)
		
	def edgeBlendSettings(self, path, output, name, value):
		op(path)[name, 1] = value
		output = op(self.ownerComp.fetch('GPU_PATH') +'/'+ output)
		parms = output.op('edgeBlendParameters')
		settings = output.op('edgeBlendSettings')

		setup = value['setup']
		for key,val in setup.items():
			parms[key, 1] = val

		value.pop('setup')

		for side,par in value.items():
			for key,v in par.items():
				settings[key, side] = v 



	def warpData(self, path, output, name, value):
		op(path)[name, 1] = value	
		warpOP = op(self.ownerComp.fetch('WARP'))
		warp = warpOP.mod.remoteWarp.Warp()
		warp.remoteControl(value, self.ownerComp.fetch('OUTPUTS') +'/'+ output +'/map2d/mapView')

		
	def maskData(self, path, output, name, value):
		op(path)[name, 1] = value

	def auxData(self, path, output, name, value):
		op(path)[name, 1] = value						


class Load(object):

	def __init__(self):
		self.lm = op('/Luminosity')
		self.remote = op('/Luminosity/remote')

	def LoadInsert(self, path, dataSlotPath):

		#print(dataSlotPath)

		pathList = dataSlotPath.split('/')
		group = pathList[4]
		channel = pathList[5]
		slot = pathList[7]

		#print('Load Slot:', pathList)
		import copy

		slotComp = op(dataSlotPath)
		slotCompParent = slotComp.parent()
		slotCompName = slotComp.name
		slotCompNodeX = slotComp.nodeX
		slotCompNodeY = slotComp.nodeY
		select = slotComp.op('select1')
		selectPath = select.par.top.eval()

		slotComp.destroy()

		slotComp = slotCompParent.loadTox(path)
		slotComp.name = slotCompName
		slotComp.nodeX = slotCompNodeX
		slotComp.nodeY = slotCompNodeY

		if not slotComp.op('select1'):
			select = slotComp.create(selectTOP, 'select1')
		else:
			select = slotComp.op('select1')

		plugin = slotComp.op('plugin')
		compAttr = plugin.fetch('CompAttr')
		compPar = plugin.fetch('CompPar')

		select.outputConnectors[0].connect(plugin.inputConnectors[0])
		select.par.top = selectPath
		plugin.cook(force = True, recurse = True)
		plugin.par.reinitextensions.pulse()

		ctrls = slotComp.op('controls')

		parNames = [r[0].val for r in plugin.op('parameters').rows()[1:]]
		compAttr['attr']['uiPath'] = ctrls
		
		ctrls.Createcompui(reCreate = False)

		op('/Luminosity/master/ui/channelCtrls/clipChannelCtrls/selectControls').cook(force = True)
		op('/Luminosity/master/ui/channelCtrls/auxChannelCtrls/selectControls').cook(force = True)
		op('/Luminosity/master/ui/channelCtrls/masterChannelCtrls/selectControls').cook(force = True)

		if plugin.HasPresets:

			presets = plugin.op('presets')
			presets.initializeExtensions()
			presetControls = slotComp.op('presetControls')
			compAttr['attr']['presetControls'] = presetControls
			presetControls = compAttr['attr']['presetControls']
			presetControls.Presets = presets
			
		btnCtrlMapSets = ctrls.findChildren(name = 'buttonCtrlMapSet')
		for btn in btnCtrlMapSets:
			btn.op('setup').run()

		if me.fetch('NODE') == 'master':

			if group != 'masterChannels' or channel == 'channel0':

				pass

		for r in runs:
			if r.group == 'GetAllPresets':
				r.kill()
		
		run("op.CUE_PLAYER.GetAllPresets()", delayFrames = 30, group = 'GetAllPresets')

		
		if group == 'masterChannels' and channel != 'channel0':
			parms = plugin.op('parameters')
			
			posX = parms.nodeX
			posY = parms.nodeY
			parms.destroy()
			plugin.op('sendParms').destroy()

			plugin.create(selectDAT, 'parameters')
			parms = plugin.op('parameters')
			parms.nodeX = posX
			parms.nodeY = posY
			parms.par.dat = '../../../../channel0/effects/'+ slot +'/plugin/parameters'

	def LoadEffect(self, path, dataSlotPath):

		#print(path, dataSlotPath)
		
		if me.fetch('NODE') == 'master' and op.DATABASE.fetch('REMOTE_MODE') != 0:

			self.remote.GetAttr(self.lm, 'LoadEffect', path, dataSlotPath)
		

		slot = dataSlotPath[-1:]

		#if it's a master channel, load effect on each of it's subchannels
		if re.match(me.fetch('MASTER_DATA') + '/channel0/effects/slot' + str(slot), str(dataSlotPath)):
			for i in range(0, op.DATABASE.fetch('NUM_MASTER_CHAN')):				
				dataSlotPath = me.fetch('MASTER_DATA') + '/channel' + str(i) + '/effects/slot' + str(slot)
				self.LoadInsert(path, dataSlotPath)
		
		else:
			self.LoadInsert(path, dataSlotPath)



		#print('Load Effect: ', path, dataSlotPath)

class TdControl(object):

	def __init__(self):
		return
		
	def Save(self, node):

		#print('Save')
		if node == me.fetch('NODE'):
			project.save()

	def Quit(self, node):

		#print('Quit')
		if node == me.fetch('NODE'):
			project.quit(force = True)

	def Realtime(self, active):

		realTime(active)



