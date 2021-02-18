from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from .models import Domains, ObtainDOI, Projects, Products, ProjectsProducts


def create_domain(name):
    """
    Create a domain with the given name
    """
    return Domains.objects.create(name=name)


def create_obtain_doi(name):
    """
    Create a ObtainDOI with the given name
    """
    return ObtainDOI.objects.create(name=name)


def create_project(name, primary_domain, obtain_doi, obtain_doi_other=""):
    """
    Create a project with the given name
    """
    return Projects.objects.create(
        name=name,
        primary_domain=primary_domain,
        obtain_doi=obtain_doi,
        obtain_doi_other=obtain_doi_other,
    )


def create_product(name):
    """
    Create a product with the given name
    """
    return Products.objects.create(name=name)


def join_project_product(project, product):
    """
    Create a ProjectsProducts between a project and a product
    """
    return ProjectsProducts.objects.create(project=project, product=product)


class ProjectIndexViewTests(TestCase):
    """
    Tests for IndexView (index.html)
    """

    def test_no_projects(self):
        """
        If no projects exist, an appropriate message is displayed
        """
        response = self.client.get(reverse("grid:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No projects are available.")
        self.assertQuerysetEqual(response.context["project_list"], [])

    def test_one_project(self):
        """
        If a project exists, display the project in the project_list
        """
        domain = create_domain(name="Domain 1")
        obtain_doi = create_obtain_doi(name="Other")
        create_project(
            name="Project Name", primary_domain=domain, obtain_doi=obtain_doi
        )

        response = self.client.get(reverse("grid:index"))
        self.assertQuerysetEqual(
            response.context["project_list"], ["<Projects: Project Name>"]
        )


class AddProjectViewTests(TestCase):
    """
    Tests for add_product (add.html)
    """

    def test_form_display(self):
        """
        Verify the add product ModelView displays correctly with 2 products
        """
        create_product(name="Product Name 1")
        create_product(name="Product Name 2")

        response = self.client.get(reverse("grid:add"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name")
        self.assertContains(response, "Product Name 1")
        self.assertContains(response, "Product Name 2")

    def test_form_no_data(self):
        """
        Submit the form with no data
        """
        url = reverse("grid:add")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "grid/add.html")
        self.assertContains(response, escape("The form is invalid"))

    def test_form_with_data(self):
        """
        Submit the form with currently filled out form and 2 products
        """
        create_domain(name="Domain 1")
        create_obtain_doi(name="Other")
        create_product(name="Product Name 1")
        create_product(name="Product Name 2")

        url = reverse("grid:add")
        response = self.client.post(
            url,
            {
                "name": "Project Name",
                "product": [1, 2],
                "primary_domain": "1",
                "obtain_doi": "1",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/1/")

        project = Projects.objects.get(pk=1)
        self.assertEqual(project.name, "Project Name")
        self.assertQuerysetEqual(
            project.projectsproducts_set.all(),
            [
                "<ProjectsProducts: Product Name 1>",
                "<ProjectsProducts: Product Name 2>",
            ],
            ordered=False,
        )


class ProjectDisplayViewTests(TestCase):
    """
    Tests for DisplayView (display.html)
    """

    def test_no_project(self):
        """
        If no projects exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("grid:display", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_valid_project(self):
        """
        Verify the product DetailView displays correctly with 2 products
        """
        domain = create_domain(name="Domain 1")
        obtain_doi = create_obtain_doi(name="Other")
        obtain_doi_other = "Other"
        project = create_project(
            name="Project Name",
            primary_domain=domain,
            obtain_doi=obtain_doi,
            obtain_doi_other=obtain_doi_other,
        )
        product_1 = create_product(name="Product Name 1")
        product_2 = create_product(name="Product Name 2")
        join_project_product(project=project, product=product_1)
        join_project_product(project=project, product=product_2)

        response = self.client.get(reverse("grid:display", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project Name")
        self.assertQuerysetEqual(
            response.context["project"].projectsproducts_set.all(),
            [
                "<ProjectsProducts: Product Name 1>",
                "<ProjectsProducts: Product Name 2>",
            ],
            ordered=False,
        )
