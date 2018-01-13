import copy
import os

class DatabaseExt(object):

	def __init__(self, ownerComp):
	
		self.ownerComp = ownerComp
		self.ServerSettings = op.SERVER_SETUP.op('serverSettings')
	
	def SaveSession(self):

		path = op.LM.fetch('CURRENT_SESSION_PATH', '')

		if path != None or path != '':

			op.LM.store('SAVE_LOAD_STATE', 1)

			self.SaveSetupState()
			self.SaveChannelUIState()

			op.LM.Delay(delayFrames = 5).Call(op.DATABASE, 'save', path)
			run("op.LM.store('SAVE_LOAD_STATE', 0)", delayFrames = 10)


	def SaveSessionAs(self):
		
		path = ui.chooseFile(load = False, start = '../Session Files', fileTypes = ['.tox'], title = 'Save Session File As:')
	
		if path:

			path = mod.fileFunc.GetRelPath(path)

			op.LM.store('CURRENT_SESSION_PATH', path)
			name = path.split('/')[-1:][0].replace('.tox', '')
			op.LM.store('CURRENT_SESSION', name)
			op.LM.store('SAVE_LOAD_STATE', 1)

			self.SaveSetupState()
			self.SaveChannelUIState()

			op.LM.Delay(delayFrames = 5).Call(op.DATABASE, 'save', path)
			run("op.LM.store('SAVE_LOAD_STATE', 0)", delayFrames = 10)

		'''
		else:
			path = op.LM.fetch('CURRENT_SESSION_PATH')
			name = path.split('/')[-1:][0].replace('.tox', '')
			op.LM.store('CURRENT_SESSION', name)
			op.LM.store('SAVE_LOAD_STATE', 0)
		'''

	def LoadSession(self):

		print('Load Session')

		path = ui.chooseFile(start = '../Session Files', fileTypes = ['.tox'], title = 'Load Session File:')

		if path:
			realTime(0)

			path = mod.fileFunc.GetRelPath(path)
			op.LM.store('CURRENT_SESSION_PATH', path)
			name = path.split('/')[-1:][0].replace('.tox', '')
			op.LM.store('CURRENT_SESSION', name)
			op.LM.store('SAVE_LOAD_STATE', 2)


			#op.DATABASE.destroy()
			#op.LM.loadTox(path)
			#op.DATABASE.nodeX = 0
			#op.DATABASE.nodeY = 200
			op.DATABASE.par.externaltox = path
			op.DATABASE.par.reinitnet.pulse()


			op.SERVER_SETUP.store('SetSettings', 0)
			#op.SERVER_SETUP.allowCooking = True
			
			op.LM.Delay(delayFrames = 15).Call(op.DATABASE, 'LoadChannelUIState')
			op.LM.Delay(delayFrames = 15).Call(op.DATABASE, 'LoadSetupState')

		'''
		else:

			path = op.LM.fetch('CURRENT_SESSION_PATH')
			name = path.split('/')[-1:][0].replace('.tox', '')
			op.LM.store('CURRENT_SESSION', name)
			op.LM.store('SAVE_LOAD_STATE', 0)
			realTime(1)
		'''

	def LoadDefaultSession(self):

		print('Load Session')

		path = '../assets/defaults/DefaultSession.tox'

		if mod.os.path.exists(path):
			realTime(0)
			op.LM.store('CURRENT_SESSION_PATH', path)
			name = path.split('/')[-1:][0].replace('.tox', '')
			op.LM.store('CURRENT_SESSION', name)
			op.LM.store('SAVE_LOAD_STATE', 2)


			op.DATABASE.destroy()
			op.LM.loadTox(path)
			op.DATABASE.nodeX = 0
			op.DATABASE.nodeY = 200
		
			op.SERVER_SETUP.store('SetSettings', 0)
			#op.SERVER_SETUP.allowCooking = True
			op.LM.Delay(delayFrames = 10).Call(op.DATABASE, 'LoadSetupState')
			op.LM.Delay(delayFrames = 15).Call(op.DATABASE, 'LoadChannelUIState')
			


	def GetControls(self, controls):

		storeComp = controls.fetch('StoreComp')
		compPar = copy.deepcopy(storeComp.fetch('CompPar'))

		return compPar

	def SetControls(self, controls, compPar):

		storeComp = controls.fetch('StoreComp')
		parDest = op(controls.fetch('Parameters'))

		storeComp.store('CompPar', compPar)

		values = compPar['values']

		for gadget in values.items():
			if controls.op(gadget[0]):
				controls.op(gadget[0]).op('setUI').run(gadget[1])
				
				for par in gadget[1].items():
					if isinstance(par[1], int) or isinstance(par[1], float) or isinstance(par[1], str):
						parDest[gadget[0], par[0]] = par[1]
						#print(controls.op(gadget[0]), par[1])
			
	def SetCurServerSettings(self):

		curServerSettings = op.SERVER_DATA.op('server0').fetch('Settings')

		self.ServerSettings.op('serverSetup/numGPUs/setValue').run(curServerSettings['numGPUs'])
		self.ServerSettings.op('serverSetup/address/setValue').run(curServerSettings['address'])
		self.ServerSettings.op('serverSetup/active/setValue').run([curServerSettings['active']])
		self.ServerSettings.op('serverSetup/firstDisplay/setValue').run(curServerSettings['firstDisplay'])
		self.ServerSettings.op('serverSetup/layoutMode/setValue').run([curServerSettings['layoutMode']])

		curSettings = op.SERVER_DATA.fetch('CurrentSettings')

		self.ServerSettings.op('selServer/server/setValue').run([curSettings['curServer']])
		self.ServerSettings.op('selectSettings/selGPU/setValue').run([curSettings['curGPU']])
		self.ServerSettings.op('selectSettings/selOutput/setValue').run([curSettings['curOutput']])

	def SetChanResSettings(self):
		chanRes = op.DATABASE.fetch('CHAN_RES')

		for key, val in chanRes.items():
			op.PROJECT_SETUP.op('plugin/setChanRes').op(key).SetState(val['resMode'], val['resX'], val['resY'], val['audioActive'])


	def SaveSetupState(self):

		projSettings = self.GetControls(op.PROJECT_SETUP.op('controls'))
		sData = self.GetControls(op.SERVER_SETUP.op('serverData/controls'))
		sGPU0 = self.GetControls(self.ServerSettings.op('gpu0/controls'))
		sGPU1 = self.GetControls(self.ServerSettings.op('gpu1/controls'))
		sGPU2 = self.GetControls(self.ServerSettings.op('gpu2/controls'))
		sGPU3 = self.GetControls(self.ServerSettings.op('gpu3/controls'))
		sOutput = self.GetControls(op.SERVER_SETUP.op('outputSettings/outputSetup/controls'))


		setupState = {'projectSettings': projSettings, 'ServerData': sData, 'GPU0': sGPU0, 'GPU1': sGPU1,
					'GPU2': sGPU2, 'GPU3': sGPU3, 'Output': sOutput}


		op.DATABASE.store('SetupState', setupState)


		pass


	def LoadSetupState(self):

		op.SERVER_SETUP.store('SetSettings', 0)
		#op.SERVER_SETUP.allowCooking = True
		if op.LM.fetch('PREVIS_ACTIVE') == 1:
			op.DATABASE.op('preVis').allowCooking = True

		setupState = copy.deepcopy(op.DATABASE.fetch('SetupState'))

		self.SetCurServerSettings()
		self.SetChanResSettings()
		self.SetControls(op.PROJECT_SETUP.op('controls'), setupState['projectSettings'])
		self.SetControls(op.SERVER_SETUP.op('serverData/controls'), setupState['ServerData'])
		self.SetControls(self.ServerSettings.op('gpu0/controls'), setupState['GPU0'])
		self.SetControls(self.ServerSettings.op('gpu1/controls'), setupState['GPU1'])
		self.SetControls(self.ServerSettings.op('gpu2/controls'), setupState['GPU2'])
		self.SetControls(self.ServerSettings.op('gpu3/controls'), setupState['GPU3'])
		self.SetControls(op.SERVER_SETUP.op('outputSettings/outputSetup/controls'), setupState['Output'])

		mod.serverFuncs.ServerCtrl().RecallEdgeBlend()

		bankUI = op.CLIP_LANES_UI.op('bankSelectContainer/bankSelect/cellId')
		if bankUI[0, 0] != '0':
			bankUI[0, 0] = 0
			op.CLIP_LANES_UI.op('setBank').run(0)
		else:
			op.LM.store('CUR_BANK', 'bank0')
			op.CLIP_DATA.op('preload').run('bank0')


		op.LM.store('SAVE_LOAD_STATE', 0)
		op.LM.Delay(delayFrames = 15, fromOP = op.DATABASE).Call(self.ownerComp, 'LoadSetupStateOff')

	def LoadSetupStateOff(self):

		op.SERVER_SETUP.store('SetSettings', 1)
		if op.LM.fetch('SERVER_SETUP_ACTIVE') == 0:
			#op.SERVER_SETUP.allowCooking = False
			realTime(1)
		if op.LM.fetch('PREVIS_ACTIVE') == 0:
			op.DATABASE.op('preVis').allowCooking = False


	def GetChanSources(self, sources):
		items = op(sources.fetch('ItemList'))
		numCols = items.numCols
		itemsList = []
		for r in items.rows():
			row = []	
			for c in range(0, numCols):
				row.append(r[c].val)
			itemsList.append(row)

	def SetChanSources(self, sources, sourceItems):
		itemTable = op(sources.fetch('ItemList'))	
		i = 0	
		if sourceItems:
			for r in sourceItems:	
				n = 0			
				for c in r:			
					itemTable[i,n] = c
					n += 1
				i += 1

	def SetStorage(self, storeComp, storage):
		for key, val in storage.items():
			storeComp.store(key, val)

	def SaveChannelUIState(self):

		id = 'SaveState'

		clipCtrls = []
		clipStorage = []
		auxCtrls = []
		auxStorage = []
		auxSources = []


		for r in op.CHAN_CLIP_UI.op('channels').rows()[1:]:
			channel = op.CHAN_CLIP_UI.op(r[0].val)
			clipCtrls.append(self.GetControls(channel))
			clipStorage.append(copy.deepcopy(channel.storage))
		
		for r in op.CHAN_AUX_UI.op('channels').rows()[1:]:	
			channel = op.CHAN_AUX_UI.op(r[0].val)	
			auxCtrls.append(self.GetControls(channel))
			auxStorage.append(copy.deepcopy(channel.storage))
			auxSources.append(self.GetChanSources(channel.op('sources0')))

		channel = op.CHAN_MASTER_UI.op('channel0')
		masterCtrls = self.GetControls(channel)
		masterStorage = copy.deepcopy(channel.storage)
		masterSources = self.GetChanSources(channel.op('sources0'))

		saveState = {'ClipCtrls': clipCtrls, 'ClipStorage': clipStorage, 'AuxCtrls': auxCtrls, 
					'AuxStorage': auxStorage, 'AuxSourcesUI': auxSources, 'MasterCtrls': masterCtrls, 
					'MasterStorage': masterStorage, 'MasterSourcesUI': masterSources}

		op.CHAN_DATA.store('SaveState', saveState)
		

	def LoadChannelUIState(self):

		saveState = op.CHAN_DATA.fetch('SaveState')


		for r in op.CHAN_CLIP_UI.op('channels').rows()[1:]:
			channel = op.CHAN_CLIP_UI.op(r[0].val)
			index = r[0].row - 1		
			self.SetControls(channel, saveState['ClipCtrls'][index])
			self.SetStorage(channel, saveState['ClipStorage'][index])
			try:	
				op.CLIP_CHAN_VID.op(r[0].val).op('channelFX').RouteFXInit()
			except:
				print(op.CLIP_CHAN_VID.op(r[0].val))


		for r in op.CHAN_AUX_UI.op('channels').rows()[1:]:	
			channel = op.CHAN_AUX_UI.op(r[0].val)	
			index = r[0].row - 1	
			self.SetControls(channel, saveState['AuxCtrls'][index])
			self.SetStorage(channel, saveState['AuxStorage'][index])
			self.SetChanSources(channel.op('sources0'), saveState['AuxSourcesUI'][index])
			op.AUX_CHAN_VID.op(r[0].val).op('channelFX').RouteFXInit()

		channel = op.CHAN_MASTER_UI.op('channel0')
		self.SetControls(channel, saveState['MasterCtrls'])
		self.SetStorage(channel, saveState['MasterStorage'])
		self.SetChanSources(channel.op('sources0'), saveState['MasterSourcesUI'])
		for r in op.MASTER_CHAN_VID.op('channels').rows()[1:]:	
			op.MASTER_CHAN_VID.op(r[0].val).op('channelFX').RouteFXInit()
	
	def Copystorage(self, copyFrom, copyTo):
	
		confirm = ui.messageBox('Copy Storage', 'Are you sure?', buttons = ['Yes', 'No'])
		print(confirm)
		if confirm == 0:

			storageKeys = [r[0].val for r in op('../storageKeys').rows()]
			fromCOMP = op('../Luminosity')
			toCOMP = op('../Luminosity/database')

			for name in storageKeys:
				val = fromCOMP.fetch(name)
				toCOMP.store(name, val)

			#mod.pprint.pprint(storageKeys)


	"""Called when a session is loaded	"""	
	def VerifyAssets(self, PluginTag = "uiGadget-fileLoader", location="Plugins"):
		
		print("Verifying Assets")
		
		#search the plugin directory to find the fileLoader Plugin.
		PluginsUsingfileLoader = op.PLUGINS.findChildren(tags=[PluginTag], maxDepth = 4)
		failedToLoad = []
		
		for Plugin in PluginsUsingfileLoader: 
			pluginParentTag = Plugin.parent(2).name + "Plugin"
			parName = Plugin.name
			PluginsUsingPlugin = op.CLIP_DATA.findChildren(tags=[pluginParentTag], maxDepth = 4)
			
			#now search through the Plugins and find plugins that utilise the plugin
			for Plugin in PluginsUsingPlugin:
				oldAssetPath = Plugin.op("parameters")[parName, "value"].val
				
				#if the param isn't blank
				if len(oldAssetPath) > 3:
					if not os.path.exists(oldAssetPath):
						failedToLoad.append({ 'Plugin':Plugin, 'parName':parName, 'oldAssetPath':oldAssetPath})
						
		if len(failedToLoad) > 0:
			op.LM.Delay(delayFrames = 2, fromOP = self.ownerComp).Call(self.ownerComp, 'HuntAssets', failedToLoad)
	
	"""Called When VerifyAssets finds missing assets"""
	def	HuntAssets(self, failedToLoad):

		numberFailed = len(failedToLoad)
		#we use a while loop as we might progressively replace a bunch of file names using a found directory root.
		while numberFailed > 0:
				
				failed = failedToLoad[numberFailed-1]
				Plugin = failed["Plugin"]
				parName = failed["parName"]
				oldAssetPath = failed["oldAssetPath"]
				msg = "The Asset " + oldAssetPath + " in " + Plugin.parent(2).name + " : " + Plugin.parent().name + " : parameter:" + parName + " is missing."
				alert = ui.messageBox('Warning:', msg, buttons=['Update Location', 'Retry', 'Ignore', 'Ignore All',  ])
				
				if alert == 2: #ignore this one only
					numberFailed -= 1
				
				elif alert == 3: #ignore all
					numberFailed = 0
					return
				
				elif alert == 1: #retry	
					op.LM.Delay(delayFrames = 60, fromOP = self.ownerComp).Call(self.ownerComp, 'VerifyAssets')
					numberFailed = 0
					return
				
				elif alert == 0: #replace
					
					newAssetPath = ui.chooseFile(start = '../Session Files', fileTypes = ['*'], title = 'Replacement for' + oldAssetPath)
					if len(newAssetPath) > 3:
						newRootPath, oldRootPath = self.GetNewDirectoryRoot(newAssetPath, oldAssetPath)
					
						if len(newRootPath) > 0:
							alert = ui.messageBox('New Root Directory Found at:' + newRootPath, 'Would you like to automatically other missing assets found inside ' + newRootPath + ' ?', buttons=['Replace all found', 'This file only'])
						
							if alert == 0: #Ok - test other missing files to see if they exist and update them
								
								for failed in failedToLoad[:]:
									
									oldAssetPath = failed["oldAssetPath"]
									newAssetPath = oldAssetPath.replace(oldRootPath, newRootPath)
									
									if os.path.exists(newAssetPath): #ok found another one great
										print("updating " + newAssetPath)
										Plugin = failed["Plugin"]
										parName = failed["parName"]
										parametersTable = Plugin.op("parameters")
										parametersTable[parName,"value"] = newAssetPath
										numberFailed -= 1
										failedToLoad.remove(failed)
										
							
							elif alert == 1: #Just replace one
									
								parametersTable = Plugin.op("parameters")
								parametersTable[parName,"value"] = newAssetPath
								numberFailed -= 1
								failedToLoad.remove(failed)
								
	
					
	""" Compares newAssetPath with oldAssetPath to get a new root path """
	def GetNewDirectoryRoot(self, newAssetPath, oldAssetPath): #D:/somepath/somefile.avi, E:/somepath/somefile.avi
		
		#probably better to start from the end of the directories and work our way backwards until we find a difference
		newdirs = newAssetPath.split("/")
		olddirs = oldAssetPath.split("/")
		sharedPath = ''
		if olddirs[-1] == newdirs[-1]: #mymovie.avi
			sharedPath = newdirs[-1]
			
			for i in range(2,len(olddirs)):
				
				if olddirs[-i] == newdirs[-i]:
					sharedPath = newdirs[-i] + "/" + sharedPath
				
				else:
					break
				
		return newAssetPath.replace(sharedPath,''), oldAssetPath.replace(sharedPath,'') #E:somefolder #D:somefolder
		
					