copyBack = '''
op(me.fetch('PROC')).copy(op('commandProcessor'))
op('commandProcessor').destroy()
'''

me.parent().copy(op(me.fetch('COMMAND_PROCESSOR')))
op(me.fetch('COMMAND_PROCESSOR')).destroy()
run(copyBack, delayFrames = 5)