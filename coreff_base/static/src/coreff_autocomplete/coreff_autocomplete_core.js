/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { KeepLast } from "@web/core/utils/concurrency";
import { useService } from "@web/core/utils/hooks";
import { renderToMarkup } from "@web/core/utils/render";
import { getDataURLFromFile } from "@web/core/utils/urls";

/**
 * Get list of companies via Autocomplete API
 *
 * @param {string} value
 * @returns {Promise}
 * @private
 */
export function useCoreffAutocomplete() {
    const keepLastOdoo = new KeepLast();
    const keepLastClearbit = new KeepLast();

    const http = useService("http");
    const notification = useService("notification");
    const orm = useService("orm");

    function autocomplete(value, valueIsCompanyCode, countryId, isHeadOffice) {
        value = value.trim();
        let odooSuggestions = [];
        return new Promise((resolve, reject) => {
            const odooPromise = getOdooSuggestions(value, valueIsCompanyCode, countryId, isHeadOffice).then((suggestions) => {
                odooSuggestions = suggestions;
            });

            const concatResults = () => {
                odooSuggestions = odooSuggestions.filter((suggestion) => {
                    return !suggestion.ignored;
                });
                odooSuggestions.forEach((suggestion) => {
                    delete suggestion.ignored;
                });
                return resolve(odooSuggestions);
            };

            whenAll([odooPromise]).then(concatResults);
        });
    }

    /**
     * Get enriched data + logo before populating partner form
     *
     * @param {Object} company
     * @returns {Promise}
     */
    function getCreateData(company) {
        const removeUselessFields = (company) => {
            // Delete attribute to avoid "Field_changed" errors
            const fields = ['label', 'description', 'domain', 'logo', 'legal_name', 'ignored', 'email', 'bank_ids', 'classList'];
            fields.forEach((field) => {
                delete company[field];
            });

            // Remove if empty and format it otherwise
            const many2oneFields = ['country_id', 'state_id'];
            many2oneFields.forEach((field) => {
                if (!company[field]) {
                    delete company[field];
                }
            });
        };

        return new Promise((resolve) => {
            // Fetch additional company info via Autocomplete Enrichment API
            // Get logo
            const logoPromise = company.logo ? getCompanyLogo(company.logo) : false;
            const company_data = company;
            // Get country record from Odoo countries by code (e.g GB, US)
            const countryPromise = getCountryId(company.country_id);

            whenAll([logoPromise, countryPromise]).then(([logo_data, country_data]) => {
                removeUselessFields(company_data);
                // Get country
                company_data.country_id = country_data;

                // Assign VAT coming from parent VIES VAT query
                if (company.vat) {
                    company_data.vat = company.vat;
                }
                resolve({
                    company: company_data,
                    logo: logo_data
                });
            });
        });
    }

    async function getCountryId(code) {
        // Get country record from Odoo countries by code (e.g GB, US)
        var domain = [['code', '=', code]];
        const prom = orm.silent.call(
            'res.country',
            'search_read',
            [domain],
        );
        const res = await keepLastOdoo.add(prom);
        return res[0]
    }

    /**
     * Use Coreff Lookup Autocomplete API to return suggestions
     *
     * @param {string} value
     * @param {boolean} valueIsCompanyCode
     * @param {int} countryId
     * @param {boolean} isHeadOffice
     * @returns {Promise}
     * @private
     */
    async function getOdooSuggestions(value, valueIsCompanyCode, countryId, isHeadOffice) {
        const isVAT = false;
        const method = isVAT ? 'read_by_vat' : 'autocomplete';
        var session = require('web.session');

        var data = {};
        data.valueIsCompanyCode = valueIsCompanyCode;
        data.country_id = countryId;
        data.is_head_office = isHeadOffice;
        data.value = value;
        data.user_id = session.uid;

        const prom = orm.silent.call(
            'coreff.api',
            "get_companies",
            [data],
        );

        const suggestions = await keepLastOdoo.add(prom);
        suggestions.map((suggestion) => {
            suggestion.label = suggestion.name;
            suggestion.description = suggestion.city + ", " + suggestion.zip
            suggestion.description += ", " + suggestion.country_id

            return suggestion;
        });

        return suggestions;
    }

    /**
     * Utility to wait for multiple promises
     * Promise.all will reject all promises whenever a promise is rejected
     * This utility will continue
     *
     * @param {Promise[]} promises
     * @returns {Promise}
     * @private
     */
    function whenAll(promises) {
        return Promise.all(promises.map((p) => {
            return Promise.resolve(p);
        }));
    }

    return { autocomplete, getCreateData };
}

// odoo.define('coreff.autocomplete.core', function (require) {
//     'use strict';

//     var rpc = require('web.rpc');
//     var session = require('web.session');

//     var AutocompleteMixin = {
//         autocomplete: function (value, valueIsCompanyCode, countryId, isHeadOffice) {
//             value = value.trim();
//             var self = this;
//             var def = $.Deferred();

//             self._getCompanies(valueIsCompanyCode, countryId, isHeadOffice, value).then(res => {
//                 if ("error" in res) {
//                     return def.reject(res.error);
//                 }
//                 else {
//                     return def.resolve(res);
//                 }
//             });

//             return def;
//         },

//         getCreateData: function (company) {
//             var self = this;
//             var def = $.Deferred();
//             var company_data = company;

//             const getCountryId = async (company) => {
//                 var countryId;
//                 countryId = await self._getCountryId(company.country_id);
//                 return countryId;
//             };

//             getCountryId(company).then(res => {
//                 company_data.country_id = res;
//                 def.resolve({
//                     company: company_data
//                 });
//             });

//             return def;
//         },

//         isOnline: function () {
//             return navigator && navigator.onLine;
//         },

//         validateSearchTerm: function (search_val, onlyCompanyCode) {
//             if (onlyCompanyCode) {
//                 return search_val && search_val.length > 8;
//             }
//             else {
//                 return search_val && search_val.length > 3;
//             }
//         },

//         getUser: function () {
//             return rpc.query({
//                 model: 'res.users',
//                 method: 'read',
//                 args: [session.uid, ['name', 'company_id']],
//             }).then(function (res) {
//                 return res[0];
//             });
//         },

//         getConnector: function (company_id) {
//             return rpc.query({
//                 model: 'res.company',
//                 method: 'read',
//                 args: [company_id, ['name', 'coreff_connector_id']]
//             }).then(function (res) {
//                 return res[0];
//             });
//         },

//         getFieldList: function (connector_id) {
//             return rpc.query({
//                 model: 'coreff.connector',
//                 method: 'read',
//                 args: [connector_id, ['name', 'autocomplete_fields']]
//             }).then(function (res) {
//                 return res[0];
//             })
//         },

//         _getCompanies: function (valueIsCompanyCode, countryId, isHeadOffice, value) {
//             var data = {};
//             data.valueIsCompanyCode = valueIsCompanyCode;
//             data.country_id = countryId;
//             data.is_head_office = isHeadOffice;
//             data.value = value;
//             data.user_id = session.uid;
//             return rpc.query({
//                 model: 'coreff.api',
//                 method: 'get_companies',
//                 args: [data],
//             }).then(function (res) {
//                 return res;
//             });
//         },

//         _getCountryId: function (code) {
//             var domain = [['code', '=', code]];

//             return rpc.query({
//                 model: 'res.country',
//                 method: 'search_read',
//                 args: [domain]
//             }).then(function (res) {
//                 return res[0];
//             });
//         }

//     };

// return AutocompleteMixin;

// });