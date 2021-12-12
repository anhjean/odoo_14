# Copyright 2021 Tecnativa - Alexandre D. Díaz
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo.http import request, route

from .main import PWA


class ServiceWorker(PWA):

    JS_PWA_CORE_EVENT_INSTALL = """
        self.addEventListener('install', evt => {{
            console.log('[ServiceWorker] Installing...');
            {}
        }});
    """

    JS_PWA_CORE_EVENT_FETCH = """
        self.addEventListener('fetch', evt => {{
            {}
        }});
    """

    JS_PWA_CORE_EVENT_ACTIVATE = """
        self.addEventListener('activate', evt => {{
            {}
        }});
    """

    JS_PWA_CORE_EVENT_PUSH = """
        self.addEventListener('push', function(event) {{
            {}
        }});
    """

    JS_PWA_MAIN = """
        self.importScripts(...{pwa_scripts});

        odoo.define("web_pwa_oca.ServiceWorker", function (require) {{
            "use strict";

            {pwa_requires}

            {pwa_init}
            {pwa_core_event_install}
            {pwa_core_event_activate}
            {pwa_core_event_fetch}
            {pwa_core_event_push}
        }});
    """

    def _get_js_pwa_requires(self):
        return """
            const PWA = require('web_pwa_oca.PWA');
        """

    def _get_js_pwa_init(self):
        return """
            const oca_pwa = new PWA({});
        """.format(
            self._get_pwa_params()
        )

    def _get_js_pwa_core_event_install_impl(self):
        return """
            evt.waitUntil(oca_pwa.installWorker());
            self.skipWaiting();
        """

    def _get_js_pwa_core_event_activate_impl(self):
        return """
            console.log('[ServiceWorker] Activating...');
            evt.waitUntil(oca_pwa.activateWorker());
            self.clients.claim();
        """

    def _get_js_pwa_core_event_fetch_impl(self):
        return ""
    
    def _get_js_noti(self):
        return """
            console.log('[Service Worker] Push Received.');
            console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);
            

            const msg = event.data.json();
            console.log(msg);
            const title = msg.notification.title;
            const options = {
            body: msg.notification.body,
            icon: 'images/icon.png',
            badge: 'images/badge.png',
            timestamp: msg.notification.timestamp,
            vibrate: [200, 100, 200, 100, 200, 100, 200],
            tag: 'vibration-sample'
            };
  
            event.waitUntil(self.registration.showNotification(title, options));
        """

    @route("/service-worker.js", type="http", auth="public")
    def render_service_worker(self):
        """Route to register the service worker in the 'main' scope ('/')"""

        sw_code = self.JS_PWA_MAIN.format(
            **{
                "pwa_scripts": self._get_pwa_scripts(),
                "pwa_requires": self._get_js_pwa_requires(),
                "pwa_init": self._get_js_pwa_init(),
                "pwa_core_event_install": self.JS_PWA_CORE_EVENT_INSTALL.format(
                    self._get_js_pwa_core_event_install_impl()
                ),
                "pwa_core_event_activate": self.JS_PWA_CORE_EVENT_ACTIVATE.format(
                    self._get_js_pwa_core_event_activate_impl()
                ),
                "pwa_core_event_fetch": self.JS_PWA_CORE_EVENT_FETCH.format(
                    self._get_js_pwa_core_event_fetch_impl()
                ),
                "pwa_core_event_push": self.JS_PWA_CORE_EVENT_PUSH.format(
                    self._get_js_noti()
                ),
            }
        )
        return request.make_response(
            sw_code,
            [
                ("Content-Type", "text/javascript;charset=utf-8"),
                ("Content-Length", len(sw_code)),
            ],
        )
