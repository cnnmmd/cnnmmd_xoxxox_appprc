#---------------------------------------------------------------------------

import sys
import asyncio
from xoxxox.shared import PrcFlw
from xoxxox.midclt import MidClt

#---------------------------------------------------------------------------

dicsrv = PrcFlw.dicsrv()
adrmid = dicsrv["xoxxox_appmid_loc"]

#---------------------------------------------------------------------------

async def exeprc(config, strprg):
  datres = await MidClt.reqprc({}, adrmid + MidClt.adrini)
  datres = await MidClt.reqset(strprg, adrmid + MidClt.adrset)
  datres = await MidClt.reqprc({"keymmd": datres["keymmd"], "keyprc": "xoxxox.PrcPrc.cnnprc", "server": "http://xoxxox_appprc", "config": config}, adrmid + MidClt.adrprc)

config = sys.argv[1]
strprg = sys.argv[2]
datres = asyncio.run(exeprc(config, strprg))
