def SetToType(dataIn):
	
	typeFilter = ['COMP', 'TOP', 'DAT', 'SOP', 'CHOP']

	if not dataIn:	
		return dataIn	
	elif dataIn in typeFilter:
		return dataIn
		
	try:
		output = eval(dataIn)
		
	except:
		output = dataIn
	
	#if dataIn[0] == '[':
	#	output = GetCellList(dataIn)
		
	return output
	
def GetCellList(dataIn):

	outputList = []
			
	dataIn = dataIn.strip('[')
	dataIn = dataIn.strip(']')
			
	items = dataIn.split(',')
	
	for item in items:

		item = item.strip()
		item = item.strip("'")
		item = item.strip("'")
		item = item.strip('"')
		item = item.strip('"')
		
		try:
			if isinstance(eval(item), float):
				item = float(item)
				
			elif isinstance(eval(item), int):
				item = int(item)
		except:
			pass
			
		outputList.append(item)
	
	return outputList	

def ColList(table, col, startRow):

	l = []

	if isinstance(col, str):		
		col = table[0, col].col
	
	for r in table.rows()[startRow:]:
	
		l.append(setToType(r[col].val))
		
	return l

def FillCol(table, col, startRow, inputList):

	for r in table.rows()[startRow:]:
		
		table[r[0].row, col] = inputList[r[0].row - startRow]	

	
			