from src.utils.id import Id
from src.ecommerce.sale import Sale
from src.ecommerce.sales_summary import SalesSummary

class SalesRegistry():
    def __init__(self) -> None:
        self.sales_by_client = {}
        self.sales_by_id = {}

    def register_sale (self, client_id, total_price, books):
        purchase_id = Id.generate()
        self._register_sale_for_client(client_id, purchase_id)
        self._register_sale_by_id(purchase_id, total_price, books)
        return purchase_id
    
    def sales_summary_for_client(self, client_id):
        client_sales = self._sales_for_client(client_id)
        return SalesSummary.generate_from_sales(client_sales)
    
    
    def _sales_for_client(self, client_id):
        clients_sales_ids = self.sales_by_client.get(client_id, [])
        return [self.sales_by_id[sale_id] for sale_id in clients_sales_ids]

    def _register_sale_for_client(self, client_id, purchase_id):
        client_current_sales = self.sales_by_client.get(client_id, [])
        client_current_sales.append(purchase_id)
        self.sales_by_client[client_id] = client_current_sales
    
    def _register_sale_by_id (self, purchase_id, total_price, sold_books):
        new_purchase = Sale.with_total_price_and_books(total_price, sold_books)
        self.sales_by_id[purchase_id] = new_purchase
