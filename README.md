# Totem Remote

Plugin for [Totem](https://wiki.gnome.org/Apps/Videos) that allows to control your videos with a web interface.


## Install

	sudo apt install python3-flask

Clone the repository on `/home/username/.local/share/totem/plugins`

	cd ~/.local/share/totem/plugins
    git clone https://github.com/dobladov/totem-remote.git

Or download the [files](https://github.com/dobladov/totem-remote/archive/master.zip) and copy the folder inside `/home/username/.local/share/totem/plugins`

Enable the plugin on Edit --> Preferences --> Plugins

![Plugins](https://my.mixtape.moe/ecwvur.png)

## Usage

Open a video in Totem and load the web interface from the IP address `http://192.168.1.2:8085`

![Interface](https://my.mixtape.moe/wdvdjb.png)


On smartphones the website can be added to the start screen with this logo, both in Chrome and Firefox.

![Logo](https://my.mixtape.moe/ikaflp.png)

## ToDo

- [ ] Set Volume
- [ ] Toggle Sound
- [ ] Toggle Fullscreen

## Documentation

+ [Totem Reference Manual](https://developer.gnome.org/totem/stable/)
+ [Writing Plugins for Totem Movie Player](http://asanka-abeyweera.blogspot.com.es/2012/03/writing-plugins-for-totem-movie-player.html)
+ [Flask docs](http://flask.pocoo.org/docs/0.10/)

---

![Remote](https://my.mixtape.moe/gpqwxi.gif)
