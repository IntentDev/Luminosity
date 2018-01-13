ctrlMaps = me.parent()
allParmMaps = op('allParmMaps')
	
curSel = args[0]
ctrlsPath = args[1]
prevSel = ctrlMaps.fetch('CurSel')
prevCtrlsPath = ctrlMaps.fetch('CtrlsPath')

ctrlMaps.store('PrevSel', prevSel)
ctrlMaps.store('CurSel',curSel)
ctrlMaps.store('CtrlsPath', ctrlsPath)

bgCol = me.fetch('CTRL_MAP_COL')

prev = op(prevSel + '/buttonCtrlMapSet')

mapData = op('allParmMaps/mapData')
mapType = me.fetch('CTRL_MAP_TYPE')
ctrls =  op('controllers')
curComp = ctrls[0, mapType].val
curMap = ctrls[1, mapType].val
curPath = ctrls[2, mapType].val	

if prev:
	
	mapState = allParmMaps.fetch(prevCtrlsPath)[prevSel][curMap] * 3

	prevCol = bgCol[mapState]	
	prev.par.bgcolorr = prevCol[0]
	prev.par.bgcolorg = prevCol[1]
	prev.par.bgcolorb = prevCol[2]
	prev.par.bgalpha = prevCol[3]
	prev.store('RollOffCol', prevCol)

cur = op(curSel + '/buttonCtrlMapSet')
curCol = bgCol[2]

cur.par.bgcolorr = curCol[0]
cur.par.bgcolorg = curCol[1]
cur.par.bgcolorb = curCol[2]
cur.par.bgalpha = curCol[3]

cur.store('RollOffCol', curCol)

if op(curComp).fetch('MapSeries') == True:
	op(curComp).op('mapSeries').run(curSel)