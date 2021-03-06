# This module requires katana framework 
# https://github.com/PowerScript/KatanaFramework

# :-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-: #
# Katana Core import                  #
from core.KatanaFramework import *    #
# :-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-: #

# LIBRARIES  
from bs4 import BeautifulSoup
import httplib                
# END LIBRARIES 

# INFORMATION MODULE
def init():
	init.Author             ="RedToor"
	init.Version            ="2.0"
	init.Description        ="Administrator Panel finder, Brute Force + Google Dork + Port Scan."
	init.CodeName           ="web/cp.finder"
	init.DateCreation       ="28/09/2015"      
	init.LastModification   ="25/12/2016"
	init.References         =None
	init.License            =KTF_LINCENSE
	init.var                ={}

	# DEFAULT OPTIONS MODULE
	init.options = {
		# NAME    VALUE                RQ     DESCRIPTION
		'target':[LOCAL_IP           ,True , 'Host Target'],
		'port'  :[HTTP_PORT          ,False, 'Port Target'],
		'file'  :[TABLE_FOLDER_ADMIN ,False, 'Tables URL']
	}
	return init
# END INFORMATION MODULE

# CODE MODULE    ############################################################################################
def main(run):
	NET.CheckConnectionHost(init.var['target'],init.var['port'],5)
	Loadingfile(init.var['file'])
	Totalresults=""

	printk.step("[1] Step : Starting Brute Force...")
	with open(init.var['file'],'r') as list_path:
		for path in list_path:
			path="/"+path.replace("\n","")
			if init.var['port'] == "443" : 
				connection = httplib.HTTPSConnection(init.var['target'])
			else : connection = httplib.HTTPConnection(init.var['target'],int(init.var['port']))
			connection.addheaders=[('User-agent', WEB.RamdonAgent())]
			connection.request("GET",path)
			response = connection.getresponse()

			if response.status == 200 or response.status == 301:
				printk.suff(" | Response "+init.var['target']+path)
				Totalresults+="\t|"+init.var['target']+path+"\n"
			else:printk.inf(" | Checking `"+colors[0]+path+"` Response:"+str(response.status))
			
	printk.step("[2] Step : Starting Google Dorking...")
	connection = httplib.HTTPSConnection("www.google.com.ru")
	connection.request("GET", "/search?q=inurl:admin+site:"+str(init.var['target']))
	connection.addheaders=[('User-agent', WEB.RamdonAgent())]
	response = connection.getresponse()
	soup = BeautifulSoup(response.read(), "lxml")
	divList = soup.findAll('cite')
	for ids in divList:
		printk.suff("| Result  "+ids.text)
		Totalresults+="\t | "+ids.text+"\n"

	printk.step("[3] Step : Scanning Port commons...")
	commonports = [2082,2083,2095,2096]
	for port in commonports:
		printk.inf(" | Testing Port "+str(port))
		if NET.CheckConnectionHost(init.var['target'],port,5):
			printk.suff(" | "+str(port)+" Port Open!")
			Totalresults+="\t|"+str(port)+" Open! \n"

	printk.inf("[*] Total Result")
	print Totalresults
	UTIL.sRegister(init,Totalresults)

# END CODE MODULE ############################################################################################
