lock = '''
labelPath = args[6]
op(labelPath).lock = True

parent(2).LoadAudio(args[0],args[1],args[2],args[3],args[4],args[5])
'''

#args(filePath,name,mediaType,bank,channel,clip)

loader = op('loader')
loader.par.file = args[1]

#thumbPath = op('thumb').path
 
#thumbSelectPath = me.fetch('CLIP_DATA') +'/'+ args[3] +'/'+ args[4] +'/'+ args[5] +'/thumb'
labelPath = me.fetch('CLIP_DATA') +'/'+ args[3] +'/'+ args[4] +'/'+ args[5] +'/label'

op(labelPath).lock = False
op(labelPath).par.text = args[0]

#op(thumbSelectPath).lock = False
#op(thumbSelectPath).par.top = thumbPath

run(lock, args[0],args[1],args[2],args[3],args[4],args[5], labelPath, delayFrames = 1)
#op('lock').run(args[0],args[1],args[2],args[3],args[4],args[5],thumbSelectPath, labelPath, delayFrames = 1)
#op('preReadCheck').run(args[0],args[1],args[2],args[3],args[4],args[5],thumbSelectPath, labelPath)