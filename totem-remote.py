# -*- coding: utf-8 -*-

from gi.repository import GObject, Peas
from flask import Flask, render_template, jsonify
# from flask import Flask, render_template, jsonify, request, Response
from threading import Thread
# from functools import wraps
from yaml import load
import os

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__, static_url_path='/static')

class StarterPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'TotemRemote'

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
        
        with open(self.plugin_info.get_data_dir() + "/config.yml", 'r') as ymlfile:
            self.cfg = load(ymlfile)

        # def check_auth(username, password):
        #     return username == self.cfg["access"]["user"] and password == self.cfg["access"]["pass"]

        # def authenticate():
        #     return Response('Could not verify your credentials', 401,
        #         {'WWW-Authenticate': 'Basic realm="Login Required"'})

        # def requires_auth(f):
        #     @wraps(f)
        #     def decorated(*args, **kwargs):
        #         auth = request.authorization
        #         if not auth or not check_auth(auth.username, auth.password):
        #             return authenticate()
        #         return f(*args, **kwargs)
        #     return decorated
 
        @app.route("/")
        # @requires_auth
        def home():
            return render_template('home.html')


        @app.route("/togglePlay")
        # @requires_auth
        def togglePlay():
            self._totem.play_pause()
            return jsonify(playing = True if self._totem.is_playing() else False)
          

        @app.route("/next")
        # @requires_auth
        def next():
            self._totem.seek_next()
            return jsonify(info="Playing the next")


        @app.route("/previous")
        # @requires_auth
        def previous():
            self._totem.seek_previous()
            return jsonify(info="Playing the previous")


        @app.route("/toggleFullscreen")
        # @requires_auth
        def toggleFullscreen():
            os.system('totem --fullscreen')
            # return jsonify(info="Toggled fullscreen")
            return jsonify(fullscreen = True if self._totem.get_property('fullscreen') else False)



        @app.route("/exit")
        # @requires_auth
        def exit():
            self._totem.exit()
            return jsonify(info='Close Totem')


        @app.route("/seekTime/<time>")
        # @requires_auth
        def seekTime(time):
            self._totem.seek_time(int(time), False)   
            return jsonify(currentTime = self._totem.get_property('current_time'))


        @app.route("/info")
        # @requires_auth
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
        # @requires_auth
        def volumeUp():
            os.system('totem --volume-up')
            return jsonify(volume = self._totem.get_volume())


        @app.route("/volumeDown")
        # @requires_auth
        def volumeDown():
            os.system('totem --volume-down')
            return jsonify(volume = self._totem.get_volume())


        @app.route("/seekFWD")
        # @requires_auth
        def seekFWD():
            os.system('totem --seek-fwd')
            return jsonify(time = self._totem.get_property('current_time'), length = self._totem.get_property('stream-length'))


        @app.route("/seekBWD")
        # @requires_auth
        def seekBWD():
            os.system('totem --seek-bwd')
            return jsonify(time = self._totem.get_property('current_time'), length = self._totem.get_property('stream-length'))


        @app.route("/toggleMute")
        # @requires_auth
        def toggleMute():
            sound = self._totem.get_volume()

            if (sound > 0):
                os.system('totem --mute')
            else:
                os.system('totem --volume-up')
            
            return jsonify(sound=sound)


        t = Thread(name='flaskServer', target=app.run, kwargs={'port':self.cfg["server"]["port"], 'host':self.cfg["server"]["host"]})
        t.start();

        print("Plugin Totem-Remote enabled")