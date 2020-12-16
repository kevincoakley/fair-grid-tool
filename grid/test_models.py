from django.test import TestCase

from .models import Projects, Products, ProjectsProducts


class ProjectsModelTests(TestCase):
    def test_str(self):
        """
        __str__ returns name
        """
        test_project = Projects(name="Test")
        self.assertEqual(str(test_project), "Test")


class ProductsModelTests(TestCase):
    def test_str(self):
        """
        __str__ returns name
        """
        test_product = Products(name="Test")
        self.assertEqual(str(test_product), "Test")


class ProjectsProductsModelTests(TestCase):
    def test_str(self):
        """
        __str__ returns name
        """
        test_project = Projects(name="Test Project")
        test_product = Products(name="Test Product")
        test_project_product = ProjectsProducts(
            project=test_project, product=test_product
        )
        self.assertEqual(str(test_project_product), "Test Product")
