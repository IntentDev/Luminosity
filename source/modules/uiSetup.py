def ValSlider(path, settings):
	
	width = settings['width']
	height = settings['height']
	fieldWidth = settings['fieldWidth']
	labelWidth = settings['labelWidth']
	scrollWidth = settings['scrollWidth']
	label = settings['label']
	format = settings['format']

	
	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	sliderCol = me.fetch('SLIDERCOL1')
	knobCol = me.fetch('KNOBCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]


	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	sliderWidth = width - fieldWidth - scrollWidth - 2 - 4
	sliderSettings = {'width': sliderWidth, 'height': height , 'sliderCol': sliderCol, 'knobCol': knobCol}
	
	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}
	
	fieldSettings = {'width': fieldWidth, 'height': height, 'fontCol': fontCol, 'fontWidth': fontWidth, 
	'format': format}

	op(path + '/slider/setup').run(sliderSettings, labelSettings)
	op(path + '/field/setup').run(fieldSettings)

def ValSliderV(path, settings):
	
	width = settings['width']
	height = settings['height']
	fieldHeight = 20
	labelHeight = settings['labelWidth']
	scrollHeight = settings['scrollHeight']
	label = settings['label']
	format = settings['format']

	
	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	sliderCol = me.fetch('SLIDERCOL1')
	knobCol = me.fetch('KNOBCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]


	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	field = o.op('field')
	field.par.y = o.par.h - fieldHeight + 2

	#slider = o.op('sliderV')
	#slider.par.y = scrollHeight + 2

	sliderHeight = height - fieldHeight - 2
	sliderSettings = {'width': width, 'height': sliderHeight , 'sliderCol': sliderCol, 'knobCol': knobCol}
	
	labelSettings = {'labelWidth': labelHeight, 'height': fieldHeight, 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}
	
	fieldSettings = {'width': width - 4, 'height': fieldHeight, 'fontCol': fontCol, 'fontWidth': fontWidth, 
	'format': format}

	op(path + '/slider/setup').run(sliderSettings, labelSettings)
	op(path + '/field/setup').run(fieldSettings)

def ValSliderM(path, settings):
	
	width = settings['width']
	height = settings['height']
	fieldWidth = settings['fieldWidth']
	labelWidth = settings['labelWidth']
	scrollWidth = settings['scrollWidth']
	label = settings['label']
	format = settings['format']
	
	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	sliderCol = me.fetch('SLIDERCOL1')
	knobCol = me.fetch('KNOBCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	o.store('GadgetHeight', height)

	modOpenWidth = height - 4
	sliderWidth = width - fieldWidth - scrollWidth - 2 - modOpenWidth - 6

	o.op('modField').par.w = fieldWidth + modOpenWidth + 4
	o.op('modField').par.h = height

	sliderSettings = {'width': sliderWidth, 'height': height , 'sliderCol': sliderCol, 'knobCol': knobCol}
	
	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}
	
	fieldSettings = {'width': fieldWidth, 'height': height, 'fontCol': fontCol, 'fontWidth': fontWidth, 
	'format': format}

	modOpenSettings = {'width': modOpenWidth, 'height': modOpenWidth, 'fontCol': fontCol, 'fontWidth': fontWidth, 
	'format': 'toggledown', 'label': 'M'}

	op(path + '/slider/setup').run(sliderSettings, labelSettings)
	op(path + '/field/setup').run(fieldSettings)
	op(path + '/mod/setup').run(modOpenSettings)
	op(path + '/modUI/setup').run(settings)

def SliderV(path, settings):
	
	width = settings['width']
	height = settings['height']
	labelHeight = settings['labelWidth']
	fieldHeight = 16
	scrollHeight = settings['scrollHeight']
	label = settings['label']
	format = settings['format']
	
	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	sliderCol = me.fetch('SLIDERCOL1')
	knobCol = me.fetch('KNOBCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	sliderHeight = height
	sliderSettings = {'width': width, 'height': sliderHeight , 'sliderCol': sliderCol, 'knobCol': knobCol}
	
	labelSettings = {'labelWidth': labelHeight, 'height': fieldHeight, 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}
	
	op(path + '/slider/setup').run(sliderSettings, labelSettings)

def Field(path, settings):
	
	width = settings['width']
	height = settings['height']
	labelWidth = settings['labelWidth']
	scrollWidth = settings['scrollWidth']
	label = settings['label']
	format = settings['format']

	
	gadgetCol = me.fetch('GADGETCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]


	gadget = op(path)
	par = gadget.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	ctrls = gadget.parent()
	attr = gadget.fetch('attr')
	ctrlsPars = [par.name for par in ctrls.customPars]

	if 'Numberfieldwidth' in ctrlsPars and attr['format'] != 'string':
		fieldWidth = ctrls.par.Numberfieldwidth.val
		labelWidth = width - fieldWidth - scrollWidth - 6

	elif 'Stringfieldwidth' in ctrlsPars and attr['format'] == 'string':
		fieldWidth = ctrls.par.Stringfieldwidth.val
		labelWidth = width - fieldWidth - scrollWidth - 6


	else:
		fieldWidth = width - labelWidth - scrollWidth - 6

	


	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}
	
	fieldSettings = {'width': fieldWidth, 'height': height, 'fontCol': fontCol, 'fontWidth': fontWidth, 
	'format': format}

	op(path + '/label/setup').run(labelSettings)
	op(path + '/field/setup').run(fieldSettings)

def Timecode(path, settings):
	
	width = settings['width']
	height = settings['height']
	labelWidth = 100
	scrollWidth = settings['scrollWidth']
	label = settings['label']
	#format = settings['format']

	
	gadgetCol = me.fetch('GADGETCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	par.marginr = scrollWidth + 4

	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}

	op(path + '/label/setup').run(labelSettings)

def Button(path, settings):

	width = settings['width']
	height = settings['height']
	scrollWidth = settings['scrollWidth']

	gadgetCol = me.fetch('GADGETCOL1')
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	settings['width'] = width 
	op(path + '/button/setup').run(settings)

def Buttons(path, settings):

	width = settings['width']
	height = settings['height']
	scrollWidth = settings['scrollWidth']
	items = settings['itemTable']
	labelWidth = settings['labelWidth']
	label = settings['label']
	

	gadgetCol = me.fetch('GADGETCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]

	gadget = op(path)
	par = gadget.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]


	radiodWidth = width - labelWidth - scrollWidth - 6

	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}

	op(path + '/label/setup').run(labelSettings)

	radio = gadget.op('radio')
	par = radio.par
	par.w = width - labelWidth- scrollWidth
	par.h = height
	par.x = labelWidth + 2

	radio.op('selectItems').par.dat = items
	cols = radio.op('selectItems').numRows
	par.tablecols = cols

def RadioButton(path, settings):

	width = settings['width']
	height = settings['height']
	scrollWidth = settings['scrollWidth']
	items = settings['itemTable']

	gadgetCol = me.fetch('GADGETCOL1')
	bgCol = gadgetCol[0]

	gadget = op(path)
	par = gadget.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	radio = gadget.op('radio')
	par = radio.par
	par.w = width - scrollWidth
	par.h = height

	radio.op('selectItems').par.dat = items
	cols = radio.op('selectItems').numRows
	par.tablecols = cols

def EffectSlots(path, settings):

	gadget = op(path)

	height = settings['height']
	items = settings['itemTable']
	width = gadget.parent().par.w - height

	gadgetCol = me.fetch('GADGETCOL1')
	bgCol = gadgetCol[0]
	
	par = gadget.par

	gadget.op('selectItems').par.dat = items
	selectItems = gadget.op('selectItems')
	rows = selectItems.numRows
	par.tablerows = rows

	par.w = width
	par.h = height * rows
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	storeComp = gadget.fetch('StoreComp')
	compPar = storeComp.fetch('CompPar')
	compPar['values'][gadget.parent().name]['value'] = 0
	i = 0

	for r in op(items).rows()[1:]:
		compPar['values'][gadget.parent().name]['slot' + str(i)] = {'name': r[1].val, 'state': int(r[2].val), 'path': r[3].val}
		i += 1
	
def ModUI(path, settings):
	
	width = settings['width']
	height = settings['height']
	fieldWidth = settings['fieldWidth']
	scrollWidth = settings['scrollWidth']


	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	sliderCol = me.fetch('SLIDERCOL1')
	knobCol = me.fetch('KNOBCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height * 2  + 2
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	sourcesWidth = 140

	sliderWidth = width - sourcesWidth - scrollWidth - 2

	gadgetSettings = settings
	gadgetSettings['width'] = width
	gadgetSettings['labelWidth'] = 60

	gainSettings = gadgetSettings
	gainSettings['label'] = 'Gain'
	gainSettings['scrollWidth'] = 0
	gainSettings['width'] = sliderWidth
	op(path + '/gain/setup').run(gainSettings)

	offsetSettings = gadgetSettings
	offsetSettings['label'] = 'Offset'
	offsetSettings['width'] = sliderWidth
	gainSettings['scrollWidth'] = 0
	op(path + '/offset/setup').run(offsetSettings)

	activeSettings = {'width': sourcesWidth, 'height': height, 'format': 'toggledown', 
	'label': 'Mod On', 'scrollWidth': scrollWidth}

	op(path + '/active/setup').run(activeSettings)
	sourcesSettings = gadgetSettings

	sourcesSettings['label'] = 'Sources'
	sourcesSettings['labelWidth'] =  60	
	sourcesSettings['scrollWidth'] = 12
	sourcesSettings['listHeight'] = 140
	sourcesSettings['width'] = sourcesWidth  + scrollWidth + 2
	op(path + '/sources/setup').run(sourcesSettings) 

def LabelCOMP(path, settings):

	lWidth = settings['labelWidth']
	height = settings['height']
	label = settings['label']
	align = settings['align']
	bgCol = settings['bgCol']
	fontCol = settings['fontCol'][0]
	fontWidth = settings['fontWidth']

	o = op(path)
	par = o.par
	par.w = lWidth
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	o = op(path + '/text')
	o.lock = False
	par = o.par
	par.text = label
	par.resolution1 = lWidth
	par.resolution2 = height

	par.fontcolorr = fontCol[0]
	par.fontcolorg = fontCol[1]
	par.fontcolorb = fontCol[2]
	par.fontalpha = fontCol[3]
	par.fontsizex = fontWidth
	par.alignx = align[0]
	par.aligny = align[1]

	o.lock = True
	o.cook(force = True)

def LabelVCOMP(path, settings):

	lWidth = settings['labelWidth']
	height = settings['height']
	label = settings['label']
	align = settings['align']
	bgCol = settings['bgCol']
	fontCol = settings['fontCol'][0]
	fontWidth = settings['fontWidth']

	o = op(path)
	par = o.par
	par.w = height
	par.h = lWidth
	par.x = (o.parent().par.w - height) * .5
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	o = op(path + '/text')
	o.lock = False
	par = o.par
	par.text = label
	par.resolution1 = lWidth
	par.resolution2 = height

	par.fontcolorr = fontCol[0]
	par.fontcolorg = fontCol[1]
	par.fontcolorb = fontCol[2]
	par.fontalpha = fontCol[3]
	par.fontsizex = fontWidth
	par.alignx = align[0]
	par.aligny = align[1]

	o.lock = True
	o.cook(force = True)	

def SliderCOMP(path, settings):

	width = settings['width']
	height = settings['height']
	bgCol = settings['sliderCol'][0]
	knobCol = settings['knobCol'][0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	o = op(path + '/knob')
	par = o.par
	par.h = height - 4
	par.bgcolorr = knobCol[0]
	par.bgcolorg = knobCol[1]
	par.bgcolorb = knobCol[2]
	par.bgalpha = knobCol[3]

def SliderVCOMP(path, settings):

	width = settings['width']
	height = settings['height']
	bgCol = settings['sliderCol'][0]
	knobCol = settings['knobCol'][0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	o = op(path + '/knob')
	par = o.par
	par.w = width - 4
	par.bgcolorr = knobCol[0]
	par.bgcolorg = knobCol[1]
	par.bgcolorb = knobCol[2]
	par.bgalpha = knobCol[3]
	
def FieldCOMP(path, settings):

	width = settings['width']
	height = settings['height']
	bgCol = settings['fontCol'][3]
	fontCol = settings['fontCol'][0]
	fontWidth = settings['fontWidth']
	format = settings['format']

	o = op(path)
	par = o.par
	par.w = width
	par.h = height - 4
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	par.fieldtype = format

	o = op(path + '/text')
	par = o.par
	par.resolution1 = width
	par.resolution2 = height - 4
	par.fontcolorr = fontCol[0]
	par.fontcolorg = fontCol[1]
	par.fontcolorb = fontCol[2]
	par.fontalpha = fontCol[3]
	par.fontsizex = fontWidth

def ButtonCOMP(path, settings):

	width = settings['width']
	height = settings['height']
	format = settings['format']

	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	fontCol = me.fetch('FONTCOL1')[0]
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	align = ['center', 'center']
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	par.buttontype = format

	
	label = settings['label']
	o = op(path + '/text')
	par = o.par
	par.text = label
	par.resolution1 = width
	par.resolution2 = height
	par.fontcolorr = fontCol[0]
	par.fontcolorg = fontCol[1]
	par.fontcolorb = fontCol[2]
	par.fontalpha = fontCol[3]
	par.fontsizex = fontWidth
	par.alignx = align[0]
	par.aligny = align[1]

	if op(path).op('string'):
		op(path).op('string')[0, 0] = label

def DropButton(path, settings):

	width = settings['width']
	height = settings['height']
	label = settings['label']
	labelWidth = settings['labelWidth']
	labelOn = settings['labelOn']

	gadgetCol = me.fetch('GADGETCOL1')
	buttonCol = me.fetch('BUTTONCOL1')
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	bgCol = gadgetCol[0]

	o = op(path)
	par = o.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]

	if labelOn == True:

		settings['align'] = ['left', 'center']
		settings['bgCol'] = bgCol
		settings['fontCol'] = fontCol
		settings['fontWidth'] = fontWidth
		op(path + '/label/setup').run(settings)

		width = width - labelWidth - 2

	else:

		o.op('label').par.display = 0

	settings['width'] = width
	settings['format'] = 'momentary'
	settings['align'] = ['center', 'center']

	item = str(o.parent().op('selectItems')[0,0])
	settings['label'] = item
	op(path + '/button/setup').run(settings)

def Scroll(path, settings):
	
	scrollWidth = settings['scrollWidth']
	listHeight = settings['listHeight']
	fullListHeight = settings['fullListHeight']
	
	knobCol = me.fetch('KNOBCOL1')[0]
	bgCol = me.fetch('SLIDERCOL1')[0]

	parent = op(path)
	par = parent.par
	par.w = scrollWidth
	par.h = listHeight

	slider = parent.op('slider')
	par = slider.par
	par.w = scrollWidth
	par.h = listHeight
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	
	knobHeight = min(listHeight,max(16, listHeight - (fullListHeight - listHeight)))

	knob = slider.op('knob')
	knob.par.w = scrollWidth - 2
	knob.par.h = knobHeight
	knob.par.y = max(min(listHeight - knobHeight * 0.5, listHeight - knobHeight - 1), 1)

	knob.par.bgcolorr = knobCol[0]
	knob.par.bgcolorg = knobCol[1]
	knob.par.bgcolorb = knobCol[2]
	knob.par.bgalpha = knobCol[3]

def ScrollH(path, settings):
	
	scrollHeight = settings['scrollHeight']
	listWidth = settings['listWidth']
	fullListWidth = settings['fullListWidth']
	
	knobCol = me.fetch('KNOBCOL1')[0]
	bgCol = me.fetch('SLIDERCOL1')[0]

	parent = op(path)
	par = parent.par
	par.h = scrollHeight
	par.w = listWidth

	slider = parent.op('slider')
	par = slider.par
	par.h = scrollHeight
	par.w = listWidth
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	
	#knobWidth = min(listWidth, max(16, listWidth * (listWidth/fullListWidth)))
	knobWidth = min(listWidth, max(64, listWidth - (fullListWidth-listWidth)))

	knob = slider.op('knob')
	knob.par.h = scrollHeight - 2
	knob.par.w = knobWidth
	knob.par.x = 0 

	knob.par.bgcolorr = knobCol[0]
	knob.par.bgcolorg = knobCol[1]
	knob.par.bgcolorb = knobCol[2]
	knob.par.bgalpha = knobCol[3]

def DropList(path, settings):
	
	width = settings['width']
	height = settings['height']
	listHeight = settings['listHeight']
	scrollWidth = settings['scrollWidth']
	labelWidth = settings['labelWidth']
	items = settings['itemTable']
	labelOn = settings['labelOn']
	bgCol = me.fetch('GADGETCOL1')[0]

	parent = op(path)
	parent.par.w = width
	parent.par.h = height
	parent.par.bgcolorr = bgCol[0]
	parent.par.bgcolorg = bgCol[1]
	parent.par.bgcolorb = bgCol[2]
	parent.par.bgalpha = bgCol[3]

	
	#settings['width'] = width
	parent.op('selectItems').par.dat = items

	parent.op('dropButton').op('setup').run(settings)


	width = width - scrollWidth - 2
	fullListHeight =parent.op('selectItems').numRows * height

	if labelOn == True:

		listWidth = width - labelWidth  

	else: 

		listWidth = width

	parent.op('maxDropHeight')[0,0] = listHeight

	listOn = 1 if listHeight < fullListHeight else 0

	parent.store('DispScroll', listOn)
	parent.store('ListHeight', fullListHeight)
	parent.store('WindowHeight', listHeight)

	settings['fullListHeight'] = listHeight

def DropListTex(path, settings):

	DropList(path, settings)

def DropListGlobal(path, settings):
	
	width = settings['width']
	height = settings['height']
	listHeight = settings['listHeight']
	scrollWidth = settings['scrollWidth']
	labelWidth = settings['labelWidth']
	items = settings['itemTable']
	labelOn = settings['labelOn']
	bgCol = me.fetch('GADGETCOL1')[0]

	parent = op(path)
	parent.par.w = width
	parent.par.h = settings['listHeight']
	parent.par.bgcolorr = bgCol[0]
	parent.par.bgcolorg = bgCol[1]
	parent.par.bgcolorb = bgCol[2]
	parent.par.bgalpha = bgCol[3]

	
	#settings['width'] = width
	parent.op('selectItems').par.dat = items

	#parent.op('dropButton').op('setup').run(settings)


	width = width - scrollWidth - 2

	dropCont = parent.op('dropContainer')

	fullListHeight = dropCont.op('in1').numRows * height

	if labelOn == True:

		listWidth = width - labelWidth  

	else: 

		listWidth = width

	#parent.par.w = width

	
	dropCont.par.h = min( listHeight, fullListHeight)
	dropCont.par.w = listWidth

	listOn = 1 if listHeight < fullListHeight else 0

	parent.store('DispScroll', listOn)
	parent.store('ListHeight', fullListHeight)
	parent.store('WindowHeight', listHeight)

	dropList = dropCont.op('list')
	dropList.par.w = listWidth
	dropList.par.h = fullListHeight

	scroll = dropCont.op('scroll')
	scroll.par.display = listOn
	scroll.par.x = listWidth - scrollWidth

	settings['fullListHeight'] = listHeight
	scroll.op('setup').run(settings)

def DropListMod(path, settings):
	
	width = settings['width']
	height = settings['height']
	listHeight = settings['listHeight']
	scrollWidth = settings['scrollWidth']
	labelWidth = settings['labelWidth']
	items = settings['itemTable']
	labelOn = settings['labelOn']
	bgCol = me.fetch('GADGETCOL1')[0]

	parent = op(path)
	parent.par.w = width
	parent.par.h = height
	parent.par.bgcolorr = bgCol[0]
	parent.par.bgcolorg = bgCol[1]
	parent.par.bgcolorb = bgCol[2]
	parent.par.bgalpha = bgCol[3]

	
	#settings['width'] = width
	parent.op('selectItems').par.dat = items

	parent.op('dropButton').op('setup').run(settings)


	width = width - scrollWidth - 2

	dropCont = parent.op('dropContainer')

	fullListHeight = parent.op('selectItems').numRows * height

	if labelOn == True:

		listWidth = width - labelWidth  

	else: 

		listWidth = width

	parent.par.w = width

	parent.op('maxDropHeight')[0,0] = listHeight

	listOn = 1 if listHeight < fullListHeight else 0

	parent.store('DispScroll', listOn)
	parent.store('ListHeight', fullListHeight)
	parent.store('WindowHeight', listHeight)

	settings['fullListHeight'] = listHeight

def CheckBox(path, settings):

	width = settings['width']
	height = settings['height']
	scrollWidth = settings['scrollWidth']
	labelWidth = settings['labelWidth']
	label = settings['label']
	fontCol = me.fetch('FONTCOL1')
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	labelAlign = ['left', 'center']
	
	gadgetCol = me.fetch('GADGETCOL1')
	bgCol = gadgetCol[0]

	gadget = op(path)
	par = gadget.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	par.marginr = scrollWidth + 4

	settings['width'] = width 

	labelSettings = {'labelWidth': labelWidth, 'height': height , 'label': label, 'align': labelAlign, 
	'bgCol': [0,0,0,0], 'fontCol': fontCol, 'fontWidth': fontWidth}

	gadget.op('label/setup').run(labelSettings)

def ButtonCtrlMap(path, settings, mapLength = 1):

	width = settings['width']
	height = settings['height']
	format = settings['format']

	bgCol = me.fetch('CTRL_MAP_COL')[0]

	button = op(path)
	par = button.par
	par.w = width
	par.h = height
	par.bgcolorr = bgCol[0]
	par.bgcolorg = bgCol[1]
	par.bgcolorb = bgCol[2]
	par.bgalpha = bgCol[3]
	par.buttontype = format

	fontCol = me.fetch('FONTCOL1')[0]
	fontWidth = me.fetch('FONTHEIGHT1')[0][0]
	align = ['center', 'center']

	text = op(path + '/text')
	par = text.par
	par.resolution1 = width
	par.resolution2 = height
	par.fontcolorr = fontCol[0]
	par.fontcolorg = fontCol[1]
	par.fontcolorb = fontCol[2]
	par.fontalpha = fontCol[3]
	par.fontsizex = fontWidth
	par.alignx = align[0]
	par.aligny = align[1]
	par.wordwrap = True

	button.store('RollOffCol', bgCol)

	allParmMaps = op(button.fetch('ALL_PARM_MAPS'))

	
	ctrlsPath = button.fetch('CtrlsPath', button.parent().path)

	if ctrlsPath in allParmMaps.storage.keys():
		mapStore = allParmMaps.fetch(ctrlsPath)
		mapStore[button.parent().path] = {'mapMIDI': 0, 'pathMIDI': [], 'lenMIDI': 0, 'mapOSC': 0, 'pathOSC': [],
		'lenOSC': 0, 'mapDMX': 0, 'pathDMX': [], 'lenDMX': 0, 'mapLive': 0, 'pathLive': [], 'lenLive': 0, 'mapLength': mapLength}

	else:
		mapStore = {}
		mapStore[button.parent().path] = {'mapMIDI': 0, 'pathMIDI': [], 'lenMIDI': 0, 'mapOSC': 0, 'pathOSC': [], 
		'lenOSC': 0, 'mapDMX': 0, 'pathDMX': [], 'lenDMX': 0, 'mapLive': 0, 'pathLive': [], 'lenLive': 0, 'mapLength': mapLength}
		allParmMaps.store(button.parent().path, mapStore)
