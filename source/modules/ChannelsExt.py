"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""

import copy

class ChannelsExt(object):
	"""
	ChannelsExt description
	
	Update all routing when channels are destroyed
	
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.destList = ['auxChannels', 'masterChannels']
		self.sourceDestList = ['clipChannels', 'auxChannels', 'masterChannels']

	def CheckRouting(self):

		for sourceDestPath in self.sourceDestList:
			sourceDest = self.ownerComp.op(sourceDestPath)
			channelPaths = [channel[0].val for channel in sourceDest.op('channels').rows()[1:]]

			for channelPath in channelPaths:
				channel = sourceDest.op(channelPath)
				#print(channel.path)
				channelUI = op(channel.path.replace('/Luminosity/database/', '/Luminosity/master/ui/'))
				#print(channelUI)


				inputDAT = channel.op('routing/input')				
				sourcesDAT = channel.op('routing/sources')
				outputsDAT = channel.op('routing/outputs')
				#print(outputsDAT)

				inputSourcePath = inputDAT[0, 0].val.replace('/Luminosity/processor/videoRouting/', '')
				inputChannel = self.ownerComp.op(inputSourcePath)

				if inputChannel == None:
					inputDAT[0, 0] = '/Luminosity/database/channels/noneChannel'
					#channelUI.op('input/setUI').run({'value': 0})

				sources = [r[0].val for r in sourcesDAT.rows()]

				for source in sources:
					sourcePath = source.replace('/Luminosity/processor/videoRouting/', '')
					sourceChannel = self.ownerComp.op(sourcePath)
					if sourceChannel == None:
						sourcesDAT.deleteRow(source)
		
				for i in range(4):
					destName = outputsDAT[i, 0].val
					src = op(outputsDAT[i, 1].val.replace('/routing/sources', ''))
					if src == None:
						outputsDAT[i, 1] = '/Luminosity/database/channels/noneChannel/routing/sources'
						#channelUI.op(destName + '/setUI').run({'value': 0})


class ChannelsUIExt(object):
	"""
	ChannelsExt description
	
	Update all routing when channels are destroyed
	
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp


	def SelectChannel(self, sel, selDigits, select):

		chanGrpSetup = self.ownerComp.op('chanGrpSetup')
		storeName = str(chanGrpSetup['storeName', 1])
		name = str(chanGrpSetup['name', 1])

		op(me.fetch('ROOT')).store(storeName, selDigits)

		channels = self.ownerComp.op('channels')

		for r in channels.rows()[1:]:

			chan = str(r[0])
			chanOP = self.ownerComp.op(chan)		
			button = chan + '/label'
			setUI = button + '/setUI'
			preview = self.ownerComp.op('preview/' + r[0])
			
			if chan != sel:
				
				self.ownerComp.op(setUI).run({'value': 0})
				
			if chan == sel:
			
				self.ownerComp.op(setUI).run({'value': 1})
				self.ownerComp.op(button + '/button').panel.state = 1
			
				if select == True: 
				
					chanOP = self.ownerComp.op(chan)
					dataChan = chanOP.fetch('Channel')
					UISelectPath = chanOP.fetch('UISelectPath')
					slots = chanOP.op('effectSlots/slots')
					slot = slots.panel.cellradioid
					slots.ext.EffectSlots.Lc(slots, slot)

					if op.LM.fetch('VIEW_PRESET_CONTROLS') != 0:	
						chanOP.op('presets').SetView()

		if name != 'Master':	
			op(self.ownerComp.fetch('SETTINGS_DAT'))[name + 'Preview',1] = selDigits

		if name == 'Aux':
			op(self.ownerComp.fetch('VIDEO_ROUTING') + '/outToUI/auxPreview').par.top = me.fetch('AUX_CHAN_VID') +'/channel' + str(selDigits) +'/out1'

		elif name == 'Clip':
			op(self.ownerComp.fetch('VIDEO_ROUTING') + '/outToUI/clipPreview').par.top = me.fetch('CLIP_CHAN_VID') +'/channel' + str(selDigits) +'/out1'

			if op.DATABASE.fetch('CLIP_TRIG_MODE') == 1:

				numClipChn = op.DATABASE.fetch('NUM_CLIP_CHAN')

				for i in range(0, numClipChn):
				
					triggerPath = me.fetch('CLIP_CHAN_VID') +'/clipChannel'+ str(selDigits) +'/trigger'
					op.CLIP_LANES_UI.op('clipLane' + str(i)).store('TriggerPath', triggerPath)

		
		channelCtrls = self.ownerComp.op(self.ownerComp.fetch('UISelectPath'))
		channelCtrls.store('ChannelName', sel)
		channelCtrls.store('DisplayName', self.ownerComp.op(sel).fetch('DisplayName'))
		channelCtrls.store('ChannelPath', self.ownerComp.op(sel).fetch('CtrlsPath'))
	







