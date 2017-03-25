# -*- coding:utf-8 -*-
from bg_biz.pay.callback import Executor
#from bg_biz.orm.emall.buying import BuyingProductsOrder,BuyingProducts
from bg_biz.orm.user import User
from bg_biz.service.user_service import UserService
#from bg_biz.service.card_service import ChargeService
from bg_biz.orm.pay.account_detail import AccountDetail
from datetime import datetime
__author__ = [
    '"liubo" <liubo@hi-wifi.cn>'
]


class BuyingExecutor(Executor):
    def execute_internal(self, obj_id):
        order = BuyingProductsOrder.get(obj_id)
        if not order:
            return False
        user = User.get(order.user_id)

        if order.status != order.Status.NEW:
            return False


        order.status = order.Status.PAY
        order.update()
        product = BuyingProducts.get(order.product_id)
        if product.product_type == BuyingProducts.ProductType.PHONE:
            charge = ChargeService.charge(order.phone,product.price, "商城", "phone", user_id=user.id,object_type="buying"
               ,object_id=order.id,do_type="buying")
        elif product.product_type == BuyingProducts.ProductType.QQ:
            charge = ChargeService.charge(order.qq,product.price, "商城", "qq", user_id=user.id,object_type="buying"
	               ,object_id=order.id,do_type="buying")
        elif product.product_type == BuyingProducts.ProductType.QQVIP:
            charge = ChargeService.charge(order.qq,product.price, "商城", "qqvip", user_id=user.id,object_type="buying"
	               ,object_id=order.id,do_type="buying")
        elif product.product_type == BuyingProducts.ProductType.SCORE:
            UserService.add_score(user, product.price, product.id, 60, datetime.now(), "商城")
            order.status = order.Status.SEND
            order.update()
        elif product.product_type == BuyingProducts.ProductType.BALANCE:
            UserService.add_balance(user, int(product.price), order.id, AccountDetail.Category.BUYING)
            order.status = order.Status.SEND
            order.update()
        else:
            pass

        return True
