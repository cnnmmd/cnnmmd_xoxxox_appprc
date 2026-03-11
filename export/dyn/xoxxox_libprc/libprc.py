#---------------------------------------------------------------------------
# 参照

import aiohttp
from xoxxox.libmid import LibMid

#---------------------------------------------------------------------------
# 処理：各種のプログミング言語を実行する

class PrcPrc:

  # 変数
  oldcfg = ""

  # 実行
  @staticmethod
  async def cnnprc(datorg, server, config):

    if config != PrcPrc.oldcfg:
      async with aiohttp.ClientSession() as sssweb:
        async with sssweb.post(server + "/sys", json={"config": config}) as datres:
          dicres = await datres.json()
      PrcPrc.oldcfg = config

    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(server + "/gen", data=datorg) as datres:
        dicres = await datres.json()
    return (dicres["stdout"], dicres["stderr"])

LibMid.dicprc["xoxxox.PrcPrc.cnnprc"] = {"frm": "xoxxox_libprc.PrcPrc.cnnprc", "arg": ["keymmd"], "cnf": ["server", "config"], "syn": False}
