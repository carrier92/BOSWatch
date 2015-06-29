#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Functions to Load and import the Plugins

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import imp
import os

from ConfigParser import NoOptionError # we need this exception
from includes import globals  # Global variables

def loadPlugins():
	"""
	Load all Plugins into globals.pluginList

	@return:    nothing
	@exception: Exception if insert into globals.pluginList failed
	"""
	try:
		logging.debug("loading plugins")
		# go to all Plugins from getPlugins()
		for i in getPlugins():
			# call for each Plugin the loadPlugin() Methode
			plugin = loadPlugin(i)
			# Try to call the .onLoad() routine for all active plugins
			try:
				logging.debug("call %s.onLoad()", i["name"])
				plugin.onLoad()
				# Add it to globals.pluginList
				globals.pluginList[i["name"]] = plugin	
			except:
				# call next plugin, if one has thrown an exception
				logging.error("error calling %s.onLoad()", i["name"])
				logging.debug("error calling %s.onLoad()", exc_info=True)
				pass
	except:
		logging.error("cannot load Plugins")
		logging.debug("cannot load Plugins", exc_info=True)
		raise


def getPlugins():
	"""
	get a Python Dict of all activeated Plugins

	@return:    Plugins as Python Dict
	@exception: Exception if Plugin search failed
	"""
	try:
		logging.debug("Search in Plugin Folder")
		PluginFolder = globals.script_path+"/plugins"
		plugins = []
		# Go to all Folders in the Plugin-Dir
		for i in os.listdir(PluginFolder):
			location = os.path.join(PluginFolder, i)
				
			# Skip if Path.isdir() or no File DIR_NAME.py is found 
			if not os.path.isdir(location) or not i + ".py" in os.listdir(location):
				continue

			# is the plugin enabled in the config-file?
			try: 
				if globals.config.getint("Plugins", i):
					info = imp.find_module(i, [location])
					plugins.append({"name": i, "info": info})
					logging.debug("Plugin [ENABLED ] %s", i)
				else:
					logging.debug("Plugin [DISABLED] %s ", i)
			# no entry for plugin found in config-file
			except NoOptionError: 
				logging.warning("Plugin [NO CONF ] %s", i)				
				pass
	except:
		logging.error("Error during Plugin search")
		logging.debug("cannot load Plugins", exc_info=True)
		raise

	return plugins


def loadPlugin(plugin):
	"""
	Imports a single Plugin

	@type    plugin: Plugin Data
	@param   plugin: Contains the information to import a Plugin
	
	
	@return:    nothing
	@exception: Exception if Plugin import failed
	"""
	try:
		logging.debug("load Plugin: %s", plugin["name"])
		return imp.load_module(plugin["name"], *plugin["info"])
	except:
		logging.error("cannot load Plugin: %s", plugin["name"])
		logging.debug("cannot load Plugin: %s", plugin["name"], exc_info=True)
		raise