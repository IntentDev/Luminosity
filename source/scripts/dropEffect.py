attr = me.fetch('attr')
itemTable = op(attr['itemTable'])

slot = op('slots').panel.celldropid

if args[0] == 'contents':
	browser = op(me.fetch('BROWSER'))
	browserContents = browser.op('contents')
	selected = browserContents.fetch('selected', [])
	selectedType = selected[0]['type']


	if selectedType == 'effect':

		name = selected[0]['name']
		path = selected[0]['location']

		channel = me.fetch('Channel')
		dataSlotPath = channel +'/effects/slot' + str(slot)
				
		storeComp = me.fetch('StoreComp')
		compPar = storeComp.fetch('CompPar')
		effectSlots = compPar['values']['effectSlots']
		
		parName = 'slot' + str(slot)
		
		effectSlots[parName]['name'] = name
		effectSlots[parName]['path'] = path
		
		itemTable[slot + 1,'name'] = name
		itemTable[slot + 1,'path'] = path

		op.LM.Load().LoadEffect(path, dataSlotPath)
