# coding=utf-8
from __future__ import absolute_import

__author__ = "wgbartley <wgbartley@gmail.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Released under terms of the AGPLv3 License"

import os
import requests

import octoprint.plugin
from octoprint.events import Events

import octoprint.printer


class ParticlePublisherCallback(octoprint.printer.PrinterCallback):
	def __init__(self, access_token, pubsub_event, api_url):
		self._access_token = access_token
		self._pubsub_event = pubsub_event
		self._api_url = api_url

	##-- Printer temperature
	def on_printer_add_temperature(self, data):
		self._publish("Temperature|"+str(data))

	def _publish(self, data):
		data = str(data)
		data = data.replace(": ", ":")
		data = data.replace(", ", ",")

		headers = {'Authorization': 'Bearer '+self._access_token}
		payload = {'name':self._pubsub_event, 'data':data, 'private':'true'}

		r = requests.post(self._api_url+"/devices/events", data=payload, headers=headers)


class ParticlePublisherPlugin(octoprint.plugin.EventHandlerPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin):


	def __init__(self):
		self._ok = False
		self._access_token = None
		self._pubsub_event = "3dprinter"
		self._api_url = "https://api.particle.io/v1"

	def _connect_publisher(self):
		try:
			r = requests.get(self._api_url+"/devices", headers={'Authorization': 'Bearer '+self._access_token})
			self._logger.info("Connected to Particle: "+str(r.status_code))
			if r.ok:
				self._ok = r.ok

			return True
		except:
			self._logger.exception("Error while instantiating ParticlePublisher")
			return False


	#~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info("Particle Publisher plugin loaded")
		self._access_token = self._settings.get(["access_token"])
		self._pubsub_event = self._settings.get(["pubsub_event"])
		self._api_url = self._settings.get(["api_url"])
		self._connect_publisher()

		if self._ok:
			callback = ParticlePublisherCallback(self._access_token, self._pubsub_event, self._api_url)
			self._printer.register_callback(callback)


	#~~ SettingsPlugin
	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		import threading
		thread = threading.Thread(target=self._connect_publisher)
		thread.daemon = True
		thread.start()


	def get_settings_defaults(self):
		return dict(
			access_token = None,
			pubsub_event = "3dprinter",
			api_url = "https://api.particle.io/v1"
		)


	#~~ TemplatePlugin API
	def get_template_configs(self):
		return [
			dict(type="settings", name="Particle Publisher", custom_bindings=False)
		]


	def on_print_progress(self, path, progress):
		#if self._ok:
		print ">>> "+path+" "+progress
		self._publish("progress|"+str(payload))


	#~~ EventHandlerPlugin
	def on_event(self, event, payload):
		if event == Events.Z_CHANGE:
			return
		if event == Events.HOME:
			return

		if self._ok:
			self._publish(event+"|"+str(payload))


	##~~ Softwareupdate hook
	def get_update_information(self):
		return dict(
			particle_publisher=dict(
				displayName="Particle Publisher Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-ParticlePublisher",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/wgbartley/OctoPrint-ParticlePublisher/archive/{target_version}.zip"
			)
		)

	def _publish(self, data):
		data = str(data)
		data = data.replace(": ", ":")
		data = data.replace(", ", ",")

		headers = {'Authorization': 'Bearer '+self._access_token}
		payload = {'name':self._pubsub_event, 'data':data, 'private':'true'}

		r = requests.post(self._api_url+"/devices/events", data=payload, headers=headers)



__plugin_name__ = "ParticlePublisher"
def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ParticlePublisherPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

