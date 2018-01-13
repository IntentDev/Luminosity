import copy

class UI(object):

	def __init__(self, type):

		self.type = type

	def StoreValue(self, gadget, valueType, value):

		name = gadget.fetch('attr')['name']
		compPar = op(gadget.fetch('StoreComp')).fetch('CompPar')
		compPar['values'][name][valueType] = value

	# call this function in gadget Lc functions to enable controller talk back
	# not fully implemented yet
	# see Slider().Lc() for usage
	def SendController(self, gadget, val):

		ctrlMaps = op(me.fetch('CTRL_MAPS'))
		allMaps = ctrlMaps.fetch('AllMaps')
		
		#if gadget.path in allMaps.keys():

		#	#print(gadget, val, allMaps[gadget.path] )

		
		
	def ExpandVal(self, low, high, value, format):

		value = ((high - low) * (value)) / 1 + low

		if format == 'integer':
			value = round(value)

		return value

	def NormalizeVal(self, low, high, value):

		return (value - low) / (high - low)

	def NormalizeValMod(self, low, high, value):

		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))

		return (value - low) / (high - low)

	def RangeVal(self, oLow, oHigh, nLow, nHigh, value, format):

		value = ((nHigh - nLow) * (value -oLow)) / (oHigh - oLow)  + nLow

		if format == 'integer':
			value = round(value)

		return value

	def SetRightClickMenu(self, path, setUIPath, resetVal, valueType, valueName, rename = False):
		rcMenu = op(me.fetch('RC_MENU'))
		rcMenu.Gadget().Open('Gadget', path, setUIPath, resetVal, valueType, valueName, rename = rename)

class Slider(UI):

	def __init__(self, field = True, valueType = 'value'):

		UI.__init__(self, "slider")
		self.field = field
		self.valueType = valueType

	def Roll(self, gadget, value):

		col = gadget.fetch('SLIDERCOL1')[value]
		par = gadget.par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def SlideKnob(self, gadget, value):

		knob = gadget.op('knob')
		knobWidth = knob.par.w
		parentWidth = gadget.par.w
	
		knob.par.x = max(min(value * parentWidth - knobWidth * .5, parentWidth - knobWidth - 2), 2,)

	def SlideKnobV(self, gadget, value):

		knob = gadget.op('knob')
		knobHeight = knob.par.h
		parentHeight = gadget.par.h
	
		knob.par.y = max(min(value * parentHeight - knobHeight * .5, parentHeight - knobHeight - 2), 2,)


	def Lc(self, gadget, value):

		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']

		val = gadget.ExpandVal(low, high, value, format)
		
		if self.field == True:
			if format == 'float':
				val = round(val, 3)
			else:
				val = round(val)
			gadget.parent().op('field/string')[0,0] = val
			gadget.parent().op('field/text').cook(force = True)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = val

		gadget.StoreValue(gadget, self.valueType, val)

		#print(gadget, parDest)

		#send assigned controller value on left click
		#gadget.SendController(gadget.parent(), val)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('../setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)


	def CtrlMap(self, gadget, value):
		
		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']

		value = gadget.ExpandVal(low, high, value, format)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)
		
class Field(UI):

	def __init__(self, slider = True, valueType = 'value'):

		UI.__init__(self, "field")
		self.slider = slider
		self.valueType = valueType

	def Roll(self, gadget, value):

		col = gadget.fetch('FIELDCOL1')[value]
		par = gadget.parent().par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

		col = gadget.fetch('FONTCOL1')[value]
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]


	def Focus(self, gadget, value):

		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']
		
		if self.slider == True:

			position = gadget.NormalizeVal(low, high, value)

			gadget.parent().op('slider').panel.u = position
			gadget.parent().op('slider').panel.trueu = position
			gadget.parent().op('slider').store('InitU', position)
			gadget.parent().op('slider').store('PrevU', position)
			
			gadget.parent().op('slider/setKnob').run()

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

class Button(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "button")
		self.valueType = valueType

	def RollOffToOn(self, gadget):

		panel = gadget.panel
		roll = panel.rollover
		lselect = panel.lselect

		index = roll + lselect

		col = gadget.fetch('BUTTONCOL1')[index]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]
		
		col = gadget.fetch('FONTCOL1')[index]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def RollOnToOff(self, gadget):

		panel = gadget.panel
		state = panel.state

		col = gadget.fetch('BUTTONCOL1')[int(state) * 2]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]


		col = gadget.fetch('FONTCOL1')[int(state) * 2]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def Lc(self, gadget, value):

		attr = gadget.fetch('attr')
		name = attr['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget, rename = False):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('../setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name, rename = rename)

	def CtrlMap(self, gadget, value):

		attr = gadget.fetch('attr')
		name = attr['name']

		value = round(value)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

class Knob(UI):

	def __init__(self, field = True, valueType = 'value'):

		UI.__init__(self, "slider")
		self.field = field
		self.valueType = valueType

	def Roll(self, gadget, value):

		col = gadget.fetch('SLIDERCOL1')[value]
		par = gadget.par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def Lc(self, gadget):

		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']

		u = gadget.panel.trueu.val
		v = gadget.panel.truev.val
	
		nLow = -50
		nHigh = 230

		angle = math.degrees(math.atan2(u,v)) + 100	
		angle = min(nHigh, max(nLow, angle))
			
		val = gadget.RangeVal(nLow, nHigh, low, high, angle, float)

		gadget.op('over1').par.r = angle

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = val

		gadget.StoreValue(gadget, self.valueType, val)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('../setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)


	def CtrlMap(self, gadget, value):
		
		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']

		value = gadget.ExpandVal(low, high, value, format)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

class ModOnButton(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "button")
		self.valueType = valueType

	def RollOffToOn(self, gadget):

		panel = gadget.panel
		roll = panel.rollover
		lselect = panel.lselect

		index = roll + lselect

		col = gadget.fetch('BUTTONCOL1')[index]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]
		
		col = gadget.fetch('FONTCOL1')[index]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def RollOnToOff(self, gadget):

		panel = gadget.panel
		state = panel.state

		col = gadget.fetch('BUTTONCOL1')[int(state) * 2]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]


		col = gadget.fetch('FONTCOL1')[int(state) * 2]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def Lc(self, gadget, value):

		attr = gadget.fetch('attr')
		name = attr['name']

		colors = [gadget.fetch('FONTCOL1')[0], gadget.fetch('FONTCOL2')[0]]
		
		col = colors[value]
		
		par = gadget.op('mod/text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]


		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.op('modUI/active/button').StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		resetVal = {'modOn': 0}
		setUIPath = gadget.op('../setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, 'modOn', name)

	def CtrlMap(self, gadget, value):

		#attr = gadget.fetch('attr')
		parentGadget = gadget.parent(2)
		name = parentGadget.fetch('attr')['name']

		colors = [gadget.fetch('FONTCOL1')[0], gadget.fetch('FONTCOL2')[0]]
		
		value = round(value)

		col = colors[value]
		
		par = gadget.parent(3).op('mod/text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

		

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(parentGadget, self.valueType, value)

class ModDisp(UI):

	def __init__(self):

		UI.__init__(self, "modDisp")

	def RollOffToOn(self, gadget):


		panel = gadget.panel
		roll = panel.rollover
		lselect = panel.lselect

		index = roll + lselect

		col = gadget.fetch('BUTTONCOL1')[index]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]
		
		name = gadget.fetch('attr')['name']
		compPar = op(gadget.fetch('StoreComp')).fetch('CompPar')
		modState = compPar['values'][name]['modOn']	
		
		colModOff = gadget.fetch('FONTCOL1')
		colModOn = gadget.fetch('FONTCOL2')
		colors = [colModOff, colModOn]
		
		col = colors[modState][index]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def RollOnToOff(self, gadget):

		panel = gadget.panel
		state = panel.state

		col = gadget.fetch('BUTTONCOL1')[int(state) * 2]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

		name = gadget.fetch('attr')['name']
		compPar = op(gadget.fetch('StoreComp')).fetch('CompPar')
		modState = compPar['values'][name]['modOn']
		
		colModOff = [gadget.fetch('FONTCOL1')[0], gadget.fetch('FONTCOL1')[2]]
		colModOn = [gadget.fetch('FONTCOL2')[0], gadget.fetch('FONTCOL2')[2]]	
		colors = [colModOff, colModOn]
		
		col = colors[modState][state]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]

	def Lc(self, gadget):

		state = gadget.panel.state
		
		name = gadget.fetch('attr')['name']
		compAttr = op(gadget.fetch('StoreComp')).fetch('CompAttr')
		compAttr['uiAttr'][name]['displayMod'] = int(state)

	def Rc(self, gadget):
		pass
		#print('Right Click   ' + gadget.path)

class ModGainOffsetSlider(UI):

	def __init__(self, field = True, valueType = 'value'):

		UI.__init__(self, "modGainSlider")
		self.field = field
		self.valueType = valueType

	def Roll(self, gadget, value):

		col = gadget.fetch('SLIDERCOL1')[value]
		par = gadget.par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def SlideKnob(self, gadget, value):

		knob = gadget.op('knob')
		knobWidth = knob.par.w
		parentWidth = gadget.par.w
	
		knob.par.x = max(min(value * parentWidth - knobWidth * .5, parentWidth - knobWidth - 2), 2,)

	def Lc(self, gadget, value, parm):

		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']

		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))

		value = gadget.op('modUI/'+ parm +'/slider').ExpandVal(low, high, value, format)
		
		if self.field == True:
			gadget.op('modUI/'+ parm +'/field/string')[0,0] = round(value,2)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.op('modUI/'+ parm +'/slider').StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget, parm):

		attr = gadget.fetch('attr')
		name = attr['name']


		if parm == 'gain':
			nValueType = 'modGain'
			resetVal = {nValueType: attr['rangeHigh']}
			
		else:
			nValueType = 'modOffset'
			resetVal = {nValueType: 0}

		setUIPath =gadget.op('modUI/'+ parm +'/slider/setUI')

		#gadget.op('modUI/'+ parm +'/slider').SetRightClickMenu(gadget.op('modUI/'+ parm +'/slider').path, setUIPath, resetVal, nValueType, name)

	def CtrlMap(self, gadget, value):
		
		parentGadget = gadget.parent(2)
		name = parentGadget.fetch('attr')['name']
		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		
		format = attr['format']

		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))

		value = gadget.ExpandVal(low, high, value, format)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(parentGadget, self.valueType, value)

class ModGainOffsetField(UI):

	def __init__(self, slider = True, valueType = 'value'):

		UI.__init__(self, "modGainOffsetField")
		self.slider = slider
		self.valueType = valueType

	def Roll(self, gadget, value):

		col = gadget.fetch('FIELDCOL1')[value]
		par = gadget.parent().par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

		col = gadget.fetch('FONTCOL1')[value]
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]


	def Focus(self, gadget, value, parm):

		attr = gadget.fetch('attr')
		low = attr['rangeLow']
		high = attr['rangeHigh']
		name = attr['name']
		format = attr['format']
		
		low = -max(abs(low),abs(high))
		high = max(abs(low),abs(high))

		field = gadget.op('modUI/'+ parm +'/field')
		slider = gadget.op('modUI/'+ parm +'/slider')

		if self.slider == True:

			position = field.NormalizeVal(low, high, value)

			slider.panel.u = position
			slider.op('setKnob').run()

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		field.StoreValue(gadget, self.valueType, value)

class Droplist(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "dropList")
		self.valueType = valueType


	def Reset(self, gadget):

		gadget.panel.v = 0
		gadget.panel.v = 1

	def Lc(self, gadget):
		##print('Left Click Droplist')
		dlGlobal = op(me.fetch('DROPLIST_GLOBAL'))
		droplist = dlGlobal.op('dropContainer/list')
		value = int(droplist.panel.celloverid)
		
		if value != -1:
			
			item = str(droplist.op('labels')[value,0])
			gadget.op('dropButton/button/button/text').par.text = item

			win = dlGlobal.op('window')
			win.par.winclose.pulse()

			name = gadget.fetch('attr')['name']

			parDest = gadget.fetch('Parameters')
			parDest[name, self.valueType] = value
		
			gadget.StoreValue(gadget, self.valueType, value)

	def TrigOpen(self, gadget):

		#print('Droplist Trigger Open')

		dlGlobal = op(me.fetch('DROPLIST_GLOBAL'))
		dlGlobal.store('Gadget', gadget)
		dlGlobal.store('ValueType', self.valueType)

		win = dlGlobal.op('window')
		drop = dlGlobal.op('dropContainer')		
		opened = win.isOpen

		
		itemTable = gadget.op(gadget.op('selectItems').par.dat.val).path 

		dlGlobal.op('selectItems').par.dat = itemTable
		
		maxHeight = int(gadget.op('maxDropHeight')[0,0].val)
		btnHeight = gadget.op('dropButton').par.h

		compH = op(itemTable).numRows * btnHeight
		##print(maxHeight, compH)

		height = min(maxHeight, compH)
		width = max(120, gadget.op('dropButton/button').par.w.val)


		#print(width)
		dlGlobal.op('dropContainer').par.w = width
		if dlGlobal.op('dropContainer/scroll').par.display.val == 1:
			w2 = width - dlGlobal.op('dropContainer/scroll').par.w.val
			dlGlobal.op('dropContainer/list').par.w = w2
			dlGlobal.op('dropContainer/scroll').par.x = w2
		else:
			dlGlobal.op('dropContainer/list').par.w = width

		dlGlobal.op('dropContainer').par.h = height
		

		#settings = {'width': width, 'height': btnHeight, 'labelWidth': 0, 'scrollWidth': 12,
		# 'listHeight': 140, 'label': 'Droplist', 'itemTable': itemTable, 'labelOn': False}
		#mod.uiSetup.DropListGlobal(dlGlobal.path, settings)

		if opened == False:
		
			#gadget.op('getMouse').run()	
			#absMouseY = gadget.op('mouseY')[0,0]
			absMouseY = op(gadget.fetch('MASTERABSMOUSE'))['ty'].eval()

			buttonHeight = gadget.op('dropButton').par.h

			dropWidth = width
			dropHeight = height
		
			mouseX = gadget.panel.insideu * gadget.par.w
			mouseY = gadget.panel.insidev * gadget.par.h
			#controlsScrollWidth = dlGlobal.op('dropContainer/scroll').par.w + 1

			if gadget.parent().name == 'controls':

				controlsScrollWidth = gadget.parent().op('scroll').par.w.val
			else:
				controlsScrollWidth = 0

			x =  dropWidth - mouseX - .5 * dropWidth + (gadget.par.w  - controlsScrollWidth - dropWidth) 
		
			if absMouseY >= dropHeight + buttonHeight:	
				y = - dropHeight * 0.5 - mouseY
		
			else:	
				y = dropHeight * 0.5 + (gadget.par.h - mouseY) 
			

			win.par.winoffsetx = x
			win.par.winoffsety = y
			win.par.winopen.pulse()
			#dlGlobal.op('winOpen').run(x, y, delayFrames = 0)

			drop.setFocus()

		else:
			win.par.winclose.pulse()
		
			
	def ChangeHeight(self, gadget):
		#print('Change Droplist Height')
		refGadget = gadget.fetch('Gadget')

		droplist = gadget.op('list')
		scroll = gadget.op('scroll')


		compH = gadget.op('in1').numRows * refGadget.op('dropButton').par.h
		maxHeight = int(refGadget.op('maxDropHeight')[0,0].val)
	
		parentW = int(gadget.par.w)

		parentH = min(compH,maxHeight)
		gadget.par.h = parentH
		compW = parentW - scroll.par.w if parentH < compH else parentW

		droplist.par.w = compW
		droplist.par.h = compH

		dispScroll = 1 if parentH < compH else 0

		gadget.parent().store('DispScroll', dispScroll)
		gadget.parent().store('ListHeight', compH)
		gadget.parent().store('WindowHeight', parentH)

		gadget.store('CompHeight', compH)
		gadget.store('CompWidth', compW)
		
		scroll.par.h = parentH - 2
		scroll.op('slider').par.h = parentH - 2
		scroll.par.display = dispScroll

		slider = scroll.op('slider')
		sliderH = slider.par.h
		knobHeight = min(sliderH,max(16, sliderH - (gadget.fetch('CompHeight') - sliderH)))

		knob = slider.op('knob')

		knob.par.h = knobHeight
		knob.par.y = max(min(sliderH - knobHeight * 0.5, sliderH - knobHeight - 1), 1)

		scroll.par.x = parentW - scroll.par.w

		self.Reset(slider)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)

	def CtrlMapList(self, gadget, nIndex):
		
		droplist = gadget.op('dropContainer/list')
		items = gadget.op('selectItems')
		length = items.numRows

		value = int(nIndex * (length - 1))
		item = str(items[value,0])
		##print(value)
		gadget.op('dropButton/button/button/text').par.text = item

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)		

	def SetValSetUI(self, gadget, index):
		
		droplist = gadget.op('dropContainer/list')
		items = gadget.op('selectItems')

		item = items[index, 0].val
		gadget.op('dropButton/button/button/text').par.text = item

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = index
	
		gadget.StoreValue(gadget, self.valueType, index)	

		gadget.op('dropButton/button/button/text').par.text = item

	def ListLengthChange(self, gadget):

		itemsList = [r[0].val for r in gadget.op('selectItems').rows()]
		curItem = gadget.op('dropButton/button/button/text').par.text.val
		if curItem in itemsList: index = itemsList.index(curItem)
		else: index = 0

		self.SetValSetUI(gadget, index)

class DroplistMod(UI):

	def __init__(self, ownerComp, valueType = 'value'):

		UI.__init__(self, "dropList")
		self.valueType = valueType
		self.ownerComp = ownerComp

	def Reset(self, gadget):

		gadget.panel.v = 0
		gadget.panel.v = 1

	def Lc(self, gadget):
		
		
		dlGlobal = op(me.fetch('DROPLIST_GLOBAL'))
		droplist = dlGlobal.op('dropContainer/list')

		value = int(droplist.panel.celloverid)

		if value != -1:
			item = str(droplist.op('labels')[value,0])
			gadget.op('dropButton/button/button/text').par.text = item

			win = dlGlobal.op('window')
			win.par.winclose.pulse()

			name = gadget.fetch('attr')['name']

			parDest = gadget.fetch('Parameters')
			parDest[name, self.valueType] = value
		
			gadget.StoreValue(gadget, self.valueType, value)


	def TrigOpen(self, gadget):

		dlGlobal = op(me.fetch('DROPLIST_GLOBAL'))
		dlGlobal.store('Gadget', gadget)
		dlGlobal.store('ValueType', self.valueType)

		win = dlGlobal.op('window')
		drop = dlGlobal.op('dropContainer')		
		opened = win.isOpen

		#attr = gadget.fetch('attr')
		itemTable = gadget.op(gadget.op('selectItems').par.dat.val).path 
		
		dlGlobal.op('selectItems').par.dat = itemTable
		
		maxHeight = int(gadget.op('maxDropHeight')[0,0].val)
		compH = op(itemTable).numRows * gadget.op('dropButton').par.h
		height = min(maxHeight, compH)
		width = gadget.op('dropButton/button').par.w.val

		dlGlobal.op('dropContainer').par.w = width
		dlGlobal.op('dropContainer').par.h = height

		if opened == False:
		
			#gadget.op('getMouse').run()	
			#absMouseY = gadget.op('mouseY')[0,0]
			absMouseY = op(gadget.fetch('MASTERABSMOUSE'))['ty'].eval()

			buttonHeight = gadget.op('dropButton').par.h

			dropWidth = width
			dropHeight = height
		
			mouseX = gadget.panel.insideu * gadget.par.w
			mouseY = gadget.panel.insidev * gadget.par.h
			controlsScrollWidth = dlGlobal.op('dropContainer/scroll').par.w + 1

			x =  dropWidth - mouseX - .5 * dropWidth + (gadget.par.w - dropWidth) + 8
		
			if absMouseY >= dropHeight + buttonHeight:	
				y = - dropHeight * 0.5 - mouseY
		
			else:	
				y = dropHeight * 0.5 + (gadget.par.h - mouseY) 
			

			win.par.winoffsetx = x
			win.par.winoffsety = y
			win.par.winopen.pulse()
			#dlGlobal.op('winOpen').run(x, y, delayFrames = 0)

		else:
	
			win.par.winclose.pulse()

	def ChangeHeight(self, gadget):

		refGadget = gadget.fetch('Gadget')

		droplist = gadget.op('list')
		scroll = gadget.op('scroll')


		compH = gadget.op('in1').numRows * refGadget.op('dropButton').par.h
		maxHeight = int(refGadget.op('maxDropHeight')[0,0].val)
	
		parentW = int(gadget.par.w)

		parentH = min(compH,maxHeight)
		gadget.par.h = parentH
		compW = parentW - scroll.par.w if parentH < compH else parentW

		droplist.par.w = compW
		droplist.par.h = compH

		dispScroll = 1 if parentH < compH else 0

		gadget.parent().store('DispScroll', dispScroll)
		gadget.parent().store('ListHeight', compH)
		gadget.parent().store('WindowHeight', parentH)


		gadget.store('CompHeight', compH)
		gadget.store('CompWidth', compW)

		
		scroll.par.h = parentH - 2
		scroll.op('slider').par.h = parentH - 2
		scroll.par.display = dispScroll



		#scroll.op('slider/setHeight').run()
		slider = scroll.op('slider')
		sliderH = slider.par.h
		knobHeight = min(sliderH,max(16, sliderH - (gadget.fetch('CompHeight') - sliderH)))

		knob = slider.op('knob')

		knob.par.h = knobHeight
		knob.par.y = max(min(sliderH - knobHeight * 0.5, sliderH - knobHeight - 1), 1)

		
		#scroll.op('reset').run()
		self.Reset(slider)
		#slider.panel.v = 0
		#slider.panel.v = 1

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)

	def CtrlMap(self, nIndex):
		gadget = self.ownerComp
		droplist = gadget.op('dropContainer/list')
		items = gadget.op('selectItems')
		length = items.numRows

		value = int(nIndex * (length - 1))
		item = str(items[value,0])
		##print(value)
		gadget.op('dropButton/button/button/text').par.text = item

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

	def SetValSetUI(self, gadget, index):
		
		droplist = gadget.op('dropContainer/list')
		items = gadget.op('selectItems')

		item = items[index, 0].val
		gadget.op('dropButton/button/button/text').par.text = item

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = index
	
		gadget.StoreValue(gadget, self.valueType, index)	

		gadget.op('dropButton/button/button/text').par.text = item

	def ListLengthChange(self, gadget):

		itemsList = [r[0].val for r in gadget.op('selectItems').rows()]
		curItem = gadget.op('dropButton/button/button/text').par.text.val
		if curItem in itemsList: index = itemsList.index(curItem)
		else: index = 0

		self.SetValSetUI(gadget, index)

class RadioButton(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def Lc(self, gadget, value):
		
		#value = int(gadget.panel.cellradioid)

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)

	def CtrlMap(self, gadget, radioId):

		name = gadget.fetch('attr')['name']

		length = gadget.op('selectItems').numRows

		value  = math.floor(radioId * (length - 1))

		gadget.panel.cellradioid = value
		gadget.op('cellId')[0,0] = value

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

class Buttons(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def Lc(self, gadget, value):
		
		#value = int(gadget.panel.cellradioid)

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name)

	def CtrlMap(self, gadget, radioId):

		name = gadget.fetch('attr')['name']

		length = gadget.op('selectItems').numRows

		value  = math.floor(radioId * (length - 1))

		gadget.panel.cellradioid = value
		gadget.op('cellId')[0,0] = value

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

class Timecode(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def FocusOff(self, gadget, value):
		
		#value = int(gadget.panel.cellradioid)
		#print(value, type(value))

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

class MultiButton(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def Lc(self, gadget, value):
		
		#value = int(gadget.panel.cellradioid)

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):
		pass
		#print('Right Click   ' + gadget.path)

	def CtrlMap(self, gadget, value, radioId):

		name = gadget.fetch('attr')['name']

		radioId = value * (radioId + 1) - 1

		gadget.panel.celloverid = radioId
		gadget.op('cellId')[0,0] = radioId
		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = radioId
	
		gadget.StoreValue(gadget, self.valueType, radioId)

class PresetsButton(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def Lc(self, gadget, value):
		
		#value = int(gadget.panel.cellradioid)

		name = gadget.fetch('attr')['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):
		pass
		#print('Right Click   ' + gadget.path)

	def CtrlMap(self, gadget, value, radioId):

		name = gadget.fetch('attr')['name']

		radioId = value * (radioId + 1) - 1

		gadget.panel.celloverid = radioId
		gadget.op('cellId')[0,0] = radioId
		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = radioId
	
		gadget.StoreValue(gadget, self.valueType, radioId)

class EffectSlots(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

	def Lc(self, gadget, value):
		
		attr = gadget.fetch('attr')
		#itemTable = attr['itemTable']
		#slot = op(itemTable)[value + 1,'slot']

		channel = gadget.fetch('Channel')
		dataSlotPath = channel +'/effects/slot' + str(value)
		slotOp = op(dataSlotPath)
		slotPlugin = slotOp.op('plugin')

		compAttr = slotPlugin.fetch('CompAttr')
		compPar = slotPlugin.fetch('CompPar')
		compPresets = slotPlugin.fetch('CompPresets')

		slotType = compAttr['attr']['type']
		curUIPath = slotOp.op('controls')

		UISelectPath = gadget.fetch('UISelectPath')
		curPrevUIPath = op(UISelectPath + '/curPrevUIPath')
		prevUIPath = curPrevUIPath[0,0].val
		curPrevUIPath[1,0] = prevUIPath
		curPrevUIPath[0,0] = curUIPath

		prevCtrls = op(prevUIPath)
		curCtrls = op(curUIPath)

		if curUIPath != prevUIPath:
			
			if prevCtrls:	
				prevCtrls.store('IsDisplayed', 0)
				prevCtrls.Hide()

			op(UISelectPath +'/selectControls').par.selectpanel = curUIPath
			curCtrls.Display()

		#name = gadget.fetch('attr')['name']
		#parDest = gadget.fetch('Parameters')
		#parDest[name, self.valueType] = value
		#gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget):
		pass
		#print('Right Click   ' + gadget.path)

	def CtrlMapSet(self, gadget, radioId):

		name = gadget.fetch('attr')['name']

		length = gadget.op('selectItems').numRows

		value  = math.floor(radioId * (length - 1))

		gadget.panel.cellradioid = value

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value
	
		gadget.StoreValue(gadget, self.valueType, value)

class EffectSlotsState(UI):

	def __init__(self, valueType = 'state'):

		UI.__init__(self, "radioButton")
		self.valueType = valueType

		self.slots = ['slot0', 'slot1', 'slot2', 'slot3', 'slot4', 'slot5']

	def Lc(self, gadget, cellid, value):
		
		attr = gadget.fetch('attr')
		name = attr['name']
		itemTable = op(attr['itemTable'])
		#print(name)

		itemTable[cellid + 1, 'state'] = value
		
		compPar = op(gadget.fetch('StoreComp')).fetch('CompPar')
		compPar['values'][name]['slot' + str(cellid)]['state'] = value

		states = [compPar['values'][name][key]['state'] for key in self.slots]
		parDest = gadget.fetch('Parameters')
		parDest[name, 'value'] = states

		compPar['values'][name]['value'] = states

	def Rc(self, gadget):
		pass
		#print('Right Click   ' + gadget.path)

	def CtrlMapSet(self, gadget, cellId):

		name = gadget.fetch('attr')['name']

		length = gadget.op('selectItems').numRows

		value  = math.floor(cellId * (length - 1))

		attr = gadget.fetch('attr')
		name = attr['name']
		itemTable = op(attr['itemTable'])

		itemTable[value + 1, 'state'] = value
		
		compPar =op(gadget.fetch('StoreComp')).fetch('CompPar')
		compPar['values'][name]['slot' + str(value)]['state'] = value

		states = [compPar['values'][name][key]['state'] for key in self.slots]
		parDest = gadget.fetch('Parameters')
		parDest[name, 'value'] = states

		compPar['values'][name]['value'] = states

class CheckBox(UI):

	def __init__(self, valueType = 'value'):

		UI.__init__(self, "button")
		self.valueType = valueType

	def RollOffToOn(self, gadget):

		panel = gadget.panel
		roll = panel.rollover.val


		col = gadget.fetch('BUTTONCOL1')[roll]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]
		
		'''
		col = gadget.fetch('FONTCOL1')[index]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]
		'''

	def RollOnToOff(self, gadget):

		panel = gadget.panel
		roll = panel.rollover.val


		col = gadget.fetch('BUTTONCOL1')[roll]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

		'''
		col = gadget.fetch('FONTCOL1')[int(state) * 2]
		
		par = gadget.op('text').par

		par.fontcolorr = col[0]
		par.fontcolorg = col[1]
		par.fontcolorb = col[2]
		par.fontalpha = col[3]
		'''

	def Lc(self, gadget, value):

		attr = gadget.fetch('attr')
		name = attr['name']

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

	def Rc(self, gadget, rename = False):

		attr = gadget.fetch('attr')
		name = attr['name']
		default = attr['default']
		resetVal = {self.valueType: default}
		setUIPath = gadget.op('../setUI')

		gadget.SetRightClickMenu(gadget.path, setUIPath, resetVal, self.valueType, name, rename = rename)

	def CtrlMap(self, gadget, value):

		attr = gadget.fetch('attr')
		name = attr['name']

		value = round(value)

		parDest = gadget.fetch('Parameters')
		parDest[name, self.valueType] = value

		gadget.StoreValue(gadget, self.valueType, value)

class Scroll(UI):

	def __init__(self):

		UI.__init__(self, "scroll")

	def Roll(self, gadget, value):

		col = gadget.fetch('KNOBCOL1')[value]
		par = gadget.op('knob').par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def SlideKnob(self, gadget, value):

		knob = gadget.op('knob')
		knobWidth = knob.par.w
		parentWidth = gadget.par.w
	
		knob.par.x = max(min(value * parentWidth - knobWidth * .5, parentWidth - knobWidth - 2), 2,)

	def Lc(self, gadget, viewWindow, fullWindow, value, offset = 0):
		knob = gadget.op('slider/knob')
		sliderH = gadget.op('slider').par.h
		knobHeight = knob.par.h
		
		knob.par.y = max(min(value * sliderH - knobHeight*.5, sliderH - knobHeight - 1), 1)
		knobHeight = knob.par.h * .5
		
		fullHeight = fullWindow.par.h 
		winHeight = gadget.fetch('WindowHeight')
					
		pos = 0.0
			
		scale = winHeight - fullHeight
		knobScaled = scale - knobHeight * 2
		

		if fullHeight > winHeight:
			
			pos =  (value) * knobScaled + knobHeight		
			pos = max(min(pos,0),scale )

		else:

			pos = scale
			
		fullWindow.par.y = pos + offset

	def TrigMcScrollOn(self, gadget):

		if gadget.fetch('DispScroll') == True:

			gadget.op('mcScroll').par.active = True

	def TrigMcScrollOff(self, gadget):

		gadget.op('mcScroll').par.active = False

	def McScrollOn(self, gadget, fullWindow, offset = 0):

		knobH = gadget.op('slider/knob').par.h
		listH = gadget.fetch('ListHeight')
		windowH = gadget.fetch('WindowHeight')

		initV = op(gadget.fetch('MASTERMOUSE'))['ty'].eval()
		initPos = fullWindow.par.y - offset
		
		t = gadget.op('mScroll')
		t['initV', 1] = initV
		t['pos', 1] = initPos
	
	def McScroll(self, gadget, fullWindow, offset = 0):

		knob = gadget.op('slider/knob')
		knobH = knob.par.h
		listH = gadget.fetch('ListHeight')
		windowH = gadget.fetch('WindowHeight')

		minPos = windowH - listH
			
		t = gadget.op('mScroll')
		initV = t['initV',1]
		pos = t['pos',1]
		curV = op(gadget.fetch('MASTERMOUSE'))['ty'].eval()
				
		relV = curV - initV
		
		relV = min(max(-.2,relV),0.2) * -200
		pos += relV 
		
		pos = min(max(pos,minPos),0)
		t['pos',1] = pos	
		
		try:
			normPos = pos / -minPos
		except:
			normPos = 0.0
					
		knob.par.y = 1 + abs(normPos * (windowH - 4 - knobH))
		
		fullWindow.par.y = pos + offset

class ScrollH(UI):

	def __init__(self):

		UI.__init__(self, "scrollH")

	def Roll(self, gadget, value):

		col = gadget.fetch('KNOBCOL1')[value]
		par = gadget.op('knob').par
		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def Lc(self, gadget, viewWindow, fullWindow, value, offset = 0):

		knob = gadget.op('slider/knob')
		sliderW = gadget.op('slider').par.w
		knobWidth = knob.par.w
		
		knob.par.x = max(min(value * sliderW - knobWidth*.5, sliderW - knobWidth - 1), 1)
		knobWidth = knob.par.w * .5
		
		fullWidth = fullWindow.par.w 
		winWidth = gadget.fetch('WindowWidth')
					
		pos = 0.0
			
		scale = winWidth - fullWidth
		knobScaled = scale - knobWidth * 2
		
		if fullWidth > winWidth:

			pos =  (value) * knobScaled + knobWidth		
			pos = max(min(pos,0),scale )

		else:

			pos = scale
					
		fullWindow.par.x = pos + offset

	def TrigMcScrollOn(self, gadget):

		if gadget.fetch('DispScroll') == True:

			gadget.op('mcScroll').par.active = True

	def TrigMcScrollOff(self, gadget):

	
		gadget.op('mcScroll').par.active = False

	def McScrollOn(self, gadget, fullWindow, offset = 0):

		knobW = gadget.op('slider/knob').par.w
		listW = gadget.fetch('ListWidth')
		windowW = gadget.fetch('WindowWidth')

		initU = op(gadget.fetch('MASTERMOUSE'))['tx'].eval()	
		initPos = fullWindow.par.x - offset
		
		t = gadget.op('mScroll')
		t['initU', 1] = initU
		t['pos', 1] = initPos
	
	def McScroll(self, gadget, fullWindow, offset = 0):

		knob = gadget.op('slider/knob')
		knobW = knob.par.w
		listW = gadget.fetch('ListWidth')
		windowW = gadget.fetch('WindowWidth')

		minPos = windowW - listW
			
		t = gadget.op('mScroll')
		initU = t['initU',1]
		pos = t['pos',1]
		#curU = gadget.op('mousein')['tx'].eval()
		curU = op(gadget.fetch('MASTERMOUSE'))['tx'].eval()		

		relU= curU - initU
		
		relU = min(max(-.2,relU),0.2) * -200
		pos += relU
		
		pos = min(max(pos,minPos), 0)
		t['pos',1] = pos	
		
		try:
			normPos = pos / -minPos
		except:
			normPos = 0.0
		
		knob.par.x = 1 + abs(normPos * (windowW - 4 - knobW))
		
		fullWindow.par.x = pos + offset


	def Midi(self, gadget, viewWindow, fullWindow, value, step, offset = 0):

		knob = gadget.op('slider/knob')
		sliderW = gadget.op('slider').par.w
		knobWidth = knob.par.w
		
		fullWidth = fullWindow.par.w 
		winWidth = gadget.fetch('WindowWidth')
		scale = winWidth - fullWidth
		knobPos = ((value * step)/3) / winWidth
		knob.par.x = max(min(knobPos * sliderW - knobWidth*.5, sliderW - knobWidth - 1), 1)


		'''
		knobWidth = knob.par.w * .5
		
		fullWidth = fullWindow.par.w 
		winWidth = gadget.fetch('WindowWidth')
				
		pos = 0.0
			
		scale = winWidth - fullWidth
		knobScaled = scale - knobWidth * 2
		
		if fullWidth > winWidth:

			pos =  (value) * knobScaled + knobWidth		
			pos = max(min(pos,0),scale )

		else:

			pos = scale
		'''
		pos = max(-value * step, scale)

		fullWindow.par.x = pos + offset
	
class ButtonCtrlMapSet(UI):

	def __init__(self, valueType = 'address'):

		UI.__init__(self, "button")
		self.valueType = valueType

	def RollOffToOn(self, gadget):

		panel = gadget.panel
		roll = panel.rollover
		lselect = panel.lselect

		index = roll + lselect

		col = gadget.fetch('CTRL_MAP_COL')[index]

		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]		

	def RollOnToOff(self, gadget):

		panel = gadget.panel
		state = panel.state

		col = gadget.fetch('RollOffCol')
		par = gadget.par

		par.bgcolorr = col[0]
		par.bgcolorg = col[1]
		par.bgcolorb = col[2]
		par.bgalpha = col[3]

	def Lc(self, gadgetPath, ctrlsPath):
	
		ctrlMaps = op(op(gadgetPath).fetch('CTRL_MAPS'))
		ctrlMaps.op('setState').run(gadgetPath, ctrlsPath)

	def Rc(self, gadgetPath, ctrlsPath):

		ctrlMaps = op(op(gadgetPath).fetch('CTRL_MAPS'))
		ctrlMaps.op('delMap').run(gadgetPath, ctrlsPath)

class RightClickMenu(UI):

	def __init__(self, valueType = 'none'):

		UI.__init__(self, "rcMenu")
		self.valueType = valueType

	def Lc(self, rcMenu, command):
		
		#value = int(gadget.panel.cellradioid)

		gadgetPath = rcMenu.fetch('GadgetPath')
		setUIPath = rcMenu.fetch('SetUIPath')
		resetVal = rcMenu.fetch('ResetVal')
		valueType = rcMenu.fetch('ValueType')
		valueName = rcMenu.fetch('ValueName')

		gadget = op(gadgetPath)
		gadgetParent = gadget.parent().path

		if command == 'reset':

			parDest = gadget.fetch('Parameters')
			if parDest[valueName, valueType] != None:
				parDest[valueName, valueType] = resetVal[valueType]

			#print(resetVal)
			#print(valueType)
				gadget.StoreValue(gadget, valueType, resetVal[valueType])

				setUI = op(setUIPath)
				setUI.run(resetVal)

