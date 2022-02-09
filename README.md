# ConsoleControlSurface

## Description

This is [Python MIDI Remote
Script](https://structure-void.com/ableton-live-midi-remote-scripts/) written
for Ableton Live 11. It enables you to connect remotely to Python interpreter
embedded in Live process and play with
the [Live Object Model](https://docs.cycling74.com/max8/vignettes/live_object_model)
interactively.

## How it works

This script will use Live scheduler to execute code at constant intervals. The
code will use `select()` system call to check if there are any user code coming
over the network to execute in non-blocking manner.

User code is executed in the main (UI) thread. This is desired since this is how
standard remote midi scripts work and there would be problems with
accessing Live objects from other threads. Please have this in mind when executing
long running code as Live will wait for it to finish to continue with normal work.

Network communication is established by opening TCP server socket on
`localhost:8484`.

The REPL will have some useful variables available in the global scope:

- `remote_script` - `MidiRemoteScript.MidiRemoteScript` instance
- `control_surface` - `ConsoleControlSurface.ConsoleControlSurface` instance
- `live_app` - `Live.Application` instance
- `live_set` / `song` - `Song.Song` instance

Note: This project is different than [pylive](https://github.com/ideoforms/pylive), since _pylive_ connects to remote service running in live interpreter
and talking OSC protocol. This is great for general high level communication,
but I believe interacting with interpreter directly is more helpful for
debugging and exploration of remote midi scripts.

## Setup

1. Install remote script into your remote midi scripts directory. I have
   attached a simple shell script `install_macos.sh` for MacOS that will create
   symbolic link in user-specific directory
   `"$HOME/Music/Ableton/User Library/Remote Scripts"`. If that works for you,
   use it. 

2. Restart Live

3. Add `ConsoleControlSurface` as control surface

5. Connect to REPL interpreter:

```shell
telnet localhost 8484
```

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

## Debugging

Check if there are any errors in the Live log file. As noted in
[Where to find Crash Reports](https://help.ableton.com/hc/en-us/articles/209071629-Where-to-find-Crash-Reports)
here are the possible locations of the log file:

- Windows - `\Users\[username]\AppData\Roaming\Ableton\Live x.x.x\Preferences\Log.txt`
- Mac - `/Users/[username]/Library/Preferences/Ableton/Live x.x.x/Log.txt`

## Configuration

You can customize some settings instead of using defaults. You can do this by
creating and editing file `~/.ccsurface.ini`. See `config/ccsurface.ini.example`
on what settings can be customized this way.

## Extra documentation

- [LOM - The Live Object Model](https://docs.cycling74.com/max8/vignettes/live_object_model)
- [Unofficial Live API documentation](https://structure-void.com/PythonLiveAPI_documentation/)
