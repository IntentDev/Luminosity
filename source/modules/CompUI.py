class CompUI(object):

	def __init__(self,ownerComp):
	
		self.ownerComp = ownerComp
		self.path = self.ownerComp.path

		if self.StoreComp.op('config'):
			self.ownerComp.store('CompAttrTbl', self.StoreComp.op('config/attributes'))
			self.ownerComp.store('UIAttrTbl', self.StoreComp.op('config/uiAttr'))
			self.ownerComp.store('ModSources', self.StoreComp.op('config/modSources'))
		else:
			self.ownerComp.store('CompAttrTbl', self.StoreComp.op('attributes'))
			self.ownerComp.store('UIAttrTblUI', self.StoreComp.op('uiAttr'))
			self.ownerComp.store('ModSources', self.StoreComp.op('modSources'))

		self.ownerComp.store('CtrlsPath', self.ownerComp.path)	
		self.UIAttrTbl = self.ownerComp.fetch('UIAttrTbl', self.StoreComp.op('uiAttr'))

		self.ParNames = [r[0].val for r in self.UIAttrTbl.rows()[1:]]
		self.NumGadgets = len(self.ParNames)

		self.CtrlsParNames = [par.name for par in self.ownerComp.pars()]

		if 'Haspresets' in self.CtrlsParNames:

			if self.ownerComp.par.Haspresets.eval():

				self.Presets = self.Plugin.op('presets')
				self.PresetControls = self.ownerComp.op('../presetControls')
				self.PresetCtrls = self.ownerComp.op('presets')	
	
	def Setupscroll(self, *args):
		scrollW = 12
		
		list = self.ownerComp.op('controlsView')
		windowW = int(self.ownerComp.par.w) 
		windowH = int(self.ownerComp.par.h)
		listW = list.par.w
		listH = list.par.h

		parTable = self.ownerComp.op(self.ownerComp.fetch('Parameters'))
		listH = 0

		for r in parTable.rows()[1:]:
			listH += op(self.path + "/" + r[0]).par.h + list.par.alignmargin

		windowH -= self.ownerComp.op('label').par.h + 2
		try:
			if self.ownerComp.par.Haspresets.eval():
				windowH -= self.ownerComp.op('presets').par.h
		except:
			pass
		
		self.ownerComp.store('ListHeight', listH)
		self.ownerComp.store('WindowHeight',windowH)

		if windowH < listH:
			
			listW = windowW - scrollW - 2
			dispScroll = True

		elif windowH >= listH:

			listW = windowW
			dispScroll = False

		list.par.w = listW
		list.par.h = listH

		scroll = self.ownerComp.op('scroll')
		scroll.par.w = scrollW
		scroll.par.h = windowH - 2
		scroll.par.x = windowW - scrollW
		scroll.par.display = dispScroll
		self.ownerComp.store('DispScroll', dispScroll)

		settings = {'width': 400, 'height': 20, 'scrollWidth': 12, 'listHeight': windowH, 'fullListHeight': listH}

		storeComp = self.ownerComp.fetch('StoreComp')
		compAttr = storeComp.fetch('CompAttr')
		#compAttr['fullListHeight',1] = listH
		scroll.op('setup').run(settings)
		
		if dispScroll == False:
			scroll.op('slider').panel.v = .5
		else:
			scroll.op('slider').panel.v = 1
			
	def Setupui(self, *args, setupScroll = True):
		allParmMaps = self.ownerComp.op(self.ownerComp.fetch('ALL_PARM_MAPS'))
		ctrlsPath = self.ownerComp.fetch('CtrlsPath')
		allParmMaps.unstore(ctrlsPath)
		allParmMaps.store(ctrlsPath, {})
		width = int(self.ownerComp.par.w)
		uiAttr = self.ownerComp.fetch('UIAttrTbl')

		if 'Labelwidth' in [par.name for par in self.ownerComp.customPars]:
			labelWidth = self.ownerComp.par.Labelwidth.val
		else:
			labelWidth = 170


		for r in uiAttr.rows()[1:]:
			
			settings = {'width': width, 'height': 20, 'fieldWidth': 50, 'labelWidth': labelWidth, 'scrollWidth': 12, 'listHeight': 140 }

			gadget = self.ownerComp.op(r[0])

			attr = gadget.fetch('attr')
			
			displayName = attr['displayName']
			format = attr['format']
			
			settings['label'] = displayName
			settings['format'] = format	
			
			self.ownerComp.op(r[0] + '/setup').run(settings)

		if setupScroll:
			self.ownerComp.Setupscroll()
		
		if 'Haspresets' in self.CtrlsParNames:

			if self.ownerComp.par.Haspresets.eval():

				self.PresetControls.par.Presetcomp = self.Presets
				self.PresetCtrls.par.Presetcomp = self.Presets

				self.PresetCtrls.op('presetRadio/buttonCtrlMapSet/setup').run()
				self.PresetControls.op('setup').run()

	def Linkcompui(self, *args, initPresets = False):
		self.ownerComp.store('StoreComp', self.ownerComp.op('../plugin'))
		self.ownerComp.store('Parameters',self.ownerComp.op('../plugin/parameters'))
		self.ownerComp.store('CtrlsPath', self.ownerComp.path)

		if self.StoreComp.op('config'):
			self.ownerComp.store('CompAttrTbl', self.StoreComp.op('config/attributes'))
			self.ownerComp.store('UIAttrTbl', self.StoreComp.op('config/uiAttr'))
			self.ownerComp.store('ModSources', self.StoreComp.op('config/modSources'))
		else:
			self.ownerComp.store('CompAttrTbl', self.StoreComp.op('attributes'))
			self.ownerComp.store('UIAttrTbl', self.StoreComp.op('uiAttr'))
			self.ownerComp.store('ModSources', self.StoreComp.op('modSources'))


		#self.Display()

		if 'Haspresets' in self.CtrlsParNames:

			if self.ownerComp.par.Haspresets.eval():

				self.Presets = self.Plugin.op('presets')
				self.PresetControls = self.ownerComp.op('../presetControls')
				self.PresetCtrls = self.ownerComp.op('presets')

				if initPresets:
					self.Presets.initializeExtensions()

				self.PresetControls.par.Presetcomp = 'plugin/presets'
				self.PresetCtrls.par.Presetcomp = '../plugin/presets'
				self.PresetCtrls.par.Presetcontrols = '../presetControls'

		
	def Createcompui(self, *args, reCreate = True):

		if reCreate:
			for gadget in self.ownerComp.findChildren(tags = ['uiGadget']):
				gadget.destroy()

		self.Linkcompui(initPresets = True)

		controlsView = self.ownerComp.op('controlsView')

		uiGadgetPath = self.ownerComp.fetch('UIGADGETS')
		parDest = self.ownerComp.op(self.ownerComp.fetch('Parameters'))
		storeComp = self.ownerComp.fetch('StoreComp')
		uiAttrTble = self.ownerComp.fetch("UIAttrTbl")
		
		#update the parameters table if any new uiAttr entries are made
		#we store them in rows[] to ensure current parameters / global mods aren't overwritten so we don't have to reset those everytime Createcompui is called
		
		#update these so we don't get empty export blips.
		rows = []
		hasDefaultValuesOP = False

		if self.StoreComp.op("modRouter/default_values"):
			defaultValues = self.ownerComp.fetch("StoreComp").op("modRouter/default_values")
			defaultValues.lock = False
			defaultValues.clear()
			hasDefaultValuesOP = True


		for r in uiAttrTble.rows()[1:]:

			if hasDefaultValuesOP:
				defaultValues.appendChan(r[0].val)
				defaultValues[r[0].val][0] = r[4].val

			try:
				rows.append[parDest.row(r[0])]
				
			except:
				rows.append([r[0],r[4],'','','',''])

		if hasDefaultValuesOP:

			defaultValues.lock = True
				
		parDest.clear(keepFirstRow=True)
		for r in rows:
			parDest.appendRow(r)
		
		#get and store type, name, outputs, uiPath, presetControl
		compAttr = {'attr': {}, 'uiAttr': {}}
		compPar = {'values': {}} 
		
		tCompAttr = self.ownerComp.op(self.ownerComp.fetch('CompAttrTbl'))

		for r in tCompAttr.rows():	
			try: val = eval(str(r[1]))
			except: val = str(r[1])
			compAttr['attr'][str(r[0])] =  val

		self.ownerComp.op('label/text').par.text = tCompAttr['name', 1].val

		#get components UI attributes from table	
		t = self.ownerComp.fetch('UIAttrTbl')

		#get list of attribute names
		tAttr = []
		for c in t.cols():
			tAttr.append(c[0].val)

		#create gadget for each parameter in attribute table
		for r in t.rows()[1:]:
			
			gadgetName = str(r[0])
			gadgetType = str(r[5])

			if reCreate:
				if self.ownerComp.op(gadgetName):
					self.ownerComp.op(gadgetName).destroy()
				self.ownerComp.copy(self.ownerComp.op(uiGadgetPath + '/' + gadgetType), name = gadgetName)

			gadget = self.ownerComp.op(gadgetName)
			gadget.nodeX = 0
			gadget.nodeY = -100 * r[0].row
			gadget.par.order = r[0].row
			gadget.par.display = True
			gadget.par.reinitextensions.pulse()

			
			controlsView.outputCOMPConnectors[0].connect(gadget)

			initGadgetAttr = gadget.op('initAttributes')
			gadgetAttr = {}

			#get and store attributes as type set in gadget initAttributes table
			for attr in initGadgetAttr.rows()[1:]:

				if attr[0] in tAttr:

					attrVal = ''
					if attr[1]  == 'string':
						attrVal = str(t[r[0].row, str(attr[0])])
					elif attr[1]  == 'float':
						attrVal = float(t[r[0].row, str(attr[0])])
					elif attr[1] == 'integer':
						attrVal = int(t[r[0].row, str(attr[0])])
					elif attr[1] == 'bool':
						attrVal = bool(t[r[0].row, str(attr[0])])
					gadgetAttr[str(attr[0])] = attrVal
				
				#if the attribute doesn't exist in component table get initVal from gadget table and store
				else:

					attrVal = ''
					if attr[1]  == 'string':
						attrVal = str(attr[2])
					elif attr[1]  == 'float':
						attrVal = float(attr[2])
					elif attr[1] == 'integer':
						attrVal = int(attr[2])
					elif attr[1] == 'bool':
						attrVal = bool(attr[2])
					gadgetAttr[str(attr[0])] = attrVal


			compAttr['uiAttr'][gadgetName] = gadgetAttr
			gadget.store('attr', gadgetAttr)


			#get initParameter values from gadget, store gadget defaults and the 'value' parameter
			#from the component parameters table

			initGadgetPar = gadget.op('initParameters')
			gadgetPar = {}

			for par in initGadgetPar.rows()[1:]:

				if par[1] == 'string':
					gadgetPar[str(par[0])] = str(par[2])
				elif par[1] == 'float':
					gadgetPar[str(par[0])] = float(par[2])
				elif par[1] == 'integer':
					gadgetPar[str(par[0])] = int(par[2])
				elif par[1] == 'bool':
					gadgetPar[str(par[0])] = bool(par[2])
			
			gadgetPar['value'] = gadgetAttr['default']	
			

			gadget.op('setUI').run(gadgetPar, delayFrames = 1)

			for par in gadgetPar.items():
				parDest[gadgetName,par[0]] = par[1]

			compPar['values'][gadgetName] = gadgetPar
				
		storeComp.store('CompAttr',compAttr)
		storeComp.store('CompPar',compPar)
		self.ownerComp.store('UIAttr', compAttr['uiAttr'])

		import copy

		#op('setupUI').run(delayFrames = 1)
		#me.fetch("ROOT").Delay(delayFrames = 2).Call(self.ownerComp, 'Setupui', [])

		self.Setupui()
		self.ownerComp.par.reinitextensions.pulse()		
		
	def Hide(self, *args):

		if self.ownerComp.fetch('IsDisplayed') == 0:

			for parName in self.ParNames:
				gadget = self.ownerComp.op(parName)
				gadget.par.display = 0

				
	def Display(self, *args, display = True, setUI = True):

		self.ownerComp.store('GadgetCount', 1)
		self.ownerComp.store('IsDisplayed', 1)

		compPar = self.ownerComp.fetch('StoreComp').fetch('CompPar', {})
		compAttr = self.ownerComp.fetch('StoreComp').fetch('CompAttr', {})

		self.ownerComp.UpdateCompUI(compPar, compAttr, self.ParNames)

	def Displaycontrols(self, *args):

		self.ownerComp.store('IsDisplayed', 1)
		self.Display()

	def Hidecontrols(self, *args):

		self.ownerComp.store('IsDisplayed', 0)
		self.Hide()

	@property
	def Plugin(self):
		if 'Plugin' in self.ownerComp.pars():
			return self.ownerComp.par.Plugin.eval()
		else:
			return self.ownerComp.op('../plugin')

	@Plugin.setter
	def Plugin(self, value):
		if 'Plugin' in self.ownerComp.pars():
			self.ownerComp.par.Plugin = value
		
	@property
	def StoreComp(self):
		if 'Storecomp' in self.ownerComp.pars():
			return self.ownerComp.par.Storecomp.eval()
		else:
			return self.Plugin

	@StoreComp.setter
	def StoreComp(self, value):
		if 'Storecomp' in self.ownerComp.pars():
			self.ownerComp.par.Storecomp = value
			self.ownerComp.store('StoreComp', value)


	@property
	def ParsOP(self):
		if 'Parametersdat' in self.ownerComp.pars():
			return self.ownerComp.par.Parametersdat.eval()
		else:
			return self.Plugin.op('parameters')

	@ParsOP.setter
	def ParsOP(self, value):
		if 'Parametersdat' in self.ownerComp.pars():
			self.ownerComp.par.Parametersdat = value
			self.ownerComp.store('Parameters', value)