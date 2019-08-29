odoo.define('coreff.creditsafe.core', function (require) {
    'use strict';

    var rpc = require('web.rpc');

    return {
        autocomplete: function (value, isSiret) {
            value = value.trim();
            var self = this;
            var def = $.Deferred(),
                creditsafeSuggestions = [];

            const getCreditSafeSuggestions = async (value, isSiret) => {
                const settings = await self._getCreditSafeSettings();
                var headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': settings.token
                };
                if (isSiret) {
                    var url = settings.url + '/companies?countries=fr%2Ces&language=en&regNo=' + value;
                }
                else {
                    var url = settings.url + '/companies?countries=fr%2Ces&language=en&name=' + value;
                }
                var options = {
                    headers: headers,
                    method: "GET"
                };
                const response = await fetch(url, options);
                const json = await response.json();
                console.log(json);
                return json;
            };

            getCreditSafeSuggestions(value, isSiret).then(res => {
                creditsafeSuggestions = res.companies.map(function (company){
                    var suggestion = {};
                    suggestion.name = company.name;
                    suggestion.siret = company.regNo;
                    suggestion.street = company.address.street;
                    suggestion.city = company.address.city;
                    suggestion.zip = company.address.postCode;
                    suggestion.country_id = company.country;
                    return suggestion;
                });
                return def.resolve(creditsafeSuggestions);
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

        _getCreditSafeSettings: function () {
            var self = this;
            var def = $.Deferred();

            const getSettings = async () => {
                var settings = {};
                settings.url = await self._getSettings("coreff_creditsafe.creditsafe_url");
                settings.username = await self._getSettings("coreff_creditsafe.creditsafe_username");
                settings.password = await self._getSettings("coreff_creditsafe.creditsafe_password");
                settings.token = await self._getSettings("coreff_creditsafe.creditsafe_token");
                return settings;
            };

            getSettings().then(res => {
                def.resolve(res);
            });

            return def;
        },

        _getSettings: function (key) {
            var domain = [['key', '=', key]];
            var fields = ['value'];

            return rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [domain, fields],
            }).then(function (res) {
                return res[0].value;
            });
        },

        _getCountryId: function (code) {
            var domain = [['code', '=', code]];

            return rpc.query({
                model: 'res.country',
                method: 'search_read',
                args: [domain]
            }).then(function (res){
                return res[0];
            });
        },

        _getSettingsId: function (key) {
            var domain = [['key', '=', key]];

            return rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [domain]
            }).then(function (res){
                return res[0];
            });
        },

        _updateSettings: function (id, value) {
            return rpc.query({
                model: 'ir.config_parameter',
                method: 'write',
                args: [id, {value: value}],
            }).then(function () {
                return;
            });
        },

        _updateToken: function (settings) {
            var self = this;
            const getToken = async () => {
                var headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                };
                var url = settings.url + '/authenticate';
                var data = {
                    username: settings.username,
                    password: settings.password
                };
                var options = {
                    headers: headers,
                    data: data,
                    method: "POST"
                };
                const response = await fetch(url, options);
                const json = await response.json();
                console.log(json);
                return json;
            };

            const updateToken = async () => {
                const token = await getToken();
                const settingId = await self._getSettingsId("coreff_creditsafe.creditsafe_token");
                await self._updateSettings(settingId, token);
            }

            return updateToken().then(function () {
                return;
            });
        },
        
    };
});
