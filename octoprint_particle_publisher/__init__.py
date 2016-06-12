# coding=utf-8
from __future__ import absolute_import

__author__ = "wgbartley <wgbartley@gmail.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Released under terms of the AGPLv3 License"

import os
import requests

import octoprint.plugin
from octoprint.events import Events


class ParticlePublisherCallback(octoprint.plugin.SettingsPlugin, octoprint.printer.PrinterCallback):
	def __init__(self, access_token, pubsub_event, api_url, temperature_format, temperature_enabled, printer):
		self._access_token = access_token
		self._pubsub_event = pubsub_event
		self._api_url = api_url
		self._temperature_format = temperature_format
		self._temperature_enabled = temperature_enabled
		self._printer = printer

	##-- Printer temperature
	def on_printer_add_temperature(self, data):
		data.update({'current_data': self._printer.get_current_data()})

		if self._temperature_enabled:
			self._publish(self._temperature_format.format(**data))

	def _publish(self, data):
		data = data.replace(": ", ":")
		data = data.replace(", ", ",")

		headers = {'Authorization': 'Bearer '+self._access_token}
		payload = {'name':self._pubsub_event, 'data':data, 'private':'true'}

		r = requests.post(self._api_url+"/devices/events", data=payload, headers=headers)


class ParticlePublisherPlugin(octoprint.plugin.EventHandlerPlugin,
			octoprint.plugin.SettingsPlugin,
			octoprint.plugin.StartupPlugin,
			octoprint.plugin.TemplatePlugin,
			octoprint.plugin.ProgressPlugin,
			octoprint.printer.PrinterInterface
			):


	def __init__(self):
		self._ok = False


	def _connect_publisher(self):
		try:
			api_url = self._settings.get(["api_url"])
			access_token = self._settings.get(["access_token"])

			r = requests.get(api_url+"/devices", headers={'Authorization': 'Bearer '+access_token})
			self._logger.info("Connected to Particle: "+str(r.status_code))
			if r.ok:
				self._ok = r.ok

			return True
		except:
			self._logger.exception("Error while instantiating Particle Publisher")
			return False


	#~~ StartupPlugin
	def on_after_startup(self):
		self._logger.info("Particle Publisher plugin loaded")
		self._connect_publisher()

		if self._ok:
			access_token = self._settings.get(["access_token"])
			pubsub_event = self._settings.get(["pubsub_event"])
			api_url = self._settings.get(["api_url"])
			temperature_format = self._settings.get(["temperature_format"])
			temperature_enabled = self._settings.get(["temperature_enabled"])

			self._callback = ParticlePublisherCallback(access_token, pubsub_event, api_url, temperature_format, temperature_enabled, self._printer)
			self._printer.register_callback(self._callback)


	#~~ SettingsPlugin
	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		if hasattr(self, '_callback'):
			self._printer.unregister_callback(self._callback)

		self.on_after_startup()


	def get_settings_defaults(self):
		return dict(
			access_token = None,
			pubsub_event = "3dprinter",
			api_url = "https://api.particle.io/v1",

			temperature_format = "Temperature|{tool0[actual]}|{tool0[target]}|{bed[actual]}|{bed[target]}",
			temperature_enabled = True,

			progress_format = "Progress|{storage}|{path}|{progress}",
			progress_enabled = True,

			events_startup_enabled = False,
			events_startup_format = "StartUp",

			events_connected_enabled = False,
			events_connected_format = "Connected|{port}|{baudrate}",

			events_disconnected_enabled = False,
			events_disconnected_format = "Disconnected",

			events_clientopened_enabled = False,
			events_clientopened_format = "ClientOpened|{remoteAddress}",

			events_clientclosed_enabled = False,
			events_clientclosed_format = "ClientClosed|{remoteAddress}",

			events_upload_enabled = False,
			events_upload_format = "Upload|{file}|{target}",

			events_fileselected_enabled = False,
			events_fileselected_format = "FileSelected|{file}|{filename}|{origin}",

			events_filedeselected_enabled = False,
			events_filedeselected_format = "FileDeselected",

			events_updatedfiles_enabled = False,
			events_updatedfiles_format = "UpdatedFiles|{type}",

			events_metadataanalysisstarted_enabled = False,
			events_metadataanalysisstarted_format = "MetadataAnalysisStarted|{file}",

			events_metadataanalysisfinished_enabled = False,
			events_metadataanalysisfinished_format = "MetadataAnalysisFinished|{file}",

			events_metadatastatisticsupdated_enabled = False,
			events_metadatastatisticsupdated_format = "MetadataStatisticsUpdated",

			events_transferstarted_enabled = False,
			events_transferstarted_format = "TransferStarted|{local}|{remote}",

			events_transferdone_enabled = False,
			events_transferdone_format = "TransferDone|{time}|{local}|{remote}",

			events_printstarted_enabled = False,
			events_printstarted_format = "PrintStarted|{file}|{origin}",

			events_printdone_enabled = False,
			events_printdone_format = "PrintDone|{file}|{origin}|{time}",

			events_printfailed_enabled = False,
			events_printfailed_format = "PrintFailed|{file}|{origin}",

			events_printcancelled_enabled = False,
			events_printcancelled_format = "PrintCancelled|{file}|{origin}",

			events_printpaused_enabled = False,
			events_printpaused_format = "PrintPaused|{file}|{origin}",

			events_printresumed_enabled = False,
			events_printresumed_format = "PrintResumed|{file}|{origin}",

			events_error_enabled = False,
			events_error_format = "Error|{error}",

			events_poweron_enabled = False,
			events_poweron_format = "PowerOn",

			events_poweroff_enabled = False,
			events_poweroff_format = "PowerOff",

			events_home_enabled = False,
			events_home_format = "Home",

			events_zchange_enabled = False,
			events_zchange_format = "ZChange|{new}|{old}",

			events_waiting_enabled = False,
			events_waiting_format = "Waiting",

			events_dwell_enabled = False,
			events_dwell_format = "Dwell",

			events_cooling_enabled = False,
			events_cooling_format = "Cooling",

			events_alert_enabled = False,
			events_alert_format = "Alert",

			events_conveyor_enabled = False,
			events_conveyor_format = "Conveyor",

			events_eject_enabled = False,
			events_eject_format = "Eject",

			events_estop_enabled = False,
			events_estop_format = "EStop",

			events_registeredmessagereceived_enabled = False,
			events_registeredmessagereceived_format = "RegisteredMessageReceived",

			events_capturestart_enabled = False,
			events_capturestart_format = "CaptureStart|{file}",

			events_capturedone_enabled = False,
			events_capturedone_format = "CaptureDone|{file}",

			events_capturefailed_enabled = False,
			events_capturefailed_format = "CaptureFailed",

			events_postrollstart_enabled = False,
			events_postrollstart_format = "PostRollStart",

			events_postrollend_enabled = False,
			events_postrollend_format = "PostRollEnd",

			events_movierendering_enabled = False,
			events_movierendering_format = "MovieRendering|{gcode}|{movie}|{movie_basename}",

			events_moviedone_enabled = False,
			events_moviedone_format = "MovieDone|{gcode}|{movie}|{movie_basename}",

			events_moviefailed_enabled = False,
			events_moviefailed_format = "MovieFailed|{gcode}|{movie}|{movie_basename}|{returncode}",

			events_slicingstarted_enabled = False,
			events_slicingstarted_format = "SlicingStarted|{stl}|{gcode}|{progressAvailable}",

			events_slicingdone_enabled = False,
			events_slicingdone_format = "SlicingDone|{stl}|{gcode}|{time}",

			events_slicingfailed_enabled = False,
			events_slicingfailed_format = "SlicingFailed|{stl}|{gcode}|{reason}",

			events_slicingcancelled_enabled = False,
			events_slicingcancelled_format = "SlicingCancelled|{stl}|{gcode}",

			events_settingsupdated_enabled = False,
			events_settingsupdated_format = "SettingsUpdated"
		)


	#~~ TemplatePlugin API
	def get_template_configs(self):
		return [
			dict(type="settings", name="Particle Publisher", custom_bindings=False)
		]


	#~~ EventHandlerPlugin
	def on_event(self, event, payload):
		if payload is None:
			payload = dict()

		payload.update({'current_data': self._printer.get_current_data()})

		this_event_enabled = self._settings.get(["events_"+event.lower()+"_enabled"])
		this_event_format = str(self._settings.get(["events_"+event.lower()+"_format"]))

		if self._ok and this_event_enabled:
			if payload is not None:
				self._publish(this_event_format.format(**payload))
			else:
				self._publish(this_event_format.format(**current_data))


	def on_print_progress(self, storage, path, progress):
		data = dict(
			storage = storage,
			path = path,
			progress = progress,
			current_data = self._printer.get_current_data()
		)

		if self._settings.get(["progress_enabled"]):
			self._publish(self._settings.get(["progress_format"]).format(**data))


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

		api_url = self._settings.get(["api_url"])
		access_token = self._settings.get(["access_token"])
		pubsub_event = self._settings.get(["pubsub_event"])

		headers = {'Authorization': 'Bearer '+access_token}
		payload = {'name': pubsub_event, 'data':data, 'private':'true'}

		r = requests.post(api_url+"/devices/events", data=payload, headers=headers)



__plugin_name__ = "ParticlePublisher"
def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ParticlePublisherPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

