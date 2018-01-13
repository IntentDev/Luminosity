'''
Call function in custom built class from right click in UI element. The first arg in the call is the UI element type 
while the following are actual arguments for the various menu functions (which all must take along all the same
arguments either implicitly or via *args.

The __init__ of the class must have a list of the function names and their corresponding menu labels.

The class must inherit the RightClick class and it must have an Open function (called from the right click in UI element)
that calls OpenMenu() in RightClick. It must pass along the args and menuItems.

'''

class RightClick(object):

	def __init__(self):

		self.rcMenu = op.RC_MENU

		self.absMouseOP = op(me.fetch('MASTERABSMOUSE'))
		self.menu = self.rcMenu.op('menu')
		self.window = self.rcMenu.op('window')


		return

	def OpenMenu(self, args, menuItems):
	
		#print('Open RC')
		#print(dir(self))
		#print(args)
		
		#self.rcMenu.op('headerText/text').par.text = args[-1]
		items = self.rcMenu.op('items')
		items.clear()
		for n in menuItems:
			items.appendRow([n[0], n[1]])

		#print(menuItems)

		
		absX = self.absMouseOP['tx'].eval()
		absY = self.absMouseOP['ty'].eval()

		menuW = self.menu.par.w.eval() * .5
		menuH = self.menu.par.h.eval() * .5

		if absX < menuW:
			self.window.par.winoffsetx = menuW
		elif absX > op.UI.par.w - menuW:
			self.window.par.winoffsetx = -menuW	
		else:
			self.window.par.winoffsetx = 0

		if absY < menuH:
			self.window.par.winoffsety = menuH
		elif absY > op.UI.par.h - menuH:
			self.window.par.winoffsety = -menuH	
		else:
			self.window.par.winoffsety = 0



		self.rcMenu.op('menu').setFocus()



		self.rcMenu.store('Args', args)
		self.rcMenu.op('window').par.winopen.pulse()

		return

class EffectSlot(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Clear', 'Delete'],
							['Cut', 'Cut'], ['Copy', 'Copy'], ['Paste', 'Paste']]


		self.opNames = ['plugin', 'controls', 'presetControls']					

	
		return

	def Open(self, *args):
		#print(args)
		header = 'Insert ' + str(args[2])
		self.rcMenu.op('headerText/text').par.text = header
		self.OpenMenu(args, self.rcMenuItems)
		self.rcMenu.op('headerText/text').cook()

	def SetEffectSlotsUI(self, gadget, slotId, name, path):

		attr = gadget.fetch('attr')
		itemTable = op(attr['itemTable'])
		storeComp = gadget.fetch('StoreComp')
		compPar = storeComp.fetch('CompPar')
		effectSlots = compPar['values']['effectSlots']
		parName = 'slot' + str(slotId)
		effectSlots[parName]['name'] = name
		effectSlots[parName]['path'] = path
		itemTable[slotId + 1,'name'] = name
		itemTable[slotId + 1,'path'] = path

		effectSlotsState = gadget.op('states')
		effectSlotsState.Lc(effectSlotsState, slotId, 0)
		gadget.parent().EffectSlotsStateSet(effectSlotsState.path)


	def Clear(self, gadget, slotId):

		#print('Clear Slot:', slotId)

		slotName = 'slot ' + str(slotId + 1)
	
		name = 'No Effect'
		#path = gadget.fetch('PLUGINS') + '/effects/noEffect'
		path = '../assets/components/effects/noEffect.lmFX.tox'
		channel = gadget.fetch('Channel')
		dataSlotPath = channel +'/effects/slot' + str(slotId)
		
		self.SetEffectSlotsUI(gadget, slotId, name, path)

		gadget.fetch('ROOT').Load().LoadEffect(path, dataSlotPath)
		#print(gadget)

	def Cut(self, gadget, slotId):

		self.Copy(gadget, slotId)
		self.Clear(gadget, slotId)

		pass

	def Copy(self, gadget, slotId):

		channel = gadget.fetch('Channel')
		dataSlotPath = channel +'/effects/slot' + str(slotId)
		dataSlot = op(dataSlotPath)


		for n in self.opNames:

			srcOP = dataSlot.op(n)
			if op.COPIED_EFFECT.op(n):
				op.COPIED_EFFECT.op(n).destroy()

			if srcOP:

				op.COPIED_EFFECT.copy(srcOP)



	def Paste(self, gadget, slotId):
		
		if op.COPIED_EFFECT.op('plugin') and op.COPIED_EFFECT.op('controls'):

			name = op.COPIED_EFFECT.op('plugin').fetch('CompAttr')['attr']['name']
			path = op.COPIED_EFFECT.path
			channel = gadget.fetch('Channel')
			dataSlotPath = channel +'/effects/slot' + str(slotId)

			dataSlot = op(dataSlotPath)

			self.SetEffectSlotsUI(gadget, slotId, name, path)

			for n in self.opNames:

				srcOP = op.COPIED_EFFECT.op(n)

				if dataSlot.op(n):
					dataSlot.op(n).destroy()

				if srcOP:
					dataSlot.copy(srcOP)



class Gadget(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Reset', 'Set Default'], ['ClearMap', 'Clear Map']]
		self.rcMenuItems2 = [['Reset', 'Set Default'], ['ClearMap', 'Clear Map'], ['Rename', 'Rename']]
	
		return

	def Open(self, *args, rename = False):
	
		self.rcMenu.op('headerText/text').par.text = args[-1]
		self.OpenMenu(args, [self.rcMenuItems, self.rcMenuItems2][int(rename)])

	def Reset(self, gadgetPath, setUIPath, resetVal, valueType, valueName):

		gadget = op(gadgetPath)
		gadgetParent = gadget.parent().path

		parDest = gadget.fetch('Parameters')
		if parDest[valueName, valueType] != None:
			parDest[valueName, valueType] = resetVal[valueType]

			gadget.StoreValue(gadget, valueType, resetVal[valueType])
			
			
			#gadget.parent().SetUI(resetVal)
			setUI = op(setUIPath)
			try:
				setUI.run(resetVal)
			except:
				pass

		#print('Set Default')

	def ClearMap(self, gadgetPath, setUIPath, resetVal, valueType, valueName):

		#print(gadgetPath)

		gadget = op(gadgetPath)
		gadgetP = gadget.parent()
		ctrlsPath = gadgetP.fetch('CtrlsPath')
		#print(ctrlsPath)
		ctrlMaps = op(gadgetP.fetch('CTRL_MAPS'))
		ctrlMaps.op('delMap').run(gadgetP.path, ctrlsPath)
		
		

		#print('Clear Map')

	def Rename(self, gadgetPath, setUIPath, resetVal, valueType, valueName):

		gadget = op(gadgetPath)
		label = gadget.op('label')
		label.par.clickthrough = 0
		label.setKeyboardFocus(selectAll = True)

class Clip(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Clear', 'Delete'], ['Rename', 'Rename'], ['UnSelect', 'Un-Select'],
							['Cut', 'Cut'], ['Copy', 'Copy'], ['Paste', 'Paste'], ['OpenNetwork', 'Open Network']]
	

		self.opNames = ['plugin', 'controls', 'presetControls']					

		return

	def Open(self, *args):
		#print(args)

		header = op(args[1]).op('select2').par.top.eval().par.text.val
	
		self.rcMenu.op('headerText/text').par.text = header
		self.rcMenu.op('headerText/text').cook()

		self.OpenMenu(args, self.rcMenuItems)

	def Delete(self, clipPath, clipId, clipName, clipLane):

		clip = op(clipPath)
		name = 'ClearSlot'
		path = clip.fetch('PLUGINS') + '/players/noClip'
		t = 'COMP'
		bank = clip.fetch('CUR_BANK')

		op.LOAD_CLIPS.LoadComp(name, path, t, bank, clipLane, clipName)
		
		clipData = op(clip.fetch('CLIP_DATA'))
		clipDataBase = clipData.fetch('CLIP_DATABASE', {})
		cDataKey = bank +'/'+ clipLane +'/'+ clipName

		curTrigClip = clip.fetch('CurTrigClip')
		if curTrigClip[0] == clip.digits:
			clip.Stop(op.NO_CLIP.path, clip.parent(), clip.parent().digits)

		mod.extPFMClips.ClearClipControls(clip)


	def Clear(self, clipPath, clipId, clipName, clipLane):
	
		confirm = ui.messageBox('Delete Clip', 'Delete Clip ' + str(clipId + 1) + '?', buttons = ['Cancel', 'Delete'])

		if confirm == 1:

			self.Delete(clipPath, clipId, clipName, clipLane)

	def Cut(self, clipPath, clipId, clipName, clipLane):
		self.Copy(clipPath, clipId, clipName, clipLane)
		self.Delete(clipPath, clipId, clipName, clipLane)


	def Copy(self, clipPath, clipId, clipName, clipLane):
		#print(clipPath)
		clip = op(op(clipPath).DataClipPath.val)
		#print(clip)

		for n in self.opNames:

			srcOP = clip.op(n)
			if op.COPIED_CLIP.op(n):
				op.COPIED_CLIP.op(n).destroy()

			if srcOP:

				op.COPIED_CLIP.copy(srcOP)
		
		op.COPIED_CLIP.op('plugin').Active = False
		
	def Paste(self, clipPath, clipId, clipName, clipLane):
		clip = op(op(clipPath).DataClipPath.val)

		if op.COPIED_CLIP.op('plugin'):

			for n in self.opNames:

				if clip.op(n):
					clip.op(n).destroy()
				
				if op.COPIED_CLIP.op(n):
					clip.copy(op.COPIED_CLIP.op(n))

			label = op.COPIED_CLIP.op('plugin').fetch('CompAttr')['attr']['name']
			labelOP = clip.op('label')
			labelOP.lock = False
			labelOP.par.text = label
			labelOP.cook()
			labelOP.lock = True

	def OpenNetwork(self, clipPath, clipId, clipName, clipLane):
		clip = op(op(clipPath).DataClipPath.val)
		plugin = clip.op('plugin')
		name = plugin.fetch('CompAttr')['attr']['name']
		
		p = ui.panes.createFloating(type = PaneType.NETWORKEDITOR, name = name)	
		p.owner = plugin

				
	def UnSelect(self, clipPath, clipId, clipName, clipLane):
	
		clip = op(clipPath)	
		
		select = clip.op('select')
		if select.panel.state.val == 1:
			
			clip.AssignNoClipCtrls()

			select.panel.state = 0
			clip.parent().panel.radio = -1

	def Rename(self, clipPath, clipId, clipName, clipLane):
		#print(clipLane)
		uiClip = op(clipPath)
		numRows = op.DATABASE.fetch('NUM_CLIP_CHAN')
		numCols = op.DATABASE.fetch('NUM_CLIP_SCENES')
		if clipId != 0:
			#row = math.floor(clipId / numCols)
			row = int(clipLane.replace('clipLane', ''))
			col = clipId % numCols
		else:
			row = 0
			col = 0
		row = numRows - row - 1

		labelPosX = col * 102
		labelPosY = row * 80

		label = op(me.fetch('CLIP_LANES_UI') +'/labelClip')
		label.par.x = labelPosX
		label.par.y = labelPosY

	
		clip = op(uiClip.DataClipPath.val)
		#print(clip)
		clipLabel = clip.op('label')
		clipLabel.lock = False
		text = clipLabel.par.text.val
		label.op('string')[0,0] = text
		label.par.display = 1
		
		label.setKeyboardFocus(selectAll = True)
		label.cook(force = True)
		#print (row, col)

class Presets(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Rename', 'Rename'], ['Update', 'Update'], ['Duplicate', 'Duplicate'],
							['Copy', 'Copy'], ['Paste', 'Paste'], ['AppendCopied', 'Append Copied'],
							['Delete', 'Delete'], ['DeleteAll', 'Delete All']]	

		self.rcMenuItems2 = [['AppendCopied', 'Append Copied']]

	def Open(self, *args):

		viewSwitch = int(args[3] == - 1)
	
		self.rcMenu.op('headerText/text').par.text = [str(args[-2] + 1) + '. ' + args[-1], args[-1]][viewSwitch]

		self.OpenMenu(args, [self.rcMenuItems, self.rcMenuItems2][viewSwitch])

	def Rename(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		cellAttribs = listCOMP.cellAttribs[presetIndex, 1]
		cellAttribs.editable = True
		#cellAttribs.textColor = [0.5, 0.5, 0.5, 1]
		listCOMP.setKeyboardFocus(presetIndex, 1, selectAll = True)

	def Update(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.UpdatePreset(presetIndex)

	def Duplicate(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.DuplicatePreset(presetIndex)
		listCOMP.par.reset.pulse()

	def Delete(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.DeletePreset(presetIndex)
		listCOMP.par.reset.pulse()

	def DeleteAll(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.par.Clearall.pulse()

	def Copy(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.CopyPreset(presetIndex)

	def Paste(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.PastePreset(presetIndex)

	def AppendCopied(self, PresetsCOMP, listCOMP, presetIndex, presetName):
		PresetsCOMP.AppendCopiedPreset(presetIndex)

class PresetsBanks(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Rename', 'Rename'], ['Duplicate', 'Duplicate'],
							['Delete', 'Delete'], ['DeleteAll', 'Delete All']]	

	def Open(self, *args):

		self.rcMenu.op('headerText/text').par.text = args[-1]
		self.OpenMenu(args, self.rcMenuItems)

	def Rename(self, PresetsCOMP, listCOMP, row, bankName):
		listCOMP.cellAttribs[row, 0].editable = True
		listCOMP.setKeyboardFocus(row, 0)

	def Duplicate(self, PresetsCOMP, listCOMP, row, bankName):
		PresetsCOMP.DuplicateBank(bankName)
		listCOMP.par.reset.pulse()

	def Delete(self, PresetsCOMP, listCOMP, row, bankName):
		PresetsCOMP.DeleteBank(bankName)
		listCOMP.store('CurrentItem', 0)

		listCOMP.op('../bankName/string')[0, 0] = PresetsCOMP.ext.Presets.BankNames[0]
		listCOMP.par.reset.pulse()

	def DeleteAll(self, PresetsCOMP, listCOMP, row, bankName):
		PresetsCOMP.par.Clearallbanks.pulse()

class CrossFadeAB(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['Linear', 'Linear'], ['Cubic', 'Cubic'], ['Bezier1', 'Bezier1'], 
							['Bezier2', 'Bezier2'], ['SmoothStep1', 'SmoothStep1'], 
							['SmoothStep2', 'SmoothStep2'], ['Step', 'Step']]

	def Open(self, *args):

		self.rcMenu.op('headerText/text').par.text = 'Cross Curves'
		self.OpenMenu(args, self.rcMenuItems)
		self.rcMenu.op('headerText/text').cook()

	def Linear(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 0
	def Cubic(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 1
	def Bezier1(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 2
	def Bezier2(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 3
	def SmoothStep1(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 4
	def SmoothStep2(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 5
	def Step(self, crossFadeAB): crossFadeAB.par.Lookupcurves = 6

class PLUGIN_DESIGNER(RightClick):
	def __init__(self):

		RightClick.__init__(self)

		self.itemsGadget = [['valSlider', 'valSlider'], ['valSliderM', 'valSliderM'], ['button', 'button'], 
							['field', 'field'], ['fileLoader', 'fileLoader'],['folderLoader', 'folderLoader'], 
							['droplist', 'droplist'],['droplistTex', 'droplistTex'],
							['radioButton', 'radioButton'],['multiButton', 'multiButton'],
							['videoSource', 'Video Source']]
	
		self.itemsFormat = [['float', 'float'], ['int', 'int'], ['string', 'string']]
		self.itemsFormatButton = [['toggle', 'toggle'], ['momentary', 'momentary']]

		self.rcMenuItems = [self.itemsGadget, self.itemsFormat, self.itemsFormatButton]

		self.menuTypes = ['Gadget', 'Format', 'FormatButton']



	def Open(self, *args): 

		menuItemsIndex = self.menuTypes.index(args[1])
		self.OpenMenu(args, self.rcMenuItems[menuItemsIndex])
		
	def valSlider(self, *args):	op.PLUGIN_DESIGNER.PluginEditor_setGadget("valSlider")
	def valSliderM(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("valSliderM")
	def button(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("button")
	def field(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("field")
	def fileLoader(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("fileLoader")
	def folderLoader(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("folderLoader")
	def droplist(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("droplist")
	def droplistTex(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("droplistTex")
	def radioButton(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("radioButton")
	def multiButton(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("multiButton")
	def videoSource(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setGadget("videoSource")

	def float(self, *args):	op.PLUGIN_DESIGNER.PluginEditor_setFormat("float")
	def int(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setFormat("int")
	def string(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setFormat("str")

	def toggle(self, *args):	op.PLUGIN_DESIGNER.PluginEditor_setFormat("toggledown")
	def momentary(self, *args): op.PLUGIN_DESIGNER.PluginEditor_setFormat("momentary")

class Browser(RightClick):

	def __init__(self):

		RightClick.__init__(self)
		self.rcMenuItems = [['EditPlugin', 'Edit Plugin']]
	
		return

	def Open(self, *args):
		#print(args)

		header = ''
	
		self.rcMenu.op('headerText/text').par.text = header
		self.rcMenu.op('headerText/text').cook()

		self.OpenMenu(args, self.rcMenuItems)

	def EditPlugin(self, keyContent):

		p = ui.panes.createFloating(type = PaneType.NETWORKEDITOR, name = keyContent['name'])
		p.owner = op(keyContent['location'])
		p.home(zoom = True)



		
	

