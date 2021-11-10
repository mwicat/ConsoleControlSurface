# ConsoleControlSurface

## Description

This remote midi script runs remote console (REPL) thread in ableton python
intepreter process (utilizing [ingress](https://github.com/tebeka/ingress) module).

It makes possible to connect remotely to
python interpreter and interact with Live Object Model interactively.

It also exports some useful objects into global scope:

- `remote_script` - `MidiRemoteScript.MidiRemoteScript` instance
- `control_surface` - `ConsoleControlSurface.ConsoleControlSurface` instance
- `song` - `Song.Song` instance

Note: This is different than [pylive](https://github.com/ideoforms/pylive) project as _pylive_ connects to
remote service running in live interpreter and talking OSC protocol. This is great for general high level communication,
but I believe interacting with interpreter directly is more helpful for debugging and exploration.

## Setup

1. Install scripts into ableton remote midi scripts directory. It creates symbolic link to this repository package
in Live 10 global remote script directory (needs sudo). If you don't want this, just copy ConsoleControlSurface to
remote midi script directory.

```
./install_osx.sh
```

2. Restart Ableton

3. Add ConsoleControlSurface as control surface

4. (Optionally) check in log that everything runs fine

5. Attach to REPL interpreter

```
telnet localhost 8484
```

It make some time to initialize, but should run ok afterwards. 

6. Explore!

Some examples:

```python
>>> song
<Song.Song object at 0x1287190d8>
>>> [t.name for t in song.tracks]
['1-Audio', '2-Audio', '3-Audio', '4-Audio', '5-Audio', '6-Audio', '7-Audio', '8-Audio', '9-Audio', '10-Audio', '11-Drum Rack', '12-Drum Rack', '13-Drum Rack', '14-Drum Rack', '15-Drum Rack', '16-Drum Rack', '17-Drum Rack', '18-Drum Rack', '19-MIDI', '20 Record']
>>> dev = song.tracks[0].devices[0]
>>> dev.name
u'Utility'
>>> dev.parameters
<Device.ATimeableValueVector object at 0x1286dce50>
>>> list(dev.parameters)
[<DeviceParameter.DeviceParameter object at 0x128719ea8>,
 <DeviceParameter.DeviceParameter object at 0x128719d98>,
 <DeviceParameter.DeviceParameter object at 0x128719d10>,
 <DeviceParameter.DeviceParameter object at 0x128719c88>,
 <DeviceParameter.DeviceParameter object at 0x128719c00>,
 <DeviceParameter.DeviceParameter object at 0x128719b78>,
 <DeviceParameter.DeviceParameter object at 0x128719e20>,
 <DeviceParameter.DeviceParameter object at 0x128719848>,
 <DeviceParameter.DeviceParameter object at 0x128719738>,
 <DeviceParameter.DeviceParameter object at 0x128719518>,
 <DeviceParameter.DeviceParameter object at 0x1287199e0>,
 <DeviceParameter.DeviceParameter object at 0x128719490>]
>>> dev.parameters[0]
<DeviceParameter.DeviceParameter object at 0x128719ea8>
>>> p = dev.parameters[0]
>>> dir(p)
['__class__',
 '__delattr__',
 '__dict__',
 '__doc__',
 '__eq__',
 '__format__',
 '__getattribute__',
 '__hash__',
 '__init__',
 '__module__',
 '__ne__',
 '__new__',
 '__nonzero__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__weakref__',
 '_live_ptr',
 'add_automation_state_listener',
 'add_name_listener',
 'add_state_listener',
 'add_value_listener',
 'automation_state',
 'automation_state_has_listener',
 'begin_gesture',
 'canonical_parent',
 'default_value',
 'end_gesture',
 'is_enabled',
 'is_quantized',
 'max',
 'min',
 'name',
 'name_has_listener',
 'original_name',
 're_enable_automation',
 'remove_automation_state_listener',
 'remove_name_listener',
 'remove_state_listener',
 'remove_value_listener',
 'state',
 'state_has_listener',
 'str_for_value',
 'value',
 'value_has_listener',
 'value_items']
>>> p.name
u'Device On'
>>> p.value = 0
```

## Extra documentation

- [LOM - The Live Object Model](https://docs.cycling74.com/max8/vignettes/live_object_model)
- [Unofficial Live API documentation](https://structure-void.com/PythonLiveAPI_documentation/)
