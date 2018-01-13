scripts = parent().findChildren()

notSelected = []

for script in scripts:

	sels = op.LM.findChildren(type = selectDAT, key = lambda x: x.par.dat.eval() == script)

	if len(sels) == 0:
		notSelected.append(script)

	print(script.name)
	for sel in sels:
		print(sel)

	print('\n')


print('\n Not Selected:')

for nSel in notSelected:
	print(nSel)
