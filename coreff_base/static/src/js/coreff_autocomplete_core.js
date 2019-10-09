odoo.define('coreff.autocomplete.core', function (require) {
    'use strict';

    var rpc = require('web.rpc');
    var session = require('web.session');

    return {
        autocomplete: function (value, isSiret) {
            value = value.trim();
            var self = this;
            var def = $.Deferred();

            // fr%2Ces
            self._getCompanies("fr", "en", isSiret, value).then(res => {
                return def.resolve(res);
            });

            return def;
        },

        getCreateData: function (company) {
            var self = this;
            var def = $.Deferred();
            var company_data = company;

            const getCountryId = async (company) => {
                var countryId;
                countryId = await self._getCountryId(company.country_id);
                return countryId;
            };

            getCountryId(company).then(res => {
                company_data.country_id = res;
                def.resolve({
                    company: company_data
                });
            });

            return def;
        },

        isOnline: function () {
            return navigator && navigator.onLine;
        },

        validateSearchTerm: function (search_val, onlySiret) {
            if (onlySiret) {
                return search_val && search_val.length > 8;
            }
            else {
                return search_val && search_val.length > 3;
            }
        },

        getUser: function () {
            return rpc.query({
                model: 'res.users',
                method: 'read',
                args: [session.uid, ['name', 'company_id']],
            }).then(function (res) {
                return res[0];
            });
        },

        getConnector: function (company_id) {
            return rpc.query({
                model: 'res.company',
                method: 'read',
                args: [company_id, ['name', 'coreff_connector_id']]
            }).then(function (res) {
                return res[0];
            });
        },

        _getCompanies: function (countries, language, isSiret, value) {
            var data = {};
            data.countries = countries;
            data.language = language;
            data.is_siret = isSiret;
            data.value = value;
            data.user_id = session.uid;
            return rpc.query({
                model: 'coreff.api',
                method: 'get_companies',
                args: [data],
            }).then(function (res) {
                return res;
            });
        },

        _getCountryId: function (code) {
            var domain = [['code', '=', code]];

            return rpc.query({
                model: 'res.country',
                method: 'search_read',
                args: [domain]
            }).then(function (res) {
                return res[0];
            });
        }

    };
});
