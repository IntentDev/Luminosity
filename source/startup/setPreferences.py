dat = op('convert1')
import tableFunc as tF

s = {r[0].val:tF.SetToType(r[1].val) for r in dat.rows()}

if s['IS_BACKUP'] == 1:
	s['MASTER_IP'] = s['BCKP_MASTER_IP']
	
for i in s.items():
	me.fetch('ROOT').store(i[0], i[1])
