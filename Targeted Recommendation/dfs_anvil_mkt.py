from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server
import random
import json


class main(mainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.cart = {}
        self.products = []
        self.product_q = []
        self.page_num = 0
        self.total_order = 0
        self.USER_ID = random.choice([234, 17850])
        print(self.USER_ID)
        self.product_q += self.bring_next_products()
        self.load_products()

    
    def get_next_page(self):
        self.page_num += 1
        
        # Case when we need to fetch the next two products
        if len(self.products) == 2*self.page_num:
            if len(self.product_q) == 0:
                self.product_q += self.bring_next_products()
                if len(self.product_q) == 0:
                    self.page_num -= 1
                    return False

            # load new products
            self.load_products()
        return True

    def bring_next_products(self):
        prod_result = anvil.server.call('get_recomendations', self.USER_ID, json.dumps(self.cart) )
        print(prod_result)
        return prod_result
        
    
    def get_prev_page(self):
        self.page_num -= 1
        
        # load new products
        self.load_products()
        return
    

    def load_products(self, ):
        self.products += self.product_q[:2]
        self.product_q = self.product_q[2:]
        #self.products 
        self.load_product_1()
        self.load_product_2()

    
    def load_product_1(self):
        # Load information to product one
        prod_info = self.products[2*self.page_num]
        self.img_prod1.source = prod_info['image_url']
        self.name_prod1.content = "**" + prod_info['product_name'] + "**"
        self.price_prod1.content = "$" + str(prod_info['price'])

        if str(prod_info['product_id']) in self.cart:
            self.remove_prod1.visible = True
        else:
            self.remove_prod1.visible = False
        return

    
    def load_product_2(self):
        # Load information to product two
        prod_info = self.products[2*self.page_num+1]
        self.img_prod2.source = prod_info['image_url']
        self.name_prod2.content = "**" + prod_info['product_name'] + "**"
        self.price_prod2.content = "$" + str(prod_info['price'])

        if str(prod_info['product_id']) in self.cart:
            self.remove_prod2.visible = True
        else:
            self.remove_prod2.visible = False
        return

    
    def next_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if not self.get_next_page():
            return
        
        if not self.prev_btn.visible:
            self.prev_btn.visible = True
        return

    
    def prev_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.get_prev_page()
        if self.page_num == 0:
            self.prev_btn.visible = False
        return

    
    def buy_btn_prod1_click(self, **event_args):
        """This method is called when the button is clicked"""
        prod_info = self.products[2*self.page_num]
        self.total_order += float(prod_info['price'])
        self.update_total_amount()
        self.add_product_to_cart(prod_info["product_id"], prod_info["product_name"])
        self.remove_prod1.visible = True
        return

    
    def buy_btn_prod2_click(self, **event_args):
        """This method is called when the button is clicked"""
        prod_info = self.products[2*self.page_num+1]
        self.total_order += float(prod_info['price'])
        self.update_total_amount()
        self.add_product_to_cart(prod_info["product_id"], prod_info["product_name"])
        self.remove_prod2.visible = True
        return

    
    def update_total_amount(self):
        self.label_total_amount.text = f"${abs(self.total_order):.2f}"


    def add_product_to_cart(self, prod_id, prod_name):
        prod_id = str(prod_id)
        if prod_id in self.cart:
            self.cart[prod_id]["qty"] += 1
        else:
            self.cart[prod_id] = {"qty":1, "name":prod_name}

        self.update_cart_info()

    
    def remove_product_from_cart(self, prod_id):
        prod_id = str(prod_id)
        if self.cart[prod_id]["qty"] > 0:
            self.cart[prod_id]["qty"] -= 1

        if self.cart[prod_id]["qty"] == 0:
            self.cart.pop(prod_id)
        self.update_cart_info()

    
    def remove_prod1_click(self, **event_args):
        """This method is called when the button is clicked"""
        prod_info = self.products[2*self.page_num]
        self.remove_product_from_cart(prod_info["product_id"])
        self.total_order -= prod_info["price"]
        self.update_total_amount()

        if not str(prod_info["product_id"]) in self.cart:
            self.remove_prod1.visible = False
        return

    
    def remove_prod2_click(self, **event_args):
        """This method is called when the button is clicked"""
        prod_info = self.products[2*self.page_num+1]
        self.remove_product_from_cart(prod_info["product_id"])
        self.total_order -= prod_info["price"]
        self.update_total_amount()

        if not str(prod_info["product_id"]) in self.cart:
            self.remove_prod2.visible = False
        return

    
    def buy_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.total_order <= 0:
            return
        
        alert(f'Your order has been placed, please head inside the convinience store to pick up your products!')
        # reload site
        open_form('main')

    def update_cart_info(self):
        """This method is called when the button is clicked"""
        final_str = "Your cart:\n\n---\n\n"
        for p in self.cart:
            contents = self.cart[p]
            final_str += f'{contents["name"]}: \t\t{contents["qty"]}\n'
        self.cart_breakdown.content = final_str

        
