''' Note!!! custom parameter menus and bank field do not update when using the control panel

- preset store dictionary of:

	- a list containing animation data (if HasAnimation):
		- channels
		- keys
		- pars

	- a list of lmParameters:
		- compPar
		- parameters.text
		
'''


import copy
from pprint import pprint
import sys


class PresetsExt(object):

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		print('Intializing ext:', self.ownerComp)

		self.callbacks = self.ownerComp.op('callbacks').module
		self.ParNames = [r[0].val for r in self.ParsOP.rows()[1:]]
		self.ParAttr = [c[0].val for c in self.ParsOP.cols()[1:]]
		self.NumPars = len(self.ParNames)
		self.PresetList = self.PresetControls.op('presetList')
		self.BankList = self.PresetControls.op('bankList')
		self.PresetRadio = self.Controls.op('presets/presetRadio')
		self.filter = self.ownerComp.op('filter')
		self.Preset = None	
		self.PresetIndex = None
		self.LM = op.LM
		self.DB = op.DATABASE
		self.Node = me.fetch('NODE')
		self.ControlOut = op.CONTROL_OUT

		self.DefaultBankName = self.ownerComp.fetch('DefaultBankName', 'Preset Bank 1')
		self.DefaultPresetName = self.ownerComp.fetch('DefaultPresetName', 'Default Preset')

		if len(self.ownerComp.par.Selectbank.menuLabels) > 0:
			self.BankName = self.ownerComp.par.Selectbank.menuLabels[int(self.ownerComp.par.Selectbank)]	
		else:
			self.BankName = self.DefaultBankName

		self.HasAnimation = self.Plugin.HasAnimation

		if self.HasAnimation:		
			self.AnimActive = self.Plugin.AnimActive
			self.Animation = self.ownerComp.par.Animationcomp.eval()
			self.SwitchCrossAnim = self.Animation.op('switchCross')
		else:
			self.AnimActive = False

		self.CompPresets = self.Plugin.fetch('CompPresets', {})

		if self.BankName in self.CompPresets.keys():

			self.Presets = self.CompPresets[self.BankName]
			self.StoreComp.store('CompPresets', self.CompPresets)
			self.StoreComp.store('CurPresets', self.Presets)

			if 'PresetPars' in self.StoreComp.storage.keys():
				self.PresetPars = self.StoreComp.fetch('PresetPars')
			else:
				self.PresetPars = [[parName, True, True] for parName in self.ParNames]
				self.StoreComp.store('PresetPars', self.PresetPars)
			

			if len(self.Presets) == 0: 

				self.InitializeBank()
			else:
				#print('Init PresetExt')
				self.GetBankNames(updateControls = False)	
				try:
					self.GetPresetNames()
				except:
					pass
				
			
		elif len(self.CompPresets.keys()) > 0:
			self.SetBank(self.ownerComp.par.Selectbank.menuLabels[int(self.ownerComp.par.Selectbank)])
			self.ownerComp.par.Selectbank = 0

		else:
			self.Initialize()

		self.SetRecallMode()
		self.SetMorph()

		self.ownerComp.op('filter').cook(force = True)

		for r in runs:
			if r.group == 'GetAllPresets':
				r.kill()
		
		#attr = self.StoreComp.fetch('CompAttr')['attr']
		#pluginType = attr['type']

		#if pluginType not in ['synth', 'audio', 'movie']:

		if not hasattr(self.Plugin, 'IsClip'):

			run("op.CUE_PLAYER.GetAllPresets()", delayFrames = 30, group = 'GetAllPresets') 

		self.LastRecalled = {'bankName': copy.copy(self.BankName), 'presetIndex': copy.copy(self.PresetIndex)}

	def InitializeBank(self):

		self.HasAnimation = self.Plugin.HasAnimation
		if self.HasAnimation:
			self.Animation.ClearAll()

		self.CompPresets = self.Plugin.fetch('CompPresets')
		self.Presets = []

		self.GetBankNames()
		self.StorePreset(self.DefaultPresetName)

		self.ownerComp.par.N = 1
		self.SetMenus()
		self.GetPresetNames()
		self.DeletePreset(0)
		self.SetMenus()

	def Initialize(self):

		self.HasAnimation = self.Plugin.HasAnimation
		if self.HasAnimation:
			self.Animation.ClearAll()

		self.BankName = self.DefaultBankName
		self.StoreComp.store('CompPresets', {self.BankName: []})
		self.CompPresets = self.Plugin.fetch('CompPresets')
		self.Presets = self.CompPresets[self.BankName]

		#self.PresetControls = self.Plugin.fetch('CompAttr')['attr']['presetControls']

		#self.StorePreset(self.DefaultPresetName)
		self.ownerComp.par.N = 1
		self.SetMenus()
		self.GetPresetNames()

		self.PresetPars = [[parName, True, True] for parName in self.ParNames]
		self.StoreComp.store('PresetPars', self.PresetPars)

	def InitPresets(self):
		self.StoreComp.unstore('*Preset*')
		self.Initialize()
		self.ownerComp.initializeExtensions()
			
	def StorePreset(self, presetName):
		
		preset = self.GetPreset(presetName)
		self.Presets.append(preset)
		self.Preset = self.Presets[-1:][0]
		self.PresetIndex = len(self.Presets) - 1

		self.LastRecalled = {'bankName': copy.copy(self.BankName), 'presetIndex': copy.copy(self.PresetIndex)}

		self.SavePresets()
		self.GetPresetNames()

		return preset

	def GetPreset(self, presetName):

		compPar = copy.deepcopy(self.Plugin.fetch('CompPar'))
		preset = {}
		preset['name'] = presetName
		#preset['lmParameters'] = [compPar, self.ParsOP.text, len(compPar['values'].keys())]
		preset['lmParameters'] = [compPar, self.ParsOP.text]

		if self.HasAnimation:
			preset['animation'] = self.Animation.PresetGetAnim()

		preset['customData'] = self.callbacks.onStore(preset, len(self.Presets))

		return preset

	def SavePresets(self):
		self.CompPresets[self.BankName] = self.Presets
		self.StoreComp.store('CompPresets', self.CompPresets)
		self.StoreComp.store('CurPresets', self.Presets)
		self.SendPresets()
	
	def RecallPreset(self, presetIndex, delayFrame = 0):
		if presetIndex < len(self.Presets):
			self.Preset = self.StoreComp.fetch('CurPresets')[presetIndex]
			self.PresetIndex = presetIndex
			self.Recall(delayFrame)
		
	def Recall(self, delayFrame = 0, playAnim = True, remote = True):

		self.callbacks.onRecall(self.Preset, self.PresetIndex)
		self.LastRecalled = {'bankName': copy.copy(self.BankName), 'presetIndex': copy.copy(self.PresetIndex)}

		group = str(self.ownerComp.id)

		for r in runs:
			if r.group == group: r.kill()
	
		enableBlend = self.ownerComp.par.Presetblend.menuIndex
		
		if enableBlend == 1:
			#print(enableBlend)
			
			self.filter.par.timeslice = 1
			self.filter.cook(force = True)

			op.LM.Delay(delayMilliSeconds = self.ownerComp.par.Blendtime.eval() * 1000, 
						group = group, fromOP = self.ownerComp).Call(self.ownerComp, 'BlendEnd')

		if self.AnimActive:
			self.Animation.PresetSetAnim(self.Preset['animation'], playAnim = playAnim, enableBlend = enableBlend)

		
		compPar = copy.deepcopy(self.Preset['lmParameters'][0])
		self.StoreComp.store('CompPar', compPar)
		self.StoreComp.CompPar = compPar

		if self.RecallMode:

			self.ParsOP.text = self.Preset['lmParameters'][1]

		ctrlsDisplayed = self.Controls.fetch('IsDisplayed', 1)
		
		#print(self.PresetPars)

		if ctrlsDisplayed == 1 or not self.RecallMode:

			i = 1 + delayFrame
			n = 0

			for parName in self.ParNames:

				val = self.Preset['lmParameters'][0]['values'][parName]

				if not self.RecallMode:

					for key, value in val.items():

						if self.PresetPars[n][1]:
							
							# needed for EffectSlots should come up with better method
							if key in self.ParAttr:

								self.ParsOP[parName, key] = value

	
				if ctrlsDisplayed == 1 and self.Node == 'master':

					d = op.LM.Delay(delayFrames = i, fromOP = self.ownerComp)
					#print(n)
					if self.PresetPars[n][1]:

						#self.Controls.op(parName).SetUI(self.Controls, val)
						d.Call(self.Controls.op(parName).ext.Gadget, 'SetUI', self.Controls, val)

				i += 1
				n += 1
				
		if (self.Node == 'master' and self.DB.fetch('REMOTE_MODE') != 0 and self.PresetIndex != None
			and self.ownerComp.path != '/Luminosity/database/cuePlayer/cueList/plugin/presets'
			and remote):
			print(self.ownerComp)
			op.LM.SendData().SendRecallPreset(self.PresetIndex, self.ownerComp.path)



		return

	def UpdatePreset(self, presetIndex):

		parmOP = op('../parameters')
		compPar = copy.deepcopy(self.StoreComp.fetch('CompPar'))

		preset = {}
		preset['name'] = self.Presets[presetIndex]['name']
		if self.HasAnimation:
			preset['animation'] = self.Animation.PresetGetAnim()
		#preset['lmParameters'] = [compPar, self.ParsOP.text, len(compPar['values'].keys())]
		preset['lmParameters'] = [compPar, self.ParsOP.text]
	
		preset['customData'] = self.callbacks.onUpdate(preset, presetIndex)

		self.Presets[presetIndex] = preset
		self.Preset = self.Presets[presetIndex]
		self.PresetIndex = presetIndex
		#mod.pprint.pprint(self.Preset)
		#print(self.Presets)
		self.SavePresets()

		return preset

	def DuplicatePreset(self, presetIndex):
		newPreset = copy.deepcopy(self.Presets[presetIndex])
		newPreset['name'] = newPreset['name'] + '_Copy'
		self.Presets.append(newPreset)
		self.SavePresets()
		self.GetPresetNames()

	def RenamePreset(self, presetIndex, name):

		self.Preset = self.StoreComp.fetch('CurPresets')[presetIndex]
		self.PresetIndex = presetIndex
		self.Preset['name'] = name
		self.SavePresets()
		self.GetPresetNames()

	def DeletePreset(self, presetIndex):	
		preset = self.Presets.pop(presetIndex)
		self.SavePresets()
		self.GetPresetNames()

		self.callbacks.onDelete(preset, presetIndex)
		if self.PresetList:	
			currentItem = self.PresetList.fetch('CurrentItem')

			if currentItem > presetIndex:

				op.LM.Delay(delayFrames = 1, fromOP = self.ownerComp).Call(self.PresetList, 'SelectCell', currentItem - 1, 1)

	def MovePreset(self, presetIndex, insertIndex, append = False):
	
		preset = self.Presets.pop(presetIndex)

		if not append:

			if insertIndex >= presetIndex:
				insertIndex -= 1

			self.Presets.insert(insertIndex, preset)

		else:

			self.Presets.append(preset)

		self.SavePresets()
		self.GetPresetNames()

		self.callbacks.onMove(self.Presets[insertIndex], presetIndex, insertIndex)

	def CopyPreset(self, presetIndex):

		self.CopiedPreset = copy.deepcopy(self.Presets[presetIndex])

	def PastePreset(self, presetIndex):

		if hasattr(self, 'CopiedPreset'):

			if presetIndex == -1:
				self.Presets.append(self.CopiedPreset)

			else:

				self.Presets[presetIndex] = self.CopiedPreset

			self.GetPresetNames()
			#self.PresetList.par.reset.pulse()
			self.SendPresets()

	def AppendCopiedPreset(self, presetIndex):

		if hasattr(self, 'CopiedPreset'):

			self.Presets.append(self.CopiedPreset)
			self.GetPresetNames()
			self.SendPresets()
			#self.PresetList.par.reset.pulse()

	def CreateBank(self, bankName, updatePar = False):

		if bankName != '':
		
			if bankName not in self.CompPresets.keys():
				self.BankName = bankName
				self.InitializeBank()
				self.SendPresets()
			else:
				ui.messageBox('Bank Exists', 'This bank name is already being used. Please select another name', buttons =['Close'])
		
		else:
			ui.messageBox('Set Bank Name', 'You must enter a name to create a Bank', buttons = ['Close'])

	def SetBank(self, bankName, updatePar = False):
		#print('SetBank')

		self.BankName = bankName

		if self.BankName not in self.CompPresets.keys():
			self.InitializeBank()

		else:
			self.Presets = self.CompPresets[bankName]
			self.StoreComp.store('CurPresets', self.Presets)	
			self.Presets = self.StoreComp.fetch('CurPresets')

			#if len(self.Presets) > 0:
			#	self.Preset = self.Presets[0]
			#	self.PresetIndex = 0

			self.ownerComp.par.Selectbank = self.BankNames.index(self.BankName)
		
		self.GetBankNames(updateControls = False)	
		self.GetPresetNames()

		self.callbacks.onSetBank(self.BankName)
		self.SendPresets()
			
	def DeleteBank(self, bankName):

		self.CompPresets.pop(bankName)
		self.StoreComp.store('CompPresets', self.CompPresets)
		self.BankNames.pop(self.BankNames.index(bankName))

		if len(self.BankNames) > 0:
			bankName = self.BankNames[0]
			self.SetBank(bankName)
			self.SetMenus()
			self.SendPresets()
		else:
			self.Initialize()	

	def RenameBank(self, bankName, newBankName):

		self.CompPresets[newBankName] = self.CompPresets[bankName]
		self.CompPresets.pop(bankName)

		self.StoreComp.store('CompPresets', self.CompPresets)
		self.CompPresets = self.StoreComp.fetch('CompPresets')
		

		if bankName == self.BankName:
			self.GetBankNames()
			self.SetBank(newBankName)

		self.SetMenus()
		self.SendPresets()

	def DuplicateBank(self, bankName):
		newBankName = bankName + ' Copy'
		self.CompPresets[newBankName] = self.CompPresets[bankName]

		self.StoreComp.store('CompPresets', self.CompPresets)
		self.CompPresets = self.StoreComp.fetch('CompPresets')

		self.SetMenus()	
		self.SendPresets()

	def GetPresetNames(self):

		#print('GetPresetNames')

		self.PresetNames = [preset['name'] for preset in self.Presets]
		self.UpdateControls()

	def AlphaNumSort(self, l):
		convert = lambda text: float(text) if text.isdigit() else text
		alphanum = lambda key: [ convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key) ]
		l.sort( key=alphanum )
		return l

	def Sorted_nicely(self, l ): 
		""" Sort the given iterable in the way that humans expect.""" 
		convert = lambda text: int(text) if text.isdigit() else text 
		alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
		return sorted(l, key = alphanum_key)	

	def GetBankNames(self, updateControls = True):

		bankNames = [key for key in self.CompPresets.keys()]
		#bankNames = self.AlphaNumSort(bankNames)

		#sorted(bankNames, key=lambda item: (int(item.partition(' ')[0]) if item[0].isdigit() else float('inf'), item))

		self.BankNames = self.Sorted_nicely(bankNames)
		#self.BankNames = [key for key in self.CompPresets.keys()]
		#self.BankNames.sort()

		if updateControls:
			self.UpdateControls()

	def SetMenus(self):
		
		#print('SetMenus')

		self.GetPresetNames()
		self.GetBankNames()
		self.ownerComp.par.Recallpreset.menuNames = self.PresetNames
		self.ownerComp.par.Recallpreset.menuLabels = self.PresetNames
		self.ownerComp.par.Movepreset.menuNames = ['None'] + self.PresetNames
		self.ownerComp.par.Movepreset.menuLabels = ['None'] + self.PresetNames
		self.ownerComp.par.Movebefore.menuNames = ['None'] + self.PresetNames
		self.ownerComp.par.Movebefore.menuLabels = ['None'] + self.PresetNames

		self.ownerComp.par.Movepreset = 'None'
		self.ownerComp.par.Movebefore = 'None'

		self.ownerComp.par.Selectbank.menuNames = self.BankNames
		self.ownerComp.par.Selectbank.menuLabels = self.BankNames
		self.ownerComp.par.Selectbank = self.BankNames.index(self.BankName)

		self.UpdateControls()

	def UpdateControls(self, force = False):

		if self.PresetControls and hasattr(self.PresetControls, 'Presets'):

			if self.PresetControls.Presets == self.ownerComp: 

				if self.PresetControls.IsDisplayed or force:

					self.BankList.par.rows = len(self.BankNames)
					
					if self.BankName in self.BankNames:
						self.PresetControls.BankListSelect(self.BankNames.index(self.BankName))		
					self.BankList.par.reset.pulse()	

					self.PresetList.par.rows = len(self.Presets)
					self.PresetList.par.reset.pulse()


					if self.PresetIndex != None and self.BankName == self.LastRecalled['bankName']:

						#print(self.PresetIndex, self.LastRecalled)
						run("args[0].PresetListSelect(args[1])", self.PresetControls, 
																	self.LastRecalled['presetIndex'], 
																	delayFrames = 1, fromOP = self.ownerComp)

					else:
						run("args[0].PresetListSelect(args[1])", self.PresetControls, -1, 
																	delayFrames = 1, fromOP = self.ownerComp)
					

					self.PresetRadio.par.reset.pulse()
					self.PresetControls.op('blendTime').SetValue(self.ownerComp.par.Blendtime.eval())

					if self.PresetControls.EditPars:
						self.EnabledParsList.par.rows = len(self.ParNames) + 1
						self.EnabledParsList.par.reset.pulse()

	def SetRecallMode(self):

		self.RecallMode = True
		for par in self.PresetPars:

			if not par[1]:
				self.RecallMode = False
				break

		#print(self.RecallMode)

	def SetMorph(self):

		fChans = self.ownerComp.op('filterChans')
		fChans.clear()
		for par in self.PresetPars:
			
			# enable for morphing of pars but not enable preset
			#if par[2]:

			if par[1] and par[2]:
				fChans.appendChan(par[0])

		if fChans.numChans == 0:
			fChans.appendChan('nullChan')

		if self.Node == 'master' and self.DB.fetch('REMOTE_MODE') != 0:
			#print('SetMorph')

			self.LM.SendData().SendPar(self.ownerComp, self.ownerComp.par.Blendtime)
		
	def BlendEnd(self):
	
		self.filter.par.timeslice = 0

		if self.AnimActive:
			self.Animation.PresetBlendEnd()

	def SendPresetsOld(self):

		extOP = me.fetch('ROOTPATH')	
		className = 'SetData'		
		functionName = 'SetPresets'
		prepend = extOP +'::'+ className +'::'+ functionName +'::'

		dataOut = op(me.fetch('RELIABLE_UDT'))

		args = [self.ownerComp.path, self.BankName, self.Presets]
		data = self.CompPresets

		print(sys.getsizeof(str(data)))
		print(sys.getsizeof(str(args)))


		msg = prepend + str(data) +'::'+ str(args)
		dataOut.send(msg)	

	def SendPresets(self):
		
		if self.Node == 'master' and self.DB.fetch('REMOTE_MODE') != 0 and self.PresetIndex != None:
			args = [self.CompPresets, self.ownerComp.path, self.BankName, self.Presets]
			#args = [self.CompPresets, self.ownerComp.path, self.BankName, self.StoreComp.fetch('CurPresets')]
			self.ControlOut.SendUDT('SetData', 'SetPresets', args)



	@property
	def Plugin(self):
		return self.ownerComp.par.Plugincomp.eval()
		
	@Plugin.setter
	def Plugin(self, value):
		self.ownerComp.par.Plugincomp = value

	@property
	def StoreComp(self):
		return self.ownerComp.par.Storecomp.eval()
		
	@StoreComp.setter
	def StoreComp(self, value):
		self.ownerComp.par.Storecomp = value

	@property
	def Controls(self):

		if op(self.Plugin.fetch('CompAttr')['attr']['uiPath']):

			return op(self.Plugin.fetch('CompAttr')['attr']['uiPath'])

		elif parent(2).op('controls'):

			return parent(2).op('controls')

		else:

			return op.MASTER_CONTROLS

	@property
	def ParsOP(self):
		return self.ownerComp.par.Parametersdat.eval()
		
	@ParsOP.setter
	def ParsOP(self, value):
		self.ownerComp.par.Parametersdat = value

	
	@property
	def PresetControls(self):
		#return self.ownerComp.par.Presetcontrols.eval()
		return self.Plugin.fetch('CompAttr')['attr']['presetControls']

	@PresetControls.setter
	def PresetControls(self, value):
		self._PresetControls = value

	@property
	def EditPars(self):
		return self.PresetControls.op('editPars').panel.state

	@property
	def EnabledParsList(self):
		return self.PresetControls.op('enabledParsList')

	'''
	@PresetControls.setter
	def PresetControls(self, value):
		self.ownerComp.par.Presetcontrols = value
	'''

	# Par Callbacks	

	def InitPresetsComp(self, *args):
		c = ui.messageBox('Initialize Presets', 'Are you sure? This will delete all Preset storage.', buttons =['Cancel', 'Initialize'])
		if c == 1:
			self.InitPresets()

	def Storepreset(self, *args):
		self.StorePreset(self.ownerComp.par.Presetname.eval())
		self.ownerComp.par.N = self.ownerComp.par.N.eval() + 1
		self.SetMenus()

	def Recallpreset(self, *args):
		self.RecallPreset(int(args[0]))

	def Updatepreset(self, *args):
		self.UpdatePreset(int(self.ownerComp.par.Recallpreset))
		self.SetMenus()

	def Duplicatepreset(self, *args):
		self.DuplicatePreset(int(self.ownerComp.par.Recallpreset))
		self.SetMenus()

	def Renamepreset(self, *args):
		self.RenamePreset(int(self.ownerComp.par.Recallpreset), args[0].eval())
		self.ownerComp.par.Renamepreset = ''
		self.SetMenus()

	def Deletepreset(self, *args):
		self.DeletePreset(int(self.ownerComp.par.Recallpreset))
		self.SetMenus()

	def Movepreset(self, *args):
		if self.ownerComp.par.Movepreset.eval() != 'None' and self.ownerComp.par.Movebefore.eval() != 'None':

			self.MovePreset(int(self.ownerComp.par.Movepreset) - 1, int(self.ownerComp.par.Movebefore) - 1)
			self.SetMenus()

	def Movebefore(self, *args):
		if self.ownerComp.par.Movepreset.eval() != 'None' and self.ownerComp.par.Movebefore.eval() != 'None':

			self.MovePreset(int(self.ownerComp.par.Movepreset) - 1, int(self.ownerComp.par.Movebefore) - 1)
			self.SetMenus()

	def Clearall(self, *args):

		c = ui.messageBox('Initialize Presets', 'This will clear all presets. Are you sure?', 
							buttons = ['Cancel', 'Clear Bank'])
		if c == 1:
			self.InitializeBank()

	def Clearallbanks(self, *args):

		c = ui.messageBox('Initialize Presets', 'This will clear all banks. Are you sure?', 
							buttons = ['Cancel', 'Clear All Banks'])
		if c == 1:
			self.Initialize()

	def Createnewbank(self, *args):
		bankName = self.ownerComp.par.Newbankname.eval()

		self.CreateBank(bankName, updatePar = True)
		self.SetMenus()
		
	def Selectbank(self, *args):

		bankName = self.BankNames[int(args[0])]
		self.SetBank(bankName)
		self.SetMenus()

	def Deletebank(self, *args):

		c = ui.messageBox('Delete Bank', 'Are you sure you want to delete ' + self.BankName + ' ?', 
							buttons = ['Cancel', 'Delete Bank'])
		if c == 1:
			self.DeleteBank(self.BankName)




