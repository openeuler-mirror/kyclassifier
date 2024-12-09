import psutil
import sys
import os

from src.log.logger import logger

def find_processes_with_cmdline_keyword(keyword):

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if keyword in ' '.join(cmdline).lower() and proc.info['pid'] != os.getpid():
                #print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Cmdline: {' '.join(cmdline)}")
                logger.error("Another kyclassifier process is running, the pid = %s " %proc.info['pid'])
                sys.exit(-1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.error("Encountered an exception for PID {proc.info.get('pid', 'unknown')}: {e}")