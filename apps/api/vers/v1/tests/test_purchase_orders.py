from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from apps.home.models.supplier import Supplier


class PurchaseOrderAPITestCase(APITestCase):
    """Purchase order Testing module"""
    def setUp(self):
        
        super().setUp()

        # Creates a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        # Creates a supplier
        self.supplier_data = {'name': 'Old Supplier', 'email': 'oldsupplier@gmail.com'}
        self.supplier = Supplier.objects.create(**self.supplier_data)

        # Creates for purchase order and line items

        # Test Order 1
        self.order1 = {
            'supplier': {'id': None, 'name': 'The ABC Company', 'email': 'abc@company.com'},
            'line_items': [
                {'item_name': 'Item123', 'quantity': 2, "tax_name": "VAT", 'price_without_tax': 10.0, 'tax_amount': 2.0},
                {'item_name': 'Item456', 'quantity': 3, "tax_name": "VAT", 'price_without_tax': 15.0, 'tax_amount': 3.0}
            ]
        }

        # Test Order 2
        self.order2_id, self.order2_item_id = None, None
        self.order2 = {
            'supplier': {'id': self.supplier.id, 'name': 'New Supplier', 'email': 'newsupplier@gmail.com'},
            'line_items': [
                {'item_name': 'SKU899', 'quantity': 28, "tax_name": "GST", 'price_without_tax': 146.0, 'tax_amount': 14.6}
            ]
        }

        # Test Order 3
        self.order3 = {
            'supplier': {'id': None, 'name': 'Stark Ind', 'email': 'starkind@marvel.com'},
            'line_items': [
                {'item_name': 'UPC54893', 'quantity': 3, "tax_name": "VAT", 'price_without_tax': 15.0, 'tax_amount': 3.0}
            ]
        }

        # Test Order 4
        self.order4 = {
            'supplier': {'id': None, 'name': 'Hammer Ind', 'email': 'hammerind@marvel.com'},
            'line_items': [
                {'item_name': 'EAN35435', 'quantity': 28, "tax_name": "GST", 'price_without_tax': 146.0, 'tax_amount': 14.6}
            ]
        }


    def test_a_create_orders(self):
        """create_purchase_order : Checks Order creation, Supplier updation, Calculation at order header and line level"""

        # self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/purchase/order/', data=self.order1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create order
        response = self.client.post('/api/v1/purchase/order/', data=self.order2, format='json')

        supplier_name = response.data['supplier']['name']
        supplier_email = response.data['supplier']['email']

        # Old order had a diffrent supplier
        self.assertEqual(supplier_name, "New Supplier")
        self.assertEqual(supplier_email, "newsupplier@gmail.com")

        total_amount = response.data['total_amount'] 
        total_quantity = response.data['total_quantity']
        total_tax = response.data['total_tax']
        item_total = response.data['line_items'][0]['line_total']

        # Check calculations
        self.assertEqual(total_amount, "4496.80")
        self.assertEqual(total_quantity, 28)
        self.assertEqual(total_tax, "408.80")
        self.assertEqual(item_total, "4496.80")

        self.order2_id = response.data['id']
        self.order2_item_id = response.data['line_items'][0]['id']


    def test_b_list_orders(self):
        """list_purchase_order : Checks no. of orders received on using and not using filters"""

        # self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/purchase/order/', data=self.order3, format='json')
        response = self.client.post('/api/v1/purchase/order/', data=self.order4, format='json')

        # Get all orders
        response = self.client.get('/api/v1/purchase/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Get all orders where item_name=EAN
        response = self.client.get('/api/v1/purchase/order/?item_name=UPC')
        self.assertEqual(len(response.data), 1)

        # Get all orders where supplier_name=Stark
        response = self.client.get('/api/v1/purchase/order/?supplier_name=Stark')
        self.assertEqual(len(response.data), 1)

        # Get all orders where supplier_name=Stark and item_name=EAN
        response = self.client.get('/api/v1/purchase/order/?supplier_name=Stark&item_name=EAN')
        self.assertEqual(len(response.data), 0)

        # Get all orders where supplier_name=Stark and item_name=UPC
        response = self.client.get('/api/v1/purchase/order/?supplier_name=Stark&item_name=UPC')
        self.assertEqual(len(response.data), 1)


    def test_c_update_order(self):
        """update_purchase_order : Checks success of the request, line item count"""

        # Create order
        response = self.client.post('/api/v1/purchase/order/', data=self.order2, format='json')
        self.order2_id = response.data['id']
        self.order2_item_id = response.data['line_items'][0]['id']

        update_data = {
            'supplier': {'id': None, 'name': 'Updated Supplier', 'email': 'updated@example.com'},
            'line_items': [
                {'id': self.order2_item_id, 'item_name': 'Updated Item', 'quantity': 5, 'price_without_tax': 20.0, 'tax_amount': 4.0},
            ]
        }

        # Update order 
        response = self.client.put(f'/api/v1/purchase/order/{self.order2_id}/', data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['line_items']), 1)



    def test_d_delete_order(self):
        """delete_purchase_order : Checks if the order is deleted"""

        response = self.client.post('/api/v1/purchase/order/', data=self.order2, format='json')
        self.order2_id = response.data['id']

        response = self.client.delete(f'/api/v1/purchase/order/{self.order2_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
