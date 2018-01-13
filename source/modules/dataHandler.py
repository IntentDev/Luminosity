class SendData(object):

	def __init__(self):


		self.DataOut = op(me.fetch('RELIABLE_UDT'))

		return

	def SendPar(self, comp, par):

		data = par.val	
		args = [comp.path, par.name]		
		extOP = '/Luminosity'	
		className = 'SetData'		
		functionName = 'SetPar' 
			
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		self.DataOut.send(msg, terminator = '')

	def SendParTable(self, dat):

		import tableFunc as tF

		data = {r[0].val:tF.SetToType(r[1].val) for r in dat.rows()[1:]}	
		args = [dat.path]		
		extOP = '/Luminosity'	
		className = 'SetData'		
		functionName = 'SetParTable' 
			
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		self.DataOut.send(msg, terminator = '')

	def SendParTablePar(self, dat, cells, prev):

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetParTablePar' 
			
		prepend = extOP +'::'+ className +'::'+ functionName +'::'
		
		
		
		for c in cells:
			msg = prepend + c.val +'::'+ str([dat.path, c.row, c.col])
			self.DataOut.send(msg, terminator = '')

	def SendDAT(self, dat):

		import tableFunc as tF

		data = dat.text	
		args = [dat.path]		
		extOP = '/Luminosity'	
		className = 'SetData'		
		functionName = 'SetDAT' 
			
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		self.DataOut.send(msg, terminator = '')

	def SendTableRow(self, dat, cells, prev):

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetTableRow' 
			
		prepend = extOP +'::'+ className +'::'+ functionName +'::'
		
		
		
		for c in cells:
			msg = prepend + c.val +'::'+ str([dat.path, c.row, c.col])
			self.DataOut.send(msg, terminator = '')


	def SendStorageKey(self, value, name, path):

		print('SendStorageKey', name, path)

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetStorageKey'
		prepend = extOP +'::'+ className +'::'+ functionName +'::'

		

		msg = prepend + str(value) +'::'+ str([name, path])
		self.DataOut.send(msg, terminator = '')	

	def SendTDControl(self, value, functionName):
			
		extOP = me.fetch('ROOTPATH')
		className = 'TdControl'	
		data = value
		args = ''
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)

		
		self.DataOut.send(msg, terminator = '')

	def SendCue(self, cue):

		data = cue	
		args = []		
		extOP = '/Luminosity'	
		className = 'SetData'		
		functionName = 'SetCue' 
			
		msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
		
		
		self.DataOut.send(msg, terminator = '')

	def SendRecallPreset(self, preset, path):
		#print(preset, path)

		if path != '/Luminosity/database/cuePlayer/cueList/plugin/presets':

			data = preset
			args = [path]		
			extOP = '/Luminosity'	
			className = 'SetData'		
			functionName = 'SetRecallPreset' 
				
			msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)
			
			
			self.DataOut.send(msg, terminator = '')


class SetData(object):

	def __init__(self):
		return
		
	def Smpl(self, data, *args):
	
		#print(args)
		#print(data)
		pass

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
		print(data, path)
		presets = op(path)
		#presets.Preset = data
		presets.RecallPreset(data)
		#print('SetRecallPreset')

	def SetCue(self, cue):
		op(me.fetch('CUE_PLAYER')).op('recallCue/list/list/cellId')[0,0] = cue

	def RemoteLoadClip(self, *args):
		data = args[0]
		op.LOAD_CLIPS.RemoteLoadClip(data)


class Load(object):

	def __init__(self):
		return

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
			extOP = me.fetch('ROOTPATH')
			className = 'Load'	
			functionName = 'LoadEffect' 
			data = path
			args = [dataSlotPath]
			msg = extOP +'::'+ className +'::'+ functionName +'::'+ str(data) +'::'+ str(args)

			dataOut = op(me.fetch('RELIABLE_UDT'))
			dataOut.send(msg, terminator = '')
		

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



