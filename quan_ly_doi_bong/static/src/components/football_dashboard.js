/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class FootballDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            teamCount: 0,
            playerCount: 0,
            matchCount: 0,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const data = await this.orm.searchCount("football.team", []);
        const players = await this.orm.searchCount("football.player", []);
        const matches = await this.orm.searchCount("football.match", []);
        
        this.state.teamCount = data;
        this.state.playerCount = players;
        this.state.matchCount = matches;
    }

    viewTeams() {
        this.action.doAction("quan_ly_doi_bong.action_football_team");
    }

    viewPlayers() {
        this.action.doAction("quan_ly_doi_bong.action_football_player");
    }

    viewMatches() {
        this.action.doAction("quan_ly_doi_bong.action_football_match");
    }
}

FootballDashboard.template = "quan_ly_doi_bong.FootballDashboard";

registry.category("actions").add("football_dashboard_client_action", FootballDashboard);
