odoo.define('coreff.creditsafe.core', function (require) {
    'use strict';

    var rpc = require('web.rpc');

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

        _getCompanies: function (countries, language, isSiret, value) {
            return rpc.query({
                model: 'creditsafe.api',
                method: 'get_companies',
                args: [countries, language, isSiret, value],
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
            }).then(function (res){
                return res[0];
            });
        }
        
    };
});
