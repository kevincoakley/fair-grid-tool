from django.db import models
from django.forms import ModelForm


class Projects(models.Model):
    name = models.CharField(max_length=200)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProjectsProducts(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class ProjectForm(ModelForm):
    """
    Project ModelForm used in add.html
    """

    class Meta:
        model = Projects
        fields = ["name"]
