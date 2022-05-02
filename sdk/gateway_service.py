import eventlet
import eventlet.wsgi
import socketio
from decouple import config
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
import json

PORT = config("PORT", default=3001, cast=int)

class GatewayService:
    def __init__(self):
        self.sio = self.__get_socket_io()
        self.app = self.__get_web_app()
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
        self.controllers = []

    def __get_socket_io(self):
        sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

        @sio.event
        def connect(sid, environ, auth):
            for controller in self.controllers:
                controller.on_connect(sid)

        @sio.on('client-state-changed')
        def on_client_state_changed(sid, data):
            for controller in self.controllers:
                controller.on_client_state_changed(sid, json.loads(data))

        return sio

    def __get_web_app(self):
        app = Flask("__main__")
        CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

        @app.route('/static/<path:path>')
        @cross_origin
        def meta(path):
            return send_from_directory("static", path)

        return app

    def listen(self):
        eventlet.wsgi.server(eventlet.listen(('', PORT)), self.app)

    def add_controller(self, controller):
        self.controllers.append(controller)