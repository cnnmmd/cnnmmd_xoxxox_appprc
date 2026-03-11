import sys
import json
import argparse
import asyncio
from aiohttp import web
from xoxxox.params import Config
from xoxxox.shared import Custom

#---------------------------------------------------------------------------

async def runprc(strcmd: str, lstarg: list[str], datprc: bytes):
  prcsub = await asyncio.create_subprocess_exec(
    strcmd,
    *lstarg,
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
    )
  try:
    stdout, stderr = await asyncio.wait_for(
      prcsub.communicate(datprc if datprc else None),
      timeout=secout
    )
  except asyncio.TimeoutError:
    prcsub.kill()
    await prcsub.wait()
  if stdout:
    print("stdout[" + str(stdout.decode("utf-8")) + "]", flush=True)
  else:
    stdout="".encode("utf-8")
  if stderr:
    print("stderr[" + str(stderr.decode("utf-8")) + "]", flush=True, file=sys.stderr)
  else:
    stderr="".encode("utf-8")
  return (stdout, stderr)

async def ressys(datreq):
  global diccnf, dicprm
  dicreq = await datreq.json()
  diccnf = Custom.update(dicreq["config"], dicprm)
  return web.Response(
    text=json.dumps({"return": "1"}),
    content_type="application/json",
  )

async def resgen(datreq):
  global diccnf
  datprc = await datreq.read()
  if diccnf["pglang"] == "nop":
    stdout = "<nop>".encode("utf-8")
    stderr = "<nop>".encode("utf-8")
  if diccnf["pglang"] == "risc-v":
    stdout, stderr = await runprc("bash", ["/env/risc-v/exersc.sh"], datprc)
  if diccnf["pglang"] == "bash":
    stdout, stderr = await runprc("bash", [], datprc)
  if diccnf["pglang"] == "haskell":
    stdout, stderr = await runprc("ghci", ["-v0"], datprc)
  if diccnf["pglang"] == "prolog":
    stdout, stderr = await runprc("swipl", ["-q"], datprc)
  if diccnf["pglang"] == "ruby":
    stdout, stderr = await runprc("ruby", [], datprc)
  if diccnf["pglang"] == "scheme":
    stdout, stderr = await runprc("guile", ["-s", "/dev/stdin"], datprc)
  if diccnf["pglang"] == "typescript":
    stdout, stderr = await runprc("bash", ["/env/nodejs/exetys.sh"], datprc)
  if diccnf["pglang"] == "python":
    stdout, stderr = await runprc("/env/python/bin/python", [], datprc)
  return web.Response(
    text=json.dumps({"stdout": stdout.decode("utf-8"), "stderr": stderr.decode("utf-8")}),
    content_type="application/json",
  )

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--secure", default="0")
parser.add_argument("--svport", type=int, default="80")
parser.add_argument("--config")
parser.add_argument("--adraco", type=str) # default: cnfnet
parser.add_argument("--pthcrt", type=str) # default: cnfnet
parser.add_argument("--pthkey", type=str) # default: cnfnet
objarg = parser.parse_args()

dicnet = Custom.update(Config.cnfnet, {k: v for k, v in vars(objarg).items() if v is not None})
dicprm = {k: v for k, v in vars(objarg).items() if v is not None}

dicprm.pop("secure")
dicprm.pop("svport")

secure = objarg.secure
svport = objarg.svport

adrsys = "/sys"
adrgen = "/gen"

#---------------------------------------------------------------------------

secout = 10
diccnf = {}
appweb = web.Application()
appweb.add_routes([web.post(adrsys, ressys)])
appweb.add_routes([web.post(adrgen, resgen)])
if secure == "0":
  web.run_app(appweb, port=svport)
if secure == "1":
  import ssl
  sslcon = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  sslcon.load_cert_chain(dicnet["pthcrt"], dicnet["pthkey"])
  web.run_app(appweb, port=svport, ssl_context=sslcon)
