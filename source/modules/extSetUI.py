

class SetUI(object):

	def __init__(self, extPath):

		self.extPath = extPath
		self.extOP = op(extPath)

		#self.itemTableGadgets = ['radioButton', 'droplist', 'multiButton', 'exclusiveButton', 'buttons']

	def SetHeight(self, reset, offset):

		#args ( args[0] = reset, args[1]= offset)

		controls = self.extOP 

		scroll = controls.op('scroll')
		scrollSlider = scroll.op('slider')
		scrollW = scroll.par.w

		list = controls.op('controlsView')
		windowW = int(controls.par.w)
		windowH = int(controls.par.h)
		listW = list.par.w
		listH = controls.fetch('ListHeight')

		windowH -= controls.op('label').par.h
		windowH -= controls.op('presets').par.h

		controls.store('ListHeight', listH)
		controls.store('WindowHeight',windowH)

		dispScroll = bool(controls.op('scroll').par.display)

		if windowH < listH and dispScroll == 0:
			
			listW = windowW - scrollW - 2
			dispScroll = True

			if controls.panel.inside == 1:

				scroll.op('mcScroll').par.active = 1
				
		elif windowH >= listH and dispScroll == 1:

			listW = windowW
			dispScroll = False
			scrollSlider.panel.v = 0
			scrollSlider.panel.v = 1
			scroll.op('mcScroll').par.active = 0
			
		list.par.w = listW
		list.par.h = listH
		list.par.y = list.par.y + offset

		scroll.par.h = windowH - 2
		scroll.par.x = windowW - scrollW
		scroll.par.display = dispScroll
		controls.store('DispScroll', dispScroll)

		storeComp = controls.fetch('StoreComp')
		compAttr = storeComp.fetch('CompAttr')
		compAttr['attr']['fullListHeight'] = listH

		#scroll.op('setHeight').run(reset)
		self.SetScrollKnobHeight(reset)

		if reset == True:

			scrollSlider.panel.v = 0
			scrollSlider.panel.v = 1

	def SetScrollKnobHeight(self, reset):

		parentH = self.extOP.op('scroll').par.h
		knobHeight = min(parentH,max(16, parentH - (self.extOP.fetch('ListHeight') - parentH)))
		knob = self.extOP.op('scroll/slider/knob')
		knob.par.h = knobHeight

		if reset == True:
			knob.par.y = max(min(parentH - knobHeight * 0.5, parentH - knobHeight - 1), 1)

		else:		

			v = self.extOP.op('scroll/slider').panel.v		
			knob.par.y = max(min(v * parentH - knobHeight*.5, parentH - knobHeight - 1), 1)

	def SetScrollKnobWidth(self, reset):

		parentW = self.extOP.op('scroll').par.w
		knobWidth = min(parentW,max(16, parentW - (self.extOP.fetch('ListWidth') - parentW)))
		knob = self.extOP.op('scroll/slider/knob')
		knob.par.w = knobWidth

		if reset == True:
			knob.par.x = max(min(parentW - knobWidth * 0.5, parentW - knobWidth - 1), 1)

		else:		

			u = self.extOP.op('scroll/slider').panel.u		
			knob.par.x = max(min(v * parentW - knobWidth*.5, parentW - knobWidth - 1), 1)

	def ModOpen(self, path):

		parent = op(path)

		parent.op('modUI').par.display = 1	

		gadgetHeight = parent.fetch('GadgetHeight')
		modHeight = gadgetHeight * 2 + 4	
		parent.par.h = gadgetHeight + modHeight

		listHeight = parent.fetch('ListHeight')
		parent.parent().store('ListHeight', listHeight + modHeight)
		parent.parent().SetHeight(False, -modHeight)


		name = parent.fetch('attr')['name']
		compPar = op(parent.fetch('StoreComp')).fetch('CompPar')
		settings = compPar['values'][name]

		self.extOP.ButtonSet(parent.op('modUI').op('active'), settings['modOn'])
		self.extOP.ModGainOffsetSet(parent.op('modUI').op('gain'), settings['modGain'])
		self.extOP.ModGainOffsetSet(parent.op('modUI').op('offset'), settings['modOffset'])
		self.extOP.DroplistSet(parent.op('modUI').op('sources'), settings['modSource'])

	def ModClose(self, path):

		parent = op(path)

		parent.op('modUI').par.display = 0
	
		gadgetHeight = parent.fetch('GadgetHeight')
		modHeight = gadgetHeight * 2 + 4	

		parent.par.h = gadgetHeight
		
		listHeight = parent.fetch('ListHeight')
		parent.parent().store('ListHeight', listHeight - modHeight) 
		parent.parent().SetHeight(False, modHeight)
	
	def NormalizeVal(self, low, high, value):

		try: return (value - low) / (high - low)
		except: return 0

	def NormalizeValMod(self, low, high, value):

		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))

		try: return (value - low) / (high - low)
		except: return 0

	def RangeVal(self, oLow, oHigh, nLow, nHigh, value, format):

		value = ((nHigh - nLow) * (value -oLow)) / (oHigh - oLow)  + nLow

		if format == 'integer':
			value = round(value)

		return value

	def ExpandVal(self, low, high, value, format):

		value = ((high - low) * (value)) / 1 + low

		if format == 'integer':
			value = round(value)

		return value
	
	def ValSliderSet(self, path, value):

		parent = op(path)

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
		name = parent.fetch('attr')['name']
		format = parent.fetch('attr')['format']

		position = self.extOP.NormalizeVal(low, high, value)

		slider = parent.op('slider')
		slider.panel.u = position
		slider.store('InitU', position)
		slider.store('PrevU', position)

		if format == 'float':
				value = round(value,2)
		else:
			value = round(value)
			parent.op('field/text').cook(force = True)
		parent.op('field/string')[0,0] = value
		
		slider.SlideKnob(slider, position)

	def ValSliderSetCtrlMap(self, path, value):

		
		parent = op(path)
		attr = parent.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		form = attr['format']
		name = attr['name']

		slider = parent.op('slider')
		slider.panel.u = value
		slider.SlideKnob(slider, value)


		value = self.extOP.ExpandVal(low, high, value, form)

		if parent.op('field/string'):
			parent.op('field/string')[0,0] = round(value,2)

	def ValSliderVSet(self, path, value):

		parent = op(path)

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
		name = parent.fetch('attr')['name']

		position = self.extOP.NormalizeVal(low, high, value)

		parent.op('slider').panel.v = position
		
		if parent.op('field/string'):
			parent.op('field/string')[0,0] = round(value,2)

	def ValSliderVSetCtrlMap(self, path, value):

		parent = op(path)
		attr = parent.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		form = attr['format']
		name = attr['name']

		parent.op('slider').panel.v = value
		value = self.extOP.ExpandVal(low, high, value, form)

		parent.op('field/string')[0,0] = round(value,2)

	def ValSliderMSet(self, path, settings):
		#print(settings)

		parent = op(path)
		#print(parent)

		value = settings['value']

		name = parent.fetch('attr')['name']

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
		name = parent.fetch('attr')['name']

		position = self.extOP.NormalizeVal(low, high, value)

		slider = parent.op('slider')

		slider.panel.u = position
		slider.store('InitU', position)
		slider.store('PrevU', position)
		parent.op('field/string')[0,0] = round(value,2)
		slider.SlideKnob(slider, position)

		
		if parent.op('mod').panel.state == 1:
			active = parent.op('modUI/active')
			self.extOP.ButtonSet(active.path, settings['modOn'])
			sources = parent.op('modUI/sources')
			self.extOP.DroplistSet(sources.path, settings['modSource'])
			gain = parent.op('modUI/gain')
			self.extOP.ModGainOffsetSet(gain.path, settings['modGain'])
			offset = parent.op('modUI/offset')
			self.extOP.ModGainOffsetSet(offset.path, settings['modOffset'])

		
		colors = [parent.fetch('FONTCOL1')[0], parent.fetch('FONTCOL2')[0]]
		
		col = colors[settings['modOn']]
		
		par = parent.op('mod/text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def SliderVSet(self, path, value):

		parent = op(path)

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
		name = parent.fetch('attr')['name']

		position = self.extOP.NormalizeVal(low, high, value)

		parent.op('slider').panel.v = position

	def SliderVSetCtrlMap(self, path, value):

		parent = op(path)
		attr = parent.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		form = attr['format']
		name = attr['name']

		parent.op('slider').panel.v = value

	def KnobPolarSet(self, path, value):

		parent = op(path)

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
		name = parent.fetch('attr')['name']

		nLow = -50
		nHigh = 230
	
		angle = self.extOP.RangeVal(low, high, nLow, nHigh, value, float)

		parent.op('knob/over1').par.r = angle

	def KnobPolarSetCtrlMap(self, path, value):

		parent = op(path)

		low = 0
		high = 1

		nLow = -50
		nHigh = 230

		angle = self.extOP.RangeVal(low, high, nLow, nHigh, value, float)

		parent.op('knob/over1').par.r = angle

	def ModGainOffsetSet(self, path, value):

		parent = op(path)

		low = parent.fetch('attr')['rangeLow']
		high = parent.fetch('attr')['rangeHigh']
	
		position = self.extOP.NormalizeValMod(low, high, value)

		slider = parent.op('slider')

		slider.panel.u = position
		slider.store('InitU', position)
		slider.store('PrevU', position)
		parent.op('field/string')[0,0] = round(value,2)

		slider.SlideKnob(slider, position)

	def ModGainOffsetSetCtrlMap(self, path, value):

		parent = op(path)

		attr = parent.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		form = attr['format']

		slider = parent.op('slider')
		slider.panel.u = value
		slider.SlideKnob(slider, value)

		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))
		value = self.extOP.ExpandVal(low, high, value, form)

		parent.op('field/string')[0,0] = round(value,2)

	def ButtonSet(self, path, value):

		parent = op(path)

		button = parent.op('button')
		par = button.par

		bgCol = me.fetch('BUTTONCOL1')[int(value) * 2]
		fontCol = me.fetch('FONTCOL1')[int(value) * 2]

		par.bgcolorr = bgCol [0]
		par.bgcolorg = bgCol [1]
		par.bgcolorb = bgCol [2]
		par.bgalpha = bgCol [3]

		par = button.op('text').par

		par.fontcolorr = fontCol[0]
		par.fontcolorg = fontCol[1]
		par.fontcolorb = fontCol[2]
		par.fontalpha = fontCol[3]

		button.panel.state = value

	def TimecodeSet(self, path, value):

		parent = op(path)
		string = parent.op('timecodeField/string')

		string[0, 0] = value
		
	def ButtonSetCtrlMap(self, path, value):

		parent = op(path)

		button = parent.op('button')
		par = button.par

		bgCol = me.fetch('BUTTONCOL1')[int(value) * 2]
		fontCol = me.fetch('FONTCOL1')[int(value) * 2]

		par.bgcolorr = bgCol [0]
		par.bgcolorg = bgCol [1]
		par.bgcolorb = bgCol [2]
		par.bgalpha = bgCol [3]

		par = button.op('text').par

		par.fontcolorr = fontCol[0]
		par.fontcolorg = fontCol[1]
		par.fontcolorb = fontCol[2]
		par.fontalpha = fontCol[3]

		value = round(value)

		button.panel.state = value

	def RadioButtonSet(self, path, value):

		gadget = op(path)

		gadget.op('cellId')[0,0] = value
		gadget.panel.cellradioid = value

	def ButtonsSet(self, path, value):

		gadget = op(path)

		
		for i in range(gadget.op('cellId').numRows):
			try:
				gadget.op('cellId')[i, 0] = value[i]
			except:
				pass

	def EffectSlotsSet(self, path, value):

		gadget = op(path)

		#gadget.panel.cellradioid = value

	def EffectSlotsStateSet(self, path):

		gadget = op(path)
		
		storeComp = gadget.fetch('StoreComp')
		compPar = storeComp.fetch('CompPar')
		effectSlots = compPar['values']['effectSlots']
		itemTable = gadget.fetch('attr')['itemTable']

		n = 1
		effectSlots.pop('value', None)
		for i in effectSlots.items():
			
			state = i[1]['state']	
			gadget.op('cellId')[i[0],1] = state
			op(itemTable)[i[0], 'state'] = state
			n += 1

	# not being used....
	def EffectSlotsPathSet(self, path):

		gadget = op(path)

		storeComp = gadget.fetch('StoreComp')
		compPar = storeComp.fetch('CompPar')
		effectSlots = compPar['values']['effectSlots']
		itemTable = gadget.fetch('attr')['itemTable']

		n = 1
		effectSlots.pop('value', None)
		for i in effectSlots.items():

			name = i[1]['name']	
			op(itemTable)[i[0], 'name'] = name
			path = i[1]['path']	
			op(itemTable)[i[0], 'path'] = path
			n += 1

	def FieldSet(self, path, value):

		parent = op(path)
		parent.op('field/string')[0,0] = value

	def DroplistSet(self, path, value):

		parent = op(path)

		itemTable = parent.op('selectItems')
		if value < itemTable.numRows:
			item = itemTable[value, 0].val
		else:
			item = itemTable[0, 0].val

		parent.op('dropButton/button/button/text').par.text = item

	def DisplayModSet(self, path, displayMod, value):

		parent = op(path)

		#name = parent.fetch('attr')['name']
		#compAttr =op(parent.fetch('StoreComp')).fetch('CompAttr')
		#displayMod = compAttr['uiAttr'][name]['displayMod']

		parent.panel.state = displayMod

		colors = [parent.fetch('BUTTONCOL1')[0], parent.fetch('BUTTONCOL1')[2]]

		col = colors[displayMod]

		par = parent.par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

		colors = [[parent.fetch('FONTCOL1')[0], parent.fetch('FONTCOL1')[2]], [parent.fetch('FONTCOL2')[0], parent.fetch('FONTCOL2')[2]]]

		col = colors[value][displayMod]

		par = parent.op('text').par
		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def CheckBoxSet(self, path, value):

		parent = op(path)

		button = parent.op('checkBoxButton')
		
		'''
		par = button.par
		bgCol = me.fetch('BUTTONCOL1')[int(value) * 2]
		fontCol = me.fetch('FONTCOL1')[int(value) * 2]

		par.bgcolorr = bgCol [0]
		par.bgcolorg = bgCol [1]
		par.bgcolorb = bgCol [2]
		par.bgalpha = bgCol [3]

		par = button.op('text').par

		par.fontcolorr = fontCol[0]
		par.fontcolorg = fontCol[1]
		par.fontcolorb = fontCol[2]
		par.fontalpha = fontCol[3]
		'''

		button.panel.state = value

	def UpdateCompUI(self, compPar, compAttr, parNames):		

		n = 1
		for parName in parNames:

			self.extOP.op(parName).store('attr', compAttr['uiAttr'][parName])

			d = op.LM.Delay(delayFrames = n, fromOP = self.extOP)
			d.Call(self.extOP.op(parName), 'SetUI', self.extOP, compPar['values'][parName])
			d.Set(self.extOP.op(parName).par, 'display', 1)

			n += 1
			
		self.extOP.op('scroll/slider').panel.v = 1

	def ButtonCtrlMapSet(self, path, value):

		button = op(path)

		par = button.par

		bgCol = me.fetch('CTRL_MAP_COL')[0]

		par.bgcolorr = bgCol [0]
		par.bgcolorg = bgCol [1]
		par.bgcolorb = bgCol [2]
		par.bgalpha = bgCol [3]
		par.display = value
		
	def SetPar(self, gadget, valueType, value):
		
		compPar = self.extOP.fetch('StoreComp').fetch('CompPar')
		
		gadget.SetUI(self.extOP, {valueType: value})
		compPar['values'][gadget.name][valueType] = value
		self.extOP.fetch("Parameters")[gadget.name, valueType] = value

	# This will only work for parameters without mods		
	def SetParameter(self, gadgetName, val, lockParms = False):
		
		compPar = self.extOP.fetch('StoreComp').fetch('CompPar')
		gadget = self.extOP.op(gadgetName)
		valueType = 'value';
		gadget.SetUI(self.extOP, {valueType: val})
		compPar['values'][gadgetName][valueType] = val
		self.extOP.fetch("Parameters")[gadgetName, valueType] = val

		
	def LockParameterExecute(self):

		params = self.extOP.fetch("Parameters")
		params.store("AllowParameterExecute", False)
		ext.lm.Delay(delayFrames = 1, fromOP = self.extOP ).Call(self.extOP, 'AllowParameterExecute')

		
	def AllowParameterExecute(self):

		params = self.extOP.fetch("Parameters")
		params.store("AllowParameterExecute", True) 

			
			