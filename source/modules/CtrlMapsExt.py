class CtrlMapsExt(object):
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.MIDI = self.ownerComp.op('MIDI')
		self.OSC = self.ownerComp.op('OSC')
		self.DMX = self.ownerComp.op('DMX')
		self.Live = self.ownerComp.op('Live')

		pass
		
	def Cleanmapdata(self, *args):
	
		deleteMissing = True	
		
		ctrlMaps = self.ownerComp
		allParmMaps = ctrlMaps.op('allParmMaps')
		mapData = mod.copy.deepcopy(allParmMaps.storage)	
			
		gadgets = 0
		actualGadgets = 0
		controls = 0
		actualControls = 0
		
		midiMap = {}
		oscMap = {}
		dmxMap = {}
		liveMap = {}
		
		for allCtrls in mapData.items():
			controls += 1
		
			if ctrlMaps.op(allCtrls[0]):
				actualControls += 1
				##print(allCtrls[0])
			else:
				if deleteMissing:
					allParmMaps.unstore(allCtrls[0])
				#print(allCtrls[0])
			for gadget in allCtrls[1].items():
				gadgets += 1
				
				if ctrlMaps.op(gadget[0]):
					actualGadgets += 1
					##print(gadget[0])
					##print('\t\t', gadget[1])
				else:
				
					if deleteMissing:
						if allCtrls[0] in allParmMaps.storage.keys():
							allParmMaps.fetch(allCtrls[0]).pop(gadget[0])
					#print(gadget[0])
					
				if gadget[1]['mapMIDI'] == 1:	
					midiMap[gadget[0]] = gadget[1]['pathMIDI'][0]
					#print(gadget[0], gadget[1])
				if gadget[1]['mapOSC'] == 1:	
					oscMap[gadget[0]] = gadget[1]['pathOSC'][0]
					#print(gadget[0], gadget[1])
				if gadget[1]['mapDMX'] == 1:	
					dmxMap[gadget[0]] = gadget[1]['pathDMX'][0]
					#print(gadget[0], gadget[1])
				if gadget[1]['mapLive'] == 1:	
					liveMap[gadget[0]] = gadget[1]['pathLive'][0]
					#print(gadget[0], gadget[1])
		
		ctrlMaps.op('MIDI').store('Maps', midiMap)
		ctrlMaps.op('OSC').store('Maps', oscMap)
		ctrlMaps.op('DMX').store('Maps', dmxMap)
		ctrlMaps.op('Live').store('Maps', liveMap)
		
		#print('Control Panels')
		#print(controls)
		#print(actualControls)
		#print('gadgets')
		#print(gadgets)
		#print(actualGadgets)

		self.MapSetOn(op.LM.fetch('CTRL_MAP'))

		'''
		if op.LM.fetch('CTRL_MAP') == 1:
			op.LM.store('CTRL_MAP', 0)
			run("op.LM.store('CTRL_MAP', 1)", delayFrames = 1)
		'''


	def Clearmapdata(self, *args):

		confirm = ui.messageBox('Clear All Controller Maps', 'Are you sure?', buttons = ['Cancel', 'Clear Maps'])

		if confirm == 1:
			self.Cleanmapdata()

			self.MIDI.store('Maps', {})
			self.OSC.store('Maps', {})
			self.DMX.store('Maps', {})
			self.Live.store('Maps', {})

			allParmMaps = self.ownerComp.op('allParmMaps')
			mapData = allParmMaps.storage	

			for allCtrls in mapData.items():
			
				for gadget in allCtrls[1].items():

					gadget[1]['mapMIDI'] = 0
					gadget[1]['pathMIDI'] = []

					gadget[1]['mapOSC'] = 0
					gadget[1]['pathOSC'] = []

					gadget[1]['mapDMX'] = 0
					gadget[1]['pathDMX'] = []

					gadget[1]['mapLive'] = 0
					gadget[1]['pathLive'] = []

					if op(gadget[0]).op('buttonCtrlMapSet/text'):
						op(gadget[0]).op('buttonCtrlMapSet/text').par.text = ''
					
					#print(gadget[0], gadget[1])

			self.Cleanmapdata()

	
	def Savecontrollermapfile(self, *args):

		allParmMaps = self.ownerComp.op('allParmMaps')
		allData = allParmMaps.storage
		mapFileName = ui.chooseFile(load = False, start = '../Controller Maps', 
			fileTypes = ['.cmap'], title = 'Save Controller Map As:')
	
		if mapFileName:
			import pickle
			import os

			#mapFileName = 'controllerMaps/' + mapFileName
			#fileDir = project.folder + '/controllerMaps'
			
			#if not os.path.exists(fileDir):
			#	os.makedirs(fileDir)

			with open(mapFileName, 'wb') as f:

				pickle.dump(allData, f)	

	def Loadcontrollermapfile(self, *args):

		cmapFile = ui.chooseFile(start = '../Controller Maps', 
			fileTypes = ['.cmap'], title = 'Load Controller Map: ')

		if cmapFile:

			allParmMaps = self.ownerComp.op('allParmMaps')
			allData = allParmMaps.storage

			import pickle

			with open(cmapFile, 'rb') as f:

				allData = pickle.load(f)
				
			##print(allData)

			allParmMaps.unstore('*')

			for i in allData.items():

				##print(i[0])
				allParmMaps.store(i[0], i[1])

			self.Cleanmapdata()


	def MapSetOn(self, val):
		
		ctrlMaps = self.ownerComp
		allParmMaps = self.ownerComp.op('allParmMaps')
		mapData = allParmMaps.storage	
		mapCols = [self.ownerComp.fetch('MIDICOL1'), self.ownerComp.fetch('OSCCOL1'), 
				self.ownerComp.fetch('DMXCOL1'), self.ownerComp.fetch('LIVECOL1')]
		
		mapType = self.ownerComp.fetch('CTRL_MAP_TYPE')
		bgColAll = mapCols[mapType]
		ctrls =  self.ownerComp.op('controllers')
		curComp = ctrls[0, mapType].val
		curMap = ctrls[1, mapType].val
		curPath = ctrls[2, mapType].val

		midiDict = self.ownerComp.op('MIDI').fetch('Maps')
		oscDict = self.ownerComp.op('OSC').fetch('Maps')
		dmxDict = self.ownerComp.op('DMX').fetch('Maps')
		liveDict = self.ownerComp.op('Live').fetch('Maps')
				
		for allCtrls in mapData.items():
		
			for gadget in allCtrls[1].items():

				if gadget[0] in midiDict.keys() and val == 1 and gadget[1]['mapMIDI'] == 0:
					gadget[1]['mapMIDI'] = 1
					gadget[1]['pathMIDI'] = [midiDict[gadget[0]]]
					op(gadget[0]).op('buttonCtrlMapSet/text').par.text = midiDict[gadget[0]]
					#print(gadget[0], gadget[1])

				if gadget[0] in oscDict.keys() and val == 1 and gadget[1]['mapOSC'] == 0:
					gadget[1]['mapOSC'] = 1
					gadget[1]['pathOSC'] = [oscDict[gadget[0]]]
					op(gadget[0]).op('buttonCtrlMapSet/text').par.text = oscDict[gadget[0]]
					#print(gadget[0], gadget[1])

				if gadget[0] in dmxDict.keys() and val == 1 and gadget[1]['mapDMX'] == 0:
					gadget[1]['mapDMX'] = 1
					gadget[1]['pathDMX'] = [dmxDict[gadget[0]]]
					op(gadget[0]).op('buttonCtrlMapSet/text').par.text = dmxDict[gadget[0]]
					#print(gadget[0], gadget[1])

				if gadget[0] in liveDict.keys() and val == 1 and gadget[1]['mapLive'] == 0:
					gadget[1]['mapLive'] = 1
					gadget[1]['pathLive'] = [liveDict[gadget[0]]]
					op(gadget[0]).op('buttonCtrlMapSet/text').par.text = liveDict[gadget[0]]
					##print(gadget[0], gadget[1])

					
				mapState = gadget[1][curMap] * 3
				bgCol = bgColAll[mapState]
		
				mapButton = op(gadget[0] + '/buttonCtrlMapSet')
				
				##print (gadget)
				
				if mapButton:
					mapButton.par.display = val
					mapButton.par.bgcolorr = bgCol[0]
					mapButton.par.bgcolorg = bgCol[1]
					mapButton.par.bgcolorb = bgCol[2]
					mapButton.par.bgalpha = bgCol[3]
					
					mapButton.store('RollOffCol', bgCol)
					
					text = op(gadget[0] + '/buttonCtrlMapSet/text')
					
					path = gadget[1][curPath]
					if len(path) > 0:
					
						path = path[0]	
						
						text.par.text = path
					
					else:
						text.par.text = ''

			ctrlMaps.store('CurSel','')
			ctrlMaps.store('PrevSel','')
			ctrlMaps.store('CtrlsPath','')