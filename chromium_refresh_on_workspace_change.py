#!/usr/bin/env python3
import subprocess
import keyboard
import time
from time import sleep
from chromote import Chromote
import select
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=int)
args = parser.parse_args()

if(getattr(args,'workspace') == None):
    event_triggered_on_this_workspace = 2
else:
    event_triggered_on_this_workspace = getattr(args,'workspace')

chrome = Chromote()
tab = chrome.tabs[0]
previous_workspace = 0

def get_res():
    # get resolution
    xr = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    pos = xr.index("current")
    return [int(xr[pos+1]), int(xr[pos+3].replace(",", "") )]

def current_workspace():
    # get the resolution (viewport size)
    res = get_res()
    # read wmctrl -d
    vp_data = subprocess.check_output(
        ["wmctrl", "-d"]
        ).decode("utf-8").split()
    # get the size of the spanning workspace (all viewports)
    dt = [int(n) for n in vp_data[3].split("x")]
    # calculate the number of columns
    cols = int(dt[0]/res[0])
    # calculate the number of rows
    rows = int(dt[1]/res[1])
    # get the current position in the spanning workspace
    curr_vpdata = [int(n) for n in vp_data[5].split(",")]
    # current column (readable format)
    curr_col = int(curr_vpdata[0]/res[0])
    # current row (readable format)
    curr_row = int(curr_vpdata[1]/res[1])
    # calculate the current viewport
    return curr_col+curr_row*cols+1;

#print(current())
def refresh_browser():
#if current() == 2:
    tab.reload()

f = subprocess.Popen('dbus-monitor',stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
p = select.poll()
p.register(f.stdout)

while True:
    line = f.stdout.readline()
    #if p.poll(1):
        #print("a")
        
        #print(line)
    if b'member=ActiveWindow' in line:        
        workspace = current_workspace()        
        if previous_workspace != workspace:
            if workspace == event_triggered_on_this_workspace:            
                refresh_browser()
        previous_workspace = workspace       

#chromium-browser --remote-debugging-port=9222