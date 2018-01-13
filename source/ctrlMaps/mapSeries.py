ctrlsPath = me.fetch('CtrlsPath')
curSel = me.fetch('CurSel')
allParmMaps = op(me.fetch('ALL_PARM_MAPS'))
mapState = 'map' + me.parent().name
mapPath = 'path' + me.parent().name
mapLen = 'len' + me.parent().name

ctrlMap = me.fetch('LastMap')

ctrlsKey = allParmMaps.fetch(ctrlsPath)
mapLength = ctrlsKey[curSel]['mapLength']
mapped = ctrlsKey[curSel][mapLen]


if mapped < mapLength:
	
	mapped += 1
	curMaps = op('curMaps')
	ctrlsKey[curSel][mapPath].append(ctrlMap)
	ctrlsKey[curSel][mapLen] = mapped	
	curMaps.appendRow([curSel, mapped - 1, ctrlMap])
	
	if mapped == mapLength:
		me.parent().store('MapSeries', False)


op('../examineMaps').cook(force = True)