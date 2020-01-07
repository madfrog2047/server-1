#!/usr/bin/python

"""
 * MaNGOS is a full featured server for World of Warcraft, supporting
 * the following clients: 1.12.x, 2.4.3, 3.3.5a, 4.3.4a and 5.4.8
 *
 * Copyright (C) 2005-2020 MaNGOS <https://getmangos.eu>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import os, sys, threading, time, subprocess
from multiprocessing import cpu_count
from collections import deque

mapList = deque([0,1,530,13,25,30,33,34,35,36,37,42,43,44,47,48,70,90,109,129,169,189,209,229,230,249,269,289,309,329,349,369,
    389,409,429,449,450,451,469,489,509,529,531,532,533,534,540,542,543,544,545,546,547,548,550,552,553,554,555,556,557,558,559,
    560,562,564,565,566,568,572,580,582,584,585,586,587,588,589,590,591,593,598])

class workerThread(threading.Thread):
    def __init__(self, mapID):
        threading.Thread.__init__(self)
        self.mapID = mapID

    def run(self):
        name = "Worker for map %u" % (self.mapID)
        print "++ %s" % (name)
        if sys.platform == 'win32':
            stInfo = subprocess.STARTUPINFO()
            stInfo.dwFlags |= 0x00000001
            stInfo.wShowWindow = 7
            cFlags = subprocess.CREATE_NEW_CONSOLE
            binName = "mmap-extractor.exe"
        else:
            stInfo = None
            cFlags = 0
            binName = "./mmap-extractor"
        if self.mapID == 0:
            retcode = subprocess.call([binName, "%u" % (self.mapID), "--silent",  "--offMeshInput", "offmesh.txt"], startupinfo=stInfo, creationflags=cFlags)
        else:
            retcode = subprocess.call([binName, "%u" % (self.mapID), "--silent"], startupinfo=stInfo, creationflags=cFlags)
        print "-- %s" % (name)

if __name__ == "__main__":
    cpu = cpu_count() - 0 # You can reduce the load by putting 1 instead of 0 if you need to free 1 core/cpu
    if cpu < 1:
        cpu = 1
    print "I will always maintain %u mmap-extractor tasks running in //\n" % (cpu)
    while (len(mapList) > 0):
        if (threading.active_count() <= cpu):
            workerThread(mapList.popleft()).start()
        time.sleep(0.2)
