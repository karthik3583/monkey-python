import os
import time

import subprocess as sub

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.firefox.options import Options

#import settings
#from util import motifcore_installer
#from util import pack_and_deploy


def open_browser(url):
	'''Will open the browser'''
	driver = webdriver.Firefox()
	driver.maximize_window()
	try:
		driver.get(url)
		'''driver.execute_script("var s=window.document.createElement('script');\
								s.setAttribute(\"type\", \"text/javascript\");\
								s.setAttribute(\"src\", \"https://raw.githubusercontent.com/marmelab/gremlins.js/master/gremlins.min.js\");\
								window.document.getElementsByTagName(\"head\")[0].appendChild(s);")'''
		driver.execute_script(open("./gremlins.js").read())
		driver.execute_script("var horde = gremlins.createHorde();\
							   horde.unleash();")
		
	except Exception as e:
		print(e)
		driver.close()
def get_devices():
	""" will also get devices ready
	:return: a list of avaiable devices names, e.g., emulator-5556
	"""
	ret = []
	p = sub.Popen('adb devices', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
	output, errors = p.communicate()
	#print output
	segs = output.split("\n")
	for seg in segs:
		device = seg.split("\t")[0].strip()
		# if seg.startswith("emulator-"):
		if not seg.startswith("List") and seg != "\r" and seg != "":
			p = sub.Popen('adb -s ' + device + ' shell getprop init.svc.bootanim', stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
			output, errors = p.communicate()
			tmp_str = output.strip()
			if output.strip() != "stopped":
				time.sleep(10)
				#print "waiting for the emulator:", device
				return get_devices()
			else:
				ret.append(device)

	assert len(ret) > 0

	return ret


def boot_devices():
	"""
	prepare the env of the device
	:return:
	"""
	for i in range(0, settings.DEVICE_NUM):
		device_name = settings.AVD_SERIES + str(i)
		#print "Booting Device:", device_name
		time.sleep(0.3)
		if settings.HEADLESS:
			sub.Popen('emulator -avd ' + device_name + " -wipe-data -no-audio -no-window",
					  stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
		else:
			sub.Popen('emulator -avd ' + device_name + " -wipe-data -no-audio",
					  stdout=sub.PIPE, stderr=sub.PIPE, shell=True)

	#print "Waiting", settings.AVD_BOOT_DELAY, "seconds"
	time.sleep(settings.AVD_BOOT_DELAY)


def clean_sdcard():
	for device in get_devices():
		os.system("adb -s " + device + " shell mount -o rw,remount rootfs /")
		os.system("adb -s " + device + " shell chmod 777 /mnt/sdcard")

		os.system("adb -s " + device + " shell rm -rf /mnt/sdcard/*")


def prepare_motifcore():
	for device in get_devices():
		motifcore_installer.install(settings.WORKING_DIR + "lib/motifcore.jar", settings.WORKING_DIR + "resources/motifcore", device)


def pack_and_deploy_aut():
	# instrument the app under test
	pack_and_deploy.main(get_devices())


def destory_devices():
	# for device in get_devices():
	# 	os.system("adb -s " + device + " emu kill")
	# do force kill
	os.system("kill -9  $(ps aux | grep 'emulator' | awk '{print $2}')")


if __name__ == "__main__":
	open_browser('http://www.google.com')