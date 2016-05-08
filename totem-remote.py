# -*- coding: utf-8 -*-

from gi.repository import GObject, Peas
from flask import Flask, render_template, jsonify
from threading import Thread
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path='/static')

class StarterPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'StarterPlugin'

    object = GObject.property (type = GObject.Object)

    def __init__ (self):
        GObject.Object.__init__ (self)
        self._totem = None
        print("Plugin Totem-Remote started")

    def do_deactivate (self):
        self._totem = None
        print("Plugin Totem-Remote disabled")
        
    def do_activate (self):
        self._totem = self.object
 
        @app.route("/")
        def home():
            return render_template('home.html')

        @app.route("/togglePlay")
        def togglePlay():
            self._totem.play_pause()
            return jsonify(playing = True if self._totem.is_playing() else False)
            
        @app.route("/next")
        def next():
            self._totem.seek_next()
            return jsonify(info="Playing the next")

        @app.route("/previous")
        def previous():
            self._totem.seek_previous()
            return jsonify(info="Playing the previous")


        @app.route("/toggleFullscreen")
        def toggleFullscreen():
            os.system('totem --fullscreen')
            return jsonify(info="Toggled fullscreen")


        @app.route("/exit")
        def exit():
            self._totem.exit()
            return jsonify(info='Close Totem')


        @app.route("/seekTime/<time>")
        def seekTime(time):
            # print(self._totem.get_property('current_time'))
            self._totem.seek_time(int(time), False)   
            return jsonify(currentTime = self._totem.get_property('current_time'))


        # @app.route("/seekRelative/<time>")
        # def seekRelative(time):
        #     # print(self._totem.get_property('current_time'))
        #     self._totem.seek_relative(int(time), False)       
        #     return 'Move relative to time: ' + time


        @app.route("/info")
        def info():
            info = {}
            info['name'] = self._totem.get_property('current-display-name')
            info['mrl'] = self._totem.get_property('current-mrl')
            info['time'] = self._totem.get_property('current_time')
            info['playing'] = self._totem.get_property('playing')
            info['length'] = self._totem.get_property('stream-length')
            info['seekable'] = self._totem.get_property('seekable')
            info['fullscreen'] = self._totem.get_property('fullscreen')
            info['volume'] = self._totem.get_volume()

            # print(info)
            return jsonify(info)


        @app.route("/volumeUp")
        def volumeUp():
            os.system('totem --volume-up')
            return jsonify(info='Volume UP')


        @app.route("/volumeDown")
        def volumeDown():
            os.system('totem --volume-down')
            return jsonify(info='Volume Down')


        @app.route("/seekFWD")
        def seekFWD():
            os.system('totem --seek-fwd')
            return jsonify(info='Seek Forward')

        @app.route("/seekBWD")
        def seekBWD():
            os.system('totem --seek-bwd')
            return jsonify(info='Seek Backwards')


        @app.route("/toggleMute")
        def toggleMute():
            sound = self._totem.get_volume()

            if (sound > 0):
                os.system('totem --mute')
            else:
                os.system('totem --volume-up')
            
            return jsonify(sound=sound)


        t = Thread(name='flaskServer', target=app.run, kwargs={'port':8085, 'host':'0.0.0.0'})
        t.start();

        print("Plugin Totem-Remote enabled")

