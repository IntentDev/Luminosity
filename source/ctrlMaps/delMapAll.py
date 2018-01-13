mapType = me.fetch('CTRL_MAP_TYPE')
ctrls =  op('controllers')
curComp = ctrls[0, mapType].val
curMap = ctrls[1, mapType].val
curPath = ctrls[2, mapType].val

ctrlMaps = me.parent()
curSel = args[0]
ctrlsPath = args[1]
ctrlMaps.store('CurSel',curSel)
ctrlMaps.store('CtrlsPath', ctrlsPath)

op(curComp).op('delMap').run()