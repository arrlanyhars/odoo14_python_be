odoo.define('custom_pos.DisableButtons', function (require) {
    "use strict";
    
    var ProductScreen = require('point_of_sale.ProductScreen');
 
    ProductScreen.include({
        start: function () {
            this._super.apply(this, arguments);
            this.$('.button.discount').hide();
            this.$('.button.price').hide();
        },
    });
 });
 

 odoo.define('custom_pos.OverrideButtonValues', function (require) {
    "use strict";

    var PosModel = require('point_of_sale.models');

    PosModel.load_fields("pos.config", ["default_button_amounts"]);

    PosModel.default_button_amounts = [10000, 50000, 100000];
});


odoo.define('custom_pos.FormHighlight', function (require) {
    "use strict";

    var FormView = require('web.FormView');

    FormView.include({
        start: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$el.find('input[type="text"]').on('focus', function () {
                $(this).css('background-color', 'yellow');
            });
        },

        on_open: function () {
            this._super.apply(this, arguments);
            this.$el.find('input[type="text"]').first().focus();
        },
    });
});
