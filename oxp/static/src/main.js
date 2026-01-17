/** @odoo-module **/

import { mount, whenReady } from "@odoo/owl";
import { WebClient } from "./webclient/web_client";
import { getTemplate } from "@web/core/templates";

// Mount the WebClient component when the document.body is ready
whenReady(() => {
  mount(WebClient, document.body, {
    getTemplate,
    dev: true,
    name: "OXP Demo App: Web Client",
  });
});