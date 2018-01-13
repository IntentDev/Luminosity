lock = '''
thumb = args[6]
labelPath = args[7]

thumb.lock = True
op(labelPath).lock = True

parent(2).LoadMovie(args[0],args[1],args[2],args[3],args[4],args[5])
'''

#args(filePath,name,mediaType,bank,channel,clip)

movLoader = op('movieLoad')
movLoader.par.file = args[1]
movLoader.par.reload.pulse()
thumbPath = op('thumb').path
 
labelPath = me.fetch('CLIP_DATA') +'/'+ args[3] +'/'+ args[4] +'/'+ args[5] +'/label'

op(labelPath).lock = False
op(labelPath).par.text = args[0]

thumb = op(me.fetch('PLUGINS') + '/players/singleMoviePlayer/plugin/config/thumb')
thumb.lock = False
thumb.par.top = thumbPath

run(lock, args[0],args[1],args[2],args[3],args[4],args[5], thumb, labelPath, delayFrames = 1)