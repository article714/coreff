odoo.define('coreff_creditsafe.create_from_button', function (require){
"use strict";
 
 
var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb; 
 
 
ListView.include({       
     
        render_buttons: function($node) {
                var self = this;
                this._super($node);
                    this.$buttons.find('.o_create_from_creditsafe').click(this.proxy('create_from_action'));
        },
 
        create_from_action: function () {           
                 
        this.do_action({               
                type: "ir.actions.act_window",               
                name: "create from creditsafe",               
                res_model: "coreff_creditsafe_createfrom_wizard",               
                views: [[false,'form']],               
                target: 'current',               
                view_type : 'form',               
                view_mode : 'form',               
                flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
        });
        return { 'type': 'ir.actions.client','tag': 'reload', } } 
 
});
 
});