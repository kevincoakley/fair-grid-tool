from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Projects, Products, ProjectsProducts, ProjectForm

from django.shortcuts import render
from .forms import ProductsForm


class IndexView(generic.ListView):
    template_name = "grid/index.html"
    context_object_name = "project_list"

    def get_queryset(self):
        """
        Return all projects ordered by the datetime submitted
        """
        return Projects.objects.order_by("submitted")


def add_project(request):
    """
    Display the add form on GET, add the project to the database on POST
    """
    error_message = None

    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save()

            for product_id in request.POST.getlist("product"):
                product = Products.objects.get(pk=product_id)
                p = ProjectsProducts(project=project, product=product)
                p.save()

            return HttpResponseRedirect(reverse("grid:display", args=(project.id,)))
        else:
            error_message = "The form is invalid"

    project_form = ProjectForm()
    products_form = ProductsForm()

    return render(
        request,
        "grid/add.html",
        {
            "project_form": project_form,
            "product_form": products_form,
            "error_message": error_message,
        },
    )


class DisplayView(generic.DetailView):
    model = Projects
    template_name = "grid/display.html"
    context_object_name = "project"

    def get_queryset(self):
        """
        Return the project with no filter
        """
        return Projects.objects.filter()
