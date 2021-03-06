# OctoPrint Particle Publisher Plugin

This is an OctoPrint Plugin that adds support for Particle PubSub publishing to OctoPrint.

OctoPrint will send messages on temperature updates, print progress updates, as well as many OctoPrint events.

## Installation

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager) 
or manually using this URL:

    https://github.com/wgbartley/OctoPrint-ParticlePublisher/archive/master.zip

## Configuration

The only thing that absolutely needs to be configured is the Access Token necessary to access Particle's cloud API. You
can find this in the [Particle Build IDE](https://build.particle.io) settings. Copy and paste the access token into the
"Access Token" input field in the configuration dialog of the Particle Publisher plugin.

By manually editing `config.yaml` it is also possible to adjust the text of the message that will be sent in the messages.

``` yaml
plugins:
  particle_publisher:
    # Particle Access Token for your account
    access_token: your_access_token
    # Optional event name for publish messages
    pubsub_event: 3dprinter
    # Optional API URL for Particle API (in case you are running your own copy of the Particle cloud)
    api_url: https://api.particle.io/v1
```


## Usage

Once configured, you will be able to publish many events to your Particle devices.  You can choose which events
to publish and configure the data sent in each message.  Some defaults have been provided, but you may change
them however you wish.  Just keep in mind that you'll need to be able to parse the messages on your devices, so
a delimited format may be easiest.  The variable replacement is handled by the [Python string format method](https://docs.python.org/2/library/string.html#string.Formatter.format).

A listing of the data available for each event is in the [OctoPrint Available Events documentation](http://docs.octoprint.org/en/master/events/index.html#available-events).
For convenience, the [current printer state data](http://docs.octoprint.org/en/master/api/printer.html#retrieve-the-current-printer-state)
is provided for each event in the `current_data` key.  An example of using `current_data`:
> `Progress|{progress}|{path}|{current_data[state][text]}`


## Disclaimer

This is my first ever real Python project, so there may be bugs or more efficient ways of doing things.  Issues and pull requests are welcomed!
