from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):
    
        """
        Test the retrieval of products from the shop.
        
        This method creates a test environment with sample products and categories,
        then verifies the correct functioning of the product listing view.
        
        Args:
            self: The test case instance.
        
        Returns:
            None: This method doesn't return anything but performs assertions.
        """
        small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
        )

    
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')

        """
        Test the retrieval of a product by its slug.
        
        This method creates a product with a small GIF image, assigns it to a category,
        and then makes a GET request to the product detail view using the product's slug.
        It verifies that the response is successful and that the correct product is
        returned in the response context.
        
        Args:
            self: The test case instance.
        
        Returns:
            None: This method doesn't return anything but performs assertions.
        """
        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)


class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        # Create a product
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='Category 1')
        product = Product.objects.create(
            title='Product 1', category=category, slug='product-1', image=uploaded)
        # Make a request to the product detail view with the product's slug
        response = self.client.get(
            reverse('shop:product-detail', kwargs={'slug': 'product-1'}))

        # Check that the response is a success
        self.assertEqual(response.status_code, 200)

        # Check that the product is in the response context
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        """Sets up the test environment with sample data.
        
        Args:
            self: The test case instance.
        
        Returns:
            None: This method doesn't return anything, but it sets up instance attributes.
        """
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_status_code(self):
        """Tests the HTTP status code for the category list view.
        
        Args:
            self: TestCase: The test case instance.
        
        Returns:
            None: This method doesn't return anything, but asserts that the response status code is 200.
        """
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        """Test the context data of the category list view.
        
        Args:
            self: TestCase: The test case instance.
        
        Returns:
            None: This method doesn't return anything, it performs assertions.
        """
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        """
        Test if the correct template is used for the category list view.
        
        Args:
            self: TestCase instance
        
        Returns:
            None: This method doesn't return anything, it performs assertions
        """        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)