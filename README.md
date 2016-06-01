# OctoPrint Particle Publisher Plugin

This is an OctoPrint Plugin that adds support for Particle PubSub publishing to OctoPrint.

OctoPrint will send messages on temperature updates as well (but not all) as many OctoPrint events.

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

