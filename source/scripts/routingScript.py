# me is this DAT.
# 
# dat is the changed DAT.
# rows is a list of row indices.
# cols is a list of column indices.
# cells is the list of cells that have changed content.
# prev is the list of previous string contents of the changed cells.
# 
# Make sure the corresponding toggle is enabled in the DAT Execute DAT.
# 
# If rows or columns are deleted, sizeChange will be called instead of row/col/cellChange.


def tableChange(dat):
	return

def rowChange(dat, rows):
	return

def colChange(dat, cols):
	return

def cellChange(dat, cells, prev):

	destinations = op(me.fetch('VIDEO_DEST_PATHS'))
	sources = op(me.fetch('VIDEO_SRC_PATHS'))
	chanName = me.fetch('ChanName')
	dispName = me.fetch('DisplayName')


	sourcePath = sources[chanName, 2]
	#print(sourcePath)
	myDestTable = op('outputs')
	srcOP = '/out1'


	for c in cells:
	
		name = str(dat[c.row,0])

		if name != 'input':	

			if re.match('send', name):

				preState = int(op('selPre')[c.row, 1])

				if preState == 1:
					srcOP = '/channelFX/input'

			destSrcTablePath = destinations[c, 1] + '/routing/sources'

			destSrcTable = op(destSrcTablePath)
			destPath = destinations[c, 2]	
			
			prevDestSrcTable = op(myDestTable[name,1])
				
			destSrcTable.appendRow([sourcePath, name, dispName, srcOP])

			if prevDestSrcTable[sourcePath, 0]:
				prevDestSrcTable.deleteRow(sourcePath)
			myDestTable[name,1] = destSrcTablePath
		
		elif name == 'input':
		
			if not re.match('clip*', chanName):

				mySourceTable = op('sources')
				myInputTable = op('input')
				prevSrcPath = myInputTable[0,0]
				sourcePath = sources[c,2]
				dispName = str(op(me.fetch('VIDEO_SOURCES'))[c,0])
				
				if int(c) != 0:				
					mySourceTable.appendRow([sourcePath, 'output', dispName, srcOP])
				
				if mySourceTable[prevSrcPath,0]:
					mySourceTable.deleteRow(prevSrcPath)

				myInputTable[0,0] = sourcePath

	return

def sizeChange(dat):
	return
	