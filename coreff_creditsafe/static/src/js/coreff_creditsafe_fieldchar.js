odoo.define('coreff.creditsafe.fieldchar', function (require) {
    'use strict';

    var basic_fields = require('web.basic_fields');
    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var Autocomplete = require('coreff.creditsafe.core');

    var QWeb = core.qweb;

    var FieldChar = basic_fields.FieldChar;

    var FieldAutocomplete = FieldChar.extend({
        className: 'o_field_partner_autocomplete',
        debounceSuggestions: 400,
        resetOnAnyFieldChange: true,

        events: _.extend({}, FieldChar.prototype.events, {
            'keyup': '_onKeyup',
            'mousedown .o_partner_autocomplete_suggestion': '_onMousedown',
            'focusout': '_onFocusout',
            'mouseenter .o_partner_autocomplete_suggestion': '_onHoverDropdown',
            'click .o_partner_autocomplete_suggestion': '_onSuggestionClicked',
        }),

        init: function () {
            this._super.apply(this, arguments);

            this.onlySiret = this.name === 'siret';

            if (this.mode === 'edit') {
                this.tagName = 'div';
                this.className += ' dropdown open';
            }

            if (this.debounceSuggestions > 0) {
                this._suggestCompanies = _.debounce(this._suggestCompanies.bind(this), this.debounceSuggestions);
            }
        },

        _isActive: function () {
            return this.model === 'res.company' ||
                (
                    this.model === 'res.partner'
                    && this.record.data.is_company
                    && !(this.record.data && this.record.data.id)
                );
        },

        _removeDropdown: function () {
            if (this.$dropdown) {
                this.$dropdown.remove();
                this.$dropdown = undefined;
            }
        },

        _renderEdit: function () {
            this.$el.empty();
            this._prepareInput().appendTo(this.$el);
        },

        _selectCompany: function (company) {
            var self = this;
            Autocomplete.getCreateData(company).then(function (data) {
                console.log(data);

                self.trigger_up('field_changed', {
                    dataPointID: self.dataPointID,
                    changes: data.company,
                });
            });

            if (this.onlySiret) {
                this.$input.val(this._formatValue(company.siret));
            }
            else {
                this.$input.val(this._formatValue(company.name));
            }
            this._removeDropdown();
        },

        _showDropdown: function () {
            this._removeDropdown();
            if (this.suggestions.length > 0) {
                this.$dropdown = $(QWeb.render('creditsafe_autocomplete.dropdown', {
                    suggestions: this.suggestions,
                }));
                this.$dropdown.appendTo(this.$el);
            }
        },

        _suggestCompanies: function (value) {
            var self = this;
            if (Autocomplete.validateSearchTerm(value, this.onlySiret) && Autocomplete.isOnline()) {
                return Autocomplete.autocomplete(value, this.onlySiret).then(function (suggestions) {
                    if (suggestions && suggestions.length) {
                        self.suggestions = suggestions;
                        self._showDropdown();
                    } else {
                        self._removeDropdown();
                    }
                });
            } else {
                this._removeDropdown();
            }
        },

        _onFocusout: function () {
            this._removeDropdown();
        },

        _onHoverDropdown: function (e) {
            this.$dropdown.find('.active').removeClass('active');
            $(e.currentTarget).parent().addClass('active');
        },

        _onInput: function () {
            this._super.apply(this, arguments);
            if (this._isActive()) {
                this._suggestCompanies(this.$input.val());
            }
        },

        _onKeydown: function (e) {
            switch (e.which) {
                case $.ui.keyCode.UP:
                case $.ui.keyCode.DOWN:
                    if (!this.$dropdown) {
                        break;
                    }
                    e.preventDefault();
                    var $suggestions = this.$dropdown.children();
                    var $active = $suggestions.filter('.active');
                    var $to;
                    if ($active.length) {
                        $to = e.which === $.ui.keyCode.DOWN ?
                            $active.next() :
                            $active.prev();
                    } else {
                        $to = $suggestions.first();
                    }
                    if ($to.length) {
                        $active.removeClass('active');
                        $to.addClass('active');
                    }
                    return;
            }
            this._super.apply(this, arguments);
        },

        _onKeyup: function (e) {
            switch (e.which) {
                case $.ui.keyCode.ESCAPE:
                    e.preventDefault();
                    this._removeDropdown();
                    break;
                case $.ui.keyCode.ENTER:
                    if (!this.$dropdown) {
                        break;
                    }
                    e.preventDefault();
                    var $active = this.$dropdown.find('.o_partner_autocomplete_suggestion.active');
                    if (!$active.length) {
                        return;
                    }
                    this._selectCompany(this.suggestions[$active.data('index')]);
                    break;
            }
        },

        _onMousedown: function (e) {
            e.preventDefault();
        },

        _onSuggestionClicked: function (e) {
            e.preventDefault();
            this._selectCompany(this.suggestions[$(e.currentTarget).data('index')]);
        },
    });

    field_registry.add('field_coreff_creditsafe', FieldAutocomplete);

    return FieldAutocomplete;
});
