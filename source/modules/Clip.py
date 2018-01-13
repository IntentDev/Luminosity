from TDStoreTools import StorageManager

class Clip(object):

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.ViewPreview = op.UI.op('clipControls/previewClip/viewTOP')

		self.IsPlaying = False
		self.IsClip = True
		
		
	def PreviewClip(self):

		self.ViewPreview.par.top = self.ownerComp.op('out1')

	def Trigger(self, *args):
		#crossFade = args[0]
		#crossFade.run(self.ownerComp.op('out1').path)

		channel = args[0]
		channel.CrossFade(self.ownerComp.op('out1').path)

		self.Active = True
		self.IsPlaying = True


	def ReTrigger(self):
		pass

	def CheckIsPreview(self):
		if self.ViewPreview.par.top.eval():
			return self.ViewPreview.par.top.eval().parent() == self.ownerComp

	def Stop(self):
		if not self.CheckIsPreview():
			self.Active = False

		self.IsPlaying = False

	def SetViewPreview(self):
		self.ViewPreview.par.top = self.ownerComp.op('out1')

	@property
	def ControlsSelected(self):
		return self.ownerComp.fetch('ControlsSelected', tdu.Dependency(False))

	@ControlsSelected.setter
	def ControlsSeleced(self, value):
		self.ownerComp.store('ControlsSeleced', tdu.Dependency(value))
