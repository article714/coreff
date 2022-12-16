/** @odoo-module **/
/* global checkVATNumber */

import { AutoComplete } from "@web/core/autocomplete/autocomplete";
import { useChildRef } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { CharField } from "@web/views/fields/char/char_field";
import { useInputField } from "@web/views/fields/input_field_hook";
import { loadJS } from "@web/core/assets";

import { useCoreffAutocomplete } from "@coreff_base/coreff_autocomplete/coreff_autocomplete_core"

export class CoreffAutoCompleteCharField extends CharField {
    setup() {
        super.setup();

        this.partner_autocomplete = useCoreffAutocomplete();
        this.isHeadOfficeOnly = true;

        this.inputRef = useChildRef();
        useInputField({ getValue: () => this.props.value || "", parse: (v) => this.parse(v), ref: this.inputRef});
    }

    validateSearchTerm(request) {
        return request && request.length > 2;
    }

    get sources() {
        return [
            {
                options: async (request) => {
                    if (this.validateSearchTerm(request)) {
                        // value, valueIsCompanyCode, countryId, isHeadOffice
                        const data = this.props.record.data;
                        const country_id = data.country_id[0] || false;
                        const valueIsCompanyCode = (this.props.name == 'coreff_company_code') || false;

                        const suggestions = await this.partner_autocomplete.autocomplete(request, valueIsCompanyCode, country_id, this.isHeadOfficeOnly);
                        suggestions.forEach((suggestion) => {
                            suggestion.classList = "partner_autocomplete_dropdown_char";
                        });
                        return suggestions;
                    }
                    else {
                        return [];
                    }
                },
                optionTemplate: "coreff_base.CharFieldDropdownOption",
                placeholder: _t('Searching Coreff Data...'),
            },
        ];
    }

    async onSelect(option) {
        const data = await this.partner_autocomplete.getCreateData(Object.getPrototypeOf(option));
        console.log("Select");

        if (data.logo) {
            const logoField = this.props.record.resModel === 'res.partner' ? 'image_1920' : 'logo';
            data.company[logoField] = data.logo;
        }

        // Some fields are unnecessary in res.company
        if (this.props.record.resModel === 'res.company') {
            const fields = ['comment', 'child_ids', 'additional_info'];
            fields.forEach((field) => {
                delete data.company[field];
            });
        }

        // Format the many2one fields
        const many2oneFields = ['country_id', 'state_id'];
        many2oneFields.forEach((field) => {
            if (data.company[field]) {
                data.company[field] = [data.company[field].id, data.company[field].display_name];
            }
        });
        this.props.record.update(data.company);
    }
}

CoreffAutoCompleteCharField.template = "coreff_base.PartnerAutoCompleteCharField";
CoreffAutoCompleteCharField.components = {
    ...CharField.components,
    AutoComplete,
};

registry.category("fields").add("field_coreff_autocomplete", CoreffAutoCompleteCharField);


// odoo.define('coreff.autocomplete.fieldchar', function (require) {
//     'use strict';

//     var basic_fields = require('web.basic_fields');
//     var core = require('web.core');
//     var field_registry = require('web.field_registry');
//     var AutocompleteMixin = require('coreff.autocomplete.core');

//     var QWeb = core.qweb;

//     var FieldChar = basic_fields.FieldChar;

//     var FieldAutocomplete = FieldChar.extend(AutocompleteMixin, {
//         className: 'o_field_partner_autocomplete',
//         debounceSuggestions: 400,
//         resetOnAnyFieldChange: true,

//         events: _.extend({}, FieldChar.prototype.events, {
//             'keyup': '_onKeyup',
//             'mousedown .o_partner_autocomplete_suggestion': '_onMousedown',
//             'mousedown .o_is_head_office_checkbox': '_onMousedown',
//             'focusout': '_onFocusout',
//             'mouseenter .o_partner_autocomplete_suggestion': '_onHoverDropdown',
//             'click .o_partner_autocomplete_suggestion': '_onSuggestionClicked',
//             'click .o_is_head_office_checkbox': '_onHeadOfficeCheckboxToggle',
//         }),

//         init: function () {
//             var self = this;
//             this._super.apply(this, arguments);
//             this.headOfficeCheckboxVisibility = this.attrs.options.headOffice !== undefined ? this.attrs.options.headOffice : false

//             this.onlyCompanyCode = !(this.name === 'name');
//             this.isHeadOfficeOnly = true;
//             if (this.mode === 'edit') {
//                 this.tagName = 'div';
//                 this.className += ' dropdown open';
//             }

//             if (this.debounceSuggestions > 0) {
//                 this._suggestCompanies = _.debounce(this._suggestCompanies.bind(this), this.debounceSuggestions);
//             }

//             self.connector = false;
//             AutocompleteMixin.getUser().then(function (res) {
//                 AutocompleteMixin.getConnector(res.company_id[0]).then(function (res) {
//                     if (res.coreff_connector_id) {
//                         AutocompleteMixin.getFieldList(res.coreff_connector_id[0]).then(function (res) {
//                             if (res.autocomplete_fields) {
//                                 var field_list = res.autocomplete_fields.split(',');
//                                 self.connector = field_list.includes(self.name);
//                             }
//                         });
//                     }
//                 })
//             });
//         },

//         _removeDropdown: function () {
//             if (this.$dropdown) {
//                 this.$dropdown.remove();
//                 this.$dropdown = undefined;
//             }
//         },

//         _renderEdit: function () {
//             this.$el.empty();
//             this._prepareInput().appendTo(this.$el);
//         },

//         _selectCompany: function (company) {
//             var self = this;
//             AutocompleteMixin.getCreateData(company).then(function (data) {
//                 self.trigger_up('field_changed', {
//                     dataPointID: self.dataPointID,
//                     changes: data.company,
//                 });
//             });

//             if (this.onlyCompanyCode) {
//                 this.$input.val(this._formatValue(company.coreff_company_code));
//             }
//             else {
//                 this.$input.val(this._formatValue(company.name));
//             }
//             this._removeDropdown();
//         },

//         _showLoading: function () {
//             this._removeDropdown();
//             this.$dropdown = $(QWeb.render('coreff_autocomplete.loading'));
//             this.$dropdown.appendTo(this.$el);
//         },

//         _showDropdown: function () {
//             this._removeDropdown();
//             if (this.suggestions.length > 0 || this.headOfficeCheckboxVisibility) {
//                 this.$dropdown = $(QWeb.render('coreff_autocomplete.dropdown', {
//                     suggestions: this.suggestions,
//                     isHeadOfficeOnly: this.isHeadOfficeOnly,
//                     headOfficeCheckboxVisibility: this.headOfficeCheckboxVisibility
//                 }));
//                 this.$dropdown.appendTo(this.$el);
//             }
//         },

//         _suggestCompanies: function (value) {
//             var self = this;
//             if (AutocompleteMixin.validateSearchTerm(value, this.onlyCompanyCode) && AutocompleteMixin.isOnline() && this.connector) {
//                 self._showLoading();
//                 return AutocompleteMixin.autocomplete(value, this.onlyCompanyCode, (this.recordData.country_id) ? this.recordData.country_id.data.id : false, this.isHeadOfficeOnly).then(function (suggestions) {
//                     $('#alert_coreff').html("").hide();
//                     if (suggestions) {
//                         self.suggestions = suggestions;
//                         self._showDropdown();
//                     } else {
//                         self._removeDropdown();
//                     }
//                 }, function (error) {
//                     $('#alert_coreff').html("<b>" + error.title + "</b><br>" + error.body).show();
//                     self._removeDropdown();
//                 });
//             } else {
//                 this._removeDropdown();
//             }
//         },

//         _onFocusout: function () {
//             this._removeDropdown();
//         },

//         _onHoverDropdown: function (e) {
//             this.$dropdown.find('.active').removeClass('active');
//             $(e.currentTarget).parent().addClass('active');
//         },

//         _onInput: function () {
//             this._super.apply(this, arguments);
//             this._suggestCompanies(this.$input.val());
//         },

//         _onKeydown: function (e) {
//             switch (e.which) {
//                 case $.ui.keyCode.UP:
//                 case $.ui.keyCode.DOWN:
//                     if (!this.$dropdown) {
//                         break;
//                     }
//                     e.preventDefault();
//                     var $suggestions = this.$dropdown.children();
//                     var $active = $suggestions.filter('.active');
//                     var $to;
//                     if ($active.length) {
//                         $to = e.which === $.ui.keyCode.DOWN ?
//                             $active.next() :
//                             $active.prev();
//                     } else {
//                         $to = $suggestions.first();
//                     }
//                     if ($to.length) {
//                         $active.removeClass('active');
//                         $to.addClass('active');
//                     }
//                     return;
//             }
//             this._super.apply(this, arguments);
//         },

//         _onKeyup: function (e) {
//             switch (e.which) {
//                 case $.ui.keyCode.ESCAPE:
//                     e.preventDefault();
//                     this._removeDropdown();
//                     break;
//                 case $.ui.keyCode.ENTER:
//                     if (!this.$dropdown) {
//                         //CM: Force display of suggestions when enter is pressed
//                         this._suggestCompanies(this.$input.val());
//                         break;
//                     }
//                     e.preventDefault();
//                     var $active = this.$dropdown.find('.o_partner_autocomplete_suggestion.active');
//                     if (!$active.length) {
//                         return;
//                     }
//                     this._selectCompany(this.suggestions[$active.data('index')]);
//                     break;
//             }
//         },

//         _onMousedown: function (e) {
//             e.preventDefault();
//         },

//         _onSuggestionClicked: function (e) {
//             e.preventDefault();
//             this._selectCompany(this.suggestions[$(e.currentTarget).data('index')]);
//         },

//         _onHeadOfficeCheckboxToggle: function (e) {
//             this.isHeadOfficeOnly = e.currentTarget.children[0].checked
//         }
//     });

// field_registry.add('field_coreff_autocomplete', FieldAutocomplete);

// return FieldAutocomplete;
// });