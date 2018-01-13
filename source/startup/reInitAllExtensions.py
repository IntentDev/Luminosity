def reInitExt(comp):
	
	hasExt = False	
	par = comp.par
	
	for n in range(1,5):
		
		nStr = str(n)
		ext = 'ext' + nStr
		extPar = 'extension' + nStr
	
		ext = getattr(par, extPar)
	
		if ext != '':
			hasExt = True	

	if hasExt == True:
	
		par.reinitextensions.pulse()
		return 1
		
	else:	
		return 0
	
def reInitAllExt():
	
	allComps = root.findChildren(type = COMP)
	
	i = 0
		
	for compPath in allComps:
		
		comp = op(compPath)
		i += reInitExt(comp)
				
	print(str(i) + ' COMPs with extensions reinitialized')

if me.fetch('NODE') == 'master':

	reInitAllExt()