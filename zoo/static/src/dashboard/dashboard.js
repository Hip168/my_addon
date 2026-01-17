/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class ZooDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            stats: {
                species: { count: 0, list: [] },
                cages: { count: 0, list: [] },
                animals: { count: 0, list: [] },
            },
        });

        onWillStart(async () => {
            await this.loadStats();
        });
    }

    async loadStats() {
        const [species, cages, animals] = await Promise.all([
            this.orm.searchRead("animal.species", [], ["name"]),
            this.orm.searchRead("cage", [], ["name"]),
            this.orm.searchRead("animal.base", [], ["name"]),
        ]);

        this.state.stats = {
            species: { count: species.length, list: species },
            cages: { count: cages.length, list: cages },
            animals: { count: animals.length, list: animals },
        };
    }

    openView(model, name) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: name,
            res_model: model,
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

ZooDashboard.template = "zoo.ZooDashboard";
registry.category("actions").add("zoo.dashboard_client_action", ZooDashboard);
