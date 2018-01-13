ctrlsPath = me.fetch('CtrlsPath')
curSel = me.fetch('CurSel')
allParmMaps = op(me.fetch('ALL_PARM_MAPS'))
mapState = 'map' + me.parent().name
mapPath = 'path' + me.parent().name
mapLen = 'len' + me.parent().name
ctrlsKey = allParmMaps.fetch(ctrlsPath)
mapLength = ctrlsKey[curSel]['mapLength']
	
ctrlsKey[curSel][mapState] = 0
ctrlsKey[curSel][mapPath] = []

ctrlsKey[curSel][mapLen] = 0

curCol = me.fetch('CTRL_MAP_COL')[0]
cur = op(curSel + '/buttonCtrlMapSet')
cur.par.bgcolorr = curCol[0]
cur.par.bgcolorg = curCol[1]
cur.par.bgcolorb = curCol[2]
cur.par.bgalpha = curCol[3]
cur.store('RollOffCol', curCol)

text = op(curSel + '/buttonCtrlMapSet/text')
text.par.text = ''

me.parent().store('MapSeries', False)

try:
	me.fetch('Maps').pop(curSel)
except:
	pass