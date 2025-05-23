# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging
logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, values):
        if self.env.context.get("skip_update_price_unit") and values.get("price_unit"):
            values.pop("price_unit")
        return super().write(values)

    def _get_price_unit(self):
        logger.warning("-----get_price_purchase_discount--------")
        """Get correct price with discount replacing current price_unit
        value before calling super and restoring it later for assuring
        maximum inheritability.

        HACK: This is needed while https://github.com/odoo/odoo/pull/29983
        is not merged.
        """
        if hasattr(self.env, "ocb"):
            logger.warning("-----hasattr-------")
            return super()._get_price_unit()
        price_unit = False
        po_line = self.purchase_line_id
        if po_line and self.product_id == po_line.product_id:
            logger.warning("----if po_line------")
            price = po_line._get_discounted_price_unit()
            if price != po_line.price_unit:
                logger.warning("---if price------")
                # Only change value if it's different
                price_unit = po_line.price_unit
                logger.warning(price_unit)
                logger.warning(price)
                po_line.price_unit = price
        res = super()._get_price_unit()

        if price_unit:
            logger.warning("-----pric_unit----")
            po_line.price_unit = price_unit
            logger.warning(po_line.price_unit)       
        logger.warning("----res_get------")
        logger.warning(res)
        return res
