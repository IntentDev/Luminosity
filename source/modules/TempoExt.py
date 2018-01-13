class TempoExt(object):
	
	def __init__(self, ownerComp):
		#The component to which this extension is attached
		self.ownerComp = ownerComp
		self.prevTime = 0
		self.totalTime = 0
		self.count = 0
		self.bpm = 0
		self.Tempo = tdu.Dependency(op.LM.time.tempo)
		self.TempoSet = tdu.Dependency(True)

		self.settings = op(op.LM.fetch('SETTINGS_DAT'))

	def Tap(self):

		self.TempoSet.val = False

		time = absTime.seconds	
		d = time - self.prevTime
		
		if (d > 2.5 or d <= 0.0):
			self.totalTime = 0
			self.count = 0		
			
		else:
			self.totalTime += d
			self.count += 1
			avgTime = self.totalTime / self.count
			self.bpm = 60 / avgTime

		self.prevTime = time
		self.Tempo.val = [self.bpm, self.Tempo.val][self.bpm == 0.0]

	def Sync(self):

		#need separate function for cues!!!
		op.LM.store('SYNC', 1)
		self.SetTempo(self.Tempo.val)

		run("args[0].store('SYNC', 0)", op.LM, delayFrames = 1, fromOP = me)

	def SetTempo(self, tempo):

		self.TempoSet.val = True

		self.Tempo.val = tempo
		op.LM.time.tempo = tempo

		self.settings['tempo', 1] = tempo

		self.SetBPMScale()


	def SetBPMScale(self):

		rate = op.LM.time.rate
		spb = rate / self.Tempo.val
		fpb = spb * rate
		animBPMScale = .5 / spb * (op.LM.fetch('TICKS_PER_BEAT').val / 120 * 4)
		#print(animBPMScale)
		
		op.LM.store('SPB', tdu.Dependency(spb))
		op.LM.store('FPB', tdu.Dependency(fpb))
		op.LM.store('ANIM_BPM_SCALE', tdu.Dependency(animBPMScale))
	


