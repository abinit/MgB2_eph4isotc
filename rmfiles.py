#!/usr/bin/env python

import os

for root, dirs, files in os.walk("."):
   for name in files:
      filepath = os.path.join(root, name)
      if name in ("out_DDB.nc", "out_OUT.nc", "out_EIG.nc", "out_EIG", "out_DDK.nc", "in_DEN.nc", # "out_WFK.nc", 
                  "mods.err", "queue.qerr", "queue.qout",
                  "in_WFK.nc", "out_DVDB", "run.log", "run.abo", "job.sh", "run.err", "__startlock__") or \
          "_1WF" in name or name == "out_EVK.nc" or name.endswith(".json") or name.endswith(".pickle"):
          print("Removing: ", filepath)
          os.remove(filepath)
