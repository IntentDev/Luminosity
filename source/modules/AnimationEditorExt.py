"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""

class AnimationEditorExt:
	"""
	AnimationEditorExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.lm = op.LM
		self.remote = self.lm.op('remote')
		self.Window = self.ownerComp.op('window')
		self.Graph = self.ownerComp.op('graph')
		self.TimeGraph = self.Graph.op('timeGraph')
		self.TimeBar = self.ownerComp.op('timeBar/bar')
		self.Transport = self.ownerComp.op('transport')
		self.TimeLineFrame = self.ownerComp.op('timeline/frame')
		self.TimeLineKeyFrame = self.TimeLineFrame.op('keyframe')
		self.TimeLineKeys = self.TimeLineFrame.op('keys')
		self.ParAnimComp = self.ownerComp.fetch('ParAnimCOMP')
		self.AnimComp = self.ownerComp.fetch('AnimCOMP')
		self.ParList = self.ownerComp.op('addParameter/list')
		self.ClipPath = self.ownerComp.op('clippath/string')

		self.datexecSendKeys = self.ownerComp.op('datexecSendKeys')
		self.datexecSendChannels = self.ownerComp.op('datexecSendChannels')
		self.parexecAnimComp = self.ownerComp.op('parexecAnimComp')


	def SetAnimEditor(self, parAnimCOMP, openUI = False, floating = False):

		#if self.ownerComp.fetch('VIEW_ANIM_EDIT') == 1 or self.Window.isOpen:

		cross = int(parAnimCOMP.par.Cross)
		animCOMP = parAnimCOMP.op('animation' + str(cross))

		
		if openUI and not self.Window.isOpen and not floating:
			self.SetViewAnimEdit(1)
		elif floating:
			self.OpenFloating()
		

		self.ownerComp.store('ParAnimCOMP', parAnimCOMP)
		self.ownerComp.store('AnimCOMP', animCOMP)
		self.ParAnimComp = self.ownerComp.fetch('ParAnimCOMP')
		self.AnimComp = self.ownerComp.fetch('AnimCOMP')

		op.ANIM_EDITOR.setVar('KEYPATH', animCOMP.path)

		numParms = len([r[0].val for r in self.AnimComp.parent.plugin.op('parameters').rows()[1:]])
		self.ParList.par.rows = numParms
		self.ParList.par.reset.pulse()
		
		name = self.ParAnimComp.fetch('CompAttr')['attr']['name']
		path = self.ParAnimComp.path.replace('/Luminosity/database/', '').replace('/plugin', '').replace('/animation', '')

		self.ClipPath[0, 0] = path + ': ' + name
		self.ClipPath.cook(force = True)

		self.SetupAnimEdit()
		animCOMP.par.cuepulse.pulse()

		self.datexecSendKeys.par.dat = self.AnimComp.op('keys')
		self.datexecSendChannels.par.dat = self.AnimComp.op('channels')
		self.parexecAnimComp.par.op = self.AnimComp



	def OpenFloating(self):
		self.Window.par.winopen.pulse()
		self.SetViewAnimEdit(2)

	def CloseFloating(self):
		self.SetViewAnimEdit(0)

	def CloseAnimEditor(self):
		if self.Window.isOpen:
			self.SetViewAnimEdit(2)
		else:
			self.SetViewAnimEdit(0)
			self.SelectNullAnimComp()

	def SetViewAnimEdit(self, state):
		op.LM.store('VIEW_ANIM_EDIT', state)

		self.TimeLineKeyFrame.bypass = -1 * min(1, state) + 1

		self.ownerComp.par.w = 1910
		self.ownerComp.par.h = 514

	def SetupAnimEdit(self, *args):
		self.Transport.Length()
		self.Transport.op('transport').panel.radio = 1
		self.TimeLineFrame.par.speed = self.AnimComp.par.speed.eval()
		#self.TimeLineFrame.par.play = True
		end = int(self.AnimComp.par.end.eval())
		self.TimeLineFrame.par.end = end
		self.TimeLineKeys[2, 1] = end
		self.TimeLineKeys[2, 2] = end
		self.TimeLineFrame.par.cuepoint = 1
		self.TimeLineFrame.par.cuepulse.pulse()

		delay = op.LM.Delay(delayFrames = 1, fromOP = me)
		delay.Call(self.TimeBar, 'Setup')
		delay.Call(self.TimeGraph, 'Fit')

	def SelectNullAnimComp(self):

		self.SetAnimEditor(op.MASTER_ANIMATION, openUI = False, floating = False)


	def SendAnimKeys(self):

		keys = [self.AnimComp.op('keys').text]



		self.remote.GetAttr(self.lm, 'SetAnimKeys', keys, self.ParAnimComp.path)


	def SendAnimChannels(self):

		channels = [self.AnimComp.op('channels').text]

		self.remote.GetAttr(self.lm, 'SetAnimChannels', channels, self.ParAnimComp.path)
		







