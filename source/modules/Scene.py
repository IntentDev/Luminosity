class Scene(object):

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.SetActive = self.Config.op('setActive')

	def SetSceneActive(self, val):

		self.SetActive.par.active = False
		self.Parameters['sceneActive', 1] = val
		
		ctrls = op(self.Attr['uiPath'])
		ctrls.op('sceneActive').SetUI(ctrls, {'value': val})
		
		run("args[0].par.active = True", self.SetActive, delayFrames = 1)


