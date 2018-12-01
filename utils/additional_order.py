from .api import API


class AdditionalOrderModel(object):
    basic_order_price = None
    basic_order_surcharge = None
    discount_percent = None
    final_order_price = None
    final_order_surcharge = None
    origin_basic_order_price = None
    origin_final_order_price = None
    id_type = None
    id_level = None
    quantity = None
    delivery_days = None
    basic_price = None
    final_price = None
    status = None


class AdditionalOrder(API):
    def __init__(self):
        API.__init__(self)

    def get_calculation(self, id_type, id_level, quantity, delivery_days, discount_percent, id_order):
        """
        Get result of order price calculation
        :param id_type: type of the additional order
        :param id_level: the additional order level
        :param quantity: quantity in the additional order
        :param delivery_days: delivery_days in the additional original_order
        :param discount_percent: discount_percent in the additional order
        :param id_order: id of test order
        :return: additional_order object with calculated price and all order parameters
        """
        additional_order_model = AdditionalOrderModel()
        response = self.api_additional_order_price_calculation(id_type,
                                                               id_level,
                                                               quantity,
                                                               delivery_days,
                                                               discount_percent,
                                                               id_order)
        additional_order_model.basic_order_price = response['additional_order']['basicOrderPrice']
        additional_order_model.basic_order_surcharge = response['additional_order']['basicOrderSurcharge']
        additional_order_model.discount_percent = response['additional_order']['discountPercent']
        additional_order_model.final_order_price = response['additional_order']['finalOrderPrice']
        additional_order_model.final_order_surcharge = response['additional_order']['finalOrderSurcharge']
        additional_order_model.id_level = response['additional_order']['idLevel']
        additional_order_model.id_type = response['additional_order']['idType']
        additional_order_model.origin_basic_order_price = response['additional_order']['originBasicOrderPrice']
        additional_order_model.origin_final_order_price = response['additional_order']['originFinalOrderPrice']
        additional_order_model.quantity = response['additional_order']['quantity']
        additional_order_model.delivery_days = response['additional_order']['delivery_days']
        additional_order_model.status = response['status']
        return additional_order_model

