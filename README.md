Learning Basics of Django

# Main Learning Topics

- Setting Up a Django Project
  - Installing Django
  - Create Django Project
  - Run Server
- Generate new app
- Django Models and the Admin
  - Django Fields
  - Django Migrations
- Django Management Command
- Build URL Handlers and Views
  - Implement URL patterns
  - Implement Django Views
- Build Django Templates

# Set Up a Django Project

## Prereq

- Python 3.8.2
- Python Version Manager (pyenv)
- Ways to manage python version woth `pyenv` and `venv`
  - https://gist.github.com/iamsarthakjoshi/903fb9669dd5454e35f468379c9e6e7b

## Installing Django

```
pip3 install django==3.0.3
```

## Create Django Project

```
django-admin startproject <project_name>
```

## Run Server

```
python3 manage.py runserver

# navigate to the given url to view the app in the browser
```

## Generate new app

A Django app is a component within an overall Django project. In the literal sense, it is a folder with a set of Python files. Each Django app supplies a set of related features for a specific purpose, and an overall project might have one or many apps. For instance, a Django project might contain a Django app for features related to a blog or a forum or a wiki.

```
python3 manage.py startapp <app_name>
```

## Add newly generated to "INSTALLED_APP" in main project's setting.py file

This setting defines the set of apps that our Django project will use, and we need to add our adoptions app to this list.

```
INSTALLED_APPS = [
   'django.contrib.admin',
   ...
   'adoptions'
]

```

## Pieces of an App

`apps.py`: file controls settings specific to this app.

`models.py`: file provides the data layer, which Django uses to construct our database schema and queries.

`admin.py`: file defines an administrative interface for the app that will allow us to see and edit the data related to this app.

`urls.py`: file can be used for URL routing specific to this app.

`views.py`: file defines the logic and control flow for handling requests and defines the HTTP responses that are returned.

`tests.py`: file can be used for writing unit tests for the functionality of this app.

`migrations`: folder holds files which Django uses to migrate the database as we create and change our database schema over time.


# Django Models and the Admin

## MVC Architecture

However, Django uses some different names for these. The four pieces to understand are `URL patterns`, `views`, `models`, and `templates`.

`URL patterns`: When a Django application receives a web request, it uses the URL patterns to decide which view to pass the request to for handling. In our project, the URL patterns will be defined in `wisdompets/urls.py`.

`views`: Views provide the logic or control flow portion of the project. A view is a Python callable, such as a function that takes an HTTP request as an argument and returns an HTTP response for the web server to return. Our views will be defined at `adoptions/views.py`.

`models`: To perform queries against the database, each `view` can leverage Django `models` as needed. We will define our models for the adoptions app in `adoptions/models.py`. **A Django model is a class with attributes that define the schema or underlying structure of a database table.** These classes will provide built-in methods for making queries on the associated tables.

`templates`: Each view we define can also leverage templates, which help with the **presentation layer** of what the HTML response will look like. Each template is a separate file that consists of HTML along with some extra template syntax for variables, loops, and other control flow. Our template files will be placed in a folder that we'll create called `templates`, and it will be inside of the `adoptions folder`.

## More on Models

Models create the data layer of a given Django app. This means that they define the structure of our data and how it will be stored in the database. We will also use our models to leverage Django's ORM, or object-relational mapper, when querying data from the database.

The `models.py` file contains the set of models for its Django app. A model is a class that inherits from `django.db.models.Model`, and it defines fields as **class attributes**.

Example:
As a rough analogy, we can conceptualize models as spreadsheets. Each model is a table in a spreadsheet, while each field of the model is a column for that spreadsheet table. Once our database is populated with data, we can think of each record in the database as a row in the spreadsheet. For our adoptions app our models will support a small set of requirements for an animal shelter adoption system. We'll need to store the pets available for adoption, each with a name, age, and some other information, like breed or description. We also want to track the vaccinations that a pet has been given, so we'll create a model with vaccine information and track which pets have been given which vaccines. Ultimately, the models we define will provide a way to store and retrieve this pet information from our views.

### Django Fields

Refer to this doc: https://docs.djangoproject.com/en/3.1/ref/models/fields/

`Field options`: https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-options

`Field types`: https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types

`Relationship fields`: https://docs.djangoproject.com/en/3.1/ref/models/fields/#module-django.db.models.fields.related

`Field API reference`: https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-api-reference

> Please note that the documentation version might be different by the time you read this. If that happens, visit https://docs.djangoproject.com and check out the Documentation link.

### Django Migrations

While the Django models define the expected structure of our database, `migrations` are responsible for creating the necessary scripts to change this structure through time as we update our code to change our models.

**There are several cases in which a migration is needed.**

`Adding a Model`: When a new model is created, a migration creates the corresponding database table.

`Adding a Field`, `Removing a Field`, `Changing a Field`: Migrations are also needed when a field is `added` or `removed` from an existing model, or, when attributes of a field have `changed`.

All of these changes to a model's file need a corresponding change to the database, and for these purposes migrations need to be created, and then run. The first migration created for a new Django app will create tables for the models that are defined. These migrations are called initial migrations.

#### Initial Migration

The first migration created for a new Django app will create tables for the models that are defined. These migrations are called initial migrations.

**Migration Commands**

The `commands` for working with migrations are `makemigrations`, `showmigrations` and `migrate`.

`makemigrations`: The `makemigrations` command generates migration files. It reads the current model's file and inspects the current state of the database to determine what changes need to be made to make the database structure match the model's file. Those files are placed in the migration's folder of the corresponding app, and are automatically numbered, starting with `0001`. Therefore, our initial migration will be named starting with `0001`, and it will be stored in the `adoption/migrations` folder.

```
# Run this command in project's root folder
python3 manage.py makemigrations

# output
>   adoptions/migrations/0001_initial.py
    - Create model Vaccine
    - Create model Pet
```

> The migration we just generated will create these models for the first time, so this will be an initial migration.

`showmigrations`: To see which migrations exist for our app, and which ones have not yet run, we can use this `show migrations` command.

```
python3 manage.py showmigrations
```

There are several migrations listed, and they are grouped by the corresponding `app name`, alphabetically. Several of these are default Django apps, such as `admin`, `auth`, `contenttypes`, `sessions` and so on.

In the second group, we can see our `adoptions app`. The default apps come with models and migrations. So, those migrations also appear in this list. The `square braces` on the left side of this output with an empty space indicates that these migrations have not yet been applied. To apply our migrations, we will now run `phython3 manage.py migrate` (more details below).

`migrate`: The `migrate` command runs all the generated migrations that have not yet run. We can also run migrations for a specific app to a specific number of migration, by using the migrate command with an app name and a number.
As an example, we could use `migrate adoptions 0001` to migrate to the first migration for the adoptions app.

```
python3 manage.py migrate <appname> <number>
#Eg:
python3 manage.py migrate adoptions 0001

# Output
>  Operations to perform:
      Target specific migration: 0001_initial, from adoptions
   Running migrations:
      Applying adoptions.0001_initial... OK
```

Or, to apply for every change

```
python3 manage.py migrate
```

> **When a migration has been created, but not yet run, we call this an `unapplied migration`.** This is a common source of errors during development, especially when collaborating with other developers.

> With this in mind, be sure that when working on a team, you coordinate carefully who is changing which model, and to look for new migration files when pulling in code changes.

From the output, we can see that all of the migrations were applied successfully. With this in place, let's run show migrations again to verify our results. Type `python3 manage.py showmigrations` to view the changes in migrations. Now, the `square braces` on the left have an `X` inside, indicating that each migration has been applied.

> You can use sqlitebrowser (client) to view the databases. https://sqlitebrowser.org

## Django Management Command

A Django management command is a script that is run using manage.py. This allows us to work with our Django models and anything else that Django needs to initialize for us, in a straightforward way.

Running a management command

```
python3 manage.py load_pet_data
```

## Work with the Django admin

Django admin to create an administrative interface for our project so that admin users can see and edit their data.

> Please refer to app's `admin.py` file (<root>/<app_name>/admin.py)

To make an admin interface for our `pet model`, we'll create a class and we'll call it `PetAdmin`. Now, we'll need to make this class inherit from admin.ModelAdmin. This class can take several attributes and method overrides to modify its behavior.

Next, we need to register `PetAdmin` class with the admin to tell it which model it's associated with. To do that, we'll use a `decorator` that's from the admin module called `Register`. This decorator takes our model classes and argument so we'll pass it our `pet model`.

Take a look at the Django admin to see the result of what we've done so far. **In order to do that, we need to create a `superuser` for ourselves to log in as.** So now, I'll open a terminal and navigate to the working project folder.

Creating a `superuser` to login in `Django Admin Dashboard`:

```
python3 manage.py createsuperuser

# fill the prompts
Username (leave blank to use '<you_username'):
Email address: --
Password: password
Password (again): password

# Output
> Superuser created successfully.
```

### Modifying Admin Table's Field Content

When Django displays a model instance in the admin or in a Python shell, by default, it just uses the model's name along with the word object, and the number of the ID field. To tell Django what to display for a given model, we need to override one of the default methods for that model.

Changes are can be made in following files:

> Please refer to app's `admin.py` file (<root>/<app_name>/admin.py)

**For Adoption Model**

```
...

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'age', 'sex']

...

```

**For Vaccine Model**

> Please refer to app's `admin.py` file (<root>/<app_name>/models.py)

```
class Vaccine(models.Model):
   name = models.CharField(max_length=50)

   # this will set names of vaccine instead of just showing Object
   def __str__(self):
      return self.name
```

If you now check `Admin Dashboard`, you would see the **actual names** of the `fileds` and their respective `values` instead of just `Object` keyword.

### Query data with the Django ORM

> Try these on python REPL. (Inside your project root dir)

To get started, let's import our `pet model`. Type `from adoptions .models import Pet`.

```
> from adoptions .models import Pet
```

Now we're ready to use our `Pet model` to make some queries.
Django models have an attribute called `Objects` with various methods attached.

Let's begin with the `.all()` method.

**.all() method**

```
> Pet.objects.all()
```

This returns the **query set** of all instances of this model. Let's assign this to a variable.

```
> pets = Pet.objects.all()
```

The pets variable is now assigned to a Django **query set** which has a `list-like interface`.

> Django also defines an ID field on all models, like we've seen. It's a unique integer that starts at 1 and automatically increments as records are added to the database.
> By default, instances in a query set are ordered by the ID field.

**.get() method**
Instead of a **query set**, the `.get()` method returns a `single instance`. Let's look at a different pet by using a different ID.

```
>>> pet = Pet.objects.get(id=1)
>>> pet.name
# 'Pepe'


>>> pet = Pet.objects.get(id=9999999)
# Throws an expection since id=999999 does not exist in the table
# model.DoesNotExist
```

When and instance has for than one requests,

```
>>> pet = Pet.objects.get(age=1)
# Throws an expection since .get() returned more than one (3) Pet.
# model.MultipleObjectReturned
```

> The .get method is used frequently, especially for a page on a site that shows the details of one specific object.

On the other hand, the `'multiple object return'` inception is usually avoided by design, in that the `.get` method isn't typically used for _non-unique field_ such as `age`. If you want to filter on an attribute that isn't unique, we instead would use the `.filter` method.

### Relational Data + ORM

Now, we can reuse the `pet` variable we already have to look at some Relational Data.

So, type

```
>>> pet.vaccinations.all()
<QuerySet[]> # Output
```

This shows an empty query set, because this pet has no vaccinations.

> Note, that the object return by `pet.vaccionations` has the same **ORM methods** provided by the objects attribute that we've been using. Therefore, `pet.vaccionations` will also have other ORM methods like, `.get` or `.filter`. When a `foreign key` or `many to many` filed is used on a model, its instances will have this type of object attached as the name of the field. So, for our case, this is the `vaccinations` field on the _pet object_. Using `.get`, or `.all` and so on in this vaccinations object we'll query among the vaccinations that are associated with that given pet.

Since this result was empty, lets find a `pet` that I know has some vaccinations. So, type:

```
# and for the attribute, pass in id=7.

>>> pet = Pet.objects.get(id=7)

```

Now, calling `>>> pet.vaccinations.all()`, wecan see that this `pet` has several vaccinations. Because we overrode (override) the `dunder method (__str__())`, the vaccines are showing their names in this output. Having taken this world wind tour of the Django ORM, we'll be able to write these database queries when we define our views later.

# Build URL Handlers and Views

## Understaing URL patterns (URL confs)

> defined in `<root>/<project_name>/urls.py`

URL patterns are the first part of our application code, and they will run when a request comes in. At a high level, they decide what views should handle the request.

> Refer to flow_of_control.png image below paragraph

Lets review the intended control flow of our project. Looking at the first row of the blue boxes, if a user navigates through the root of our site with nothing in the path, we want to handle this request in the home view which will use the `home.html` template. The first box in this row is empty here to represent that the path is an empty string. This homepage will show a list of pets available for adoption, and clicking one will link to `/adoptions/` a number for the `pet ID` of that pet. To handle these _requests_, looking at the second row of blue boxes here, when Django sees a request for `/adoptions/` and some number like `1`, it will route to the `pet detail view`. Which in turn, will use the pet detail `template`.

Let's take a first look at what the code to handle this will look like. In `urls.py`, we'll have a variable called `urlpatterns`. And this will be a list of calls to the path function.

When a `request` comes in, Django checks the path definition in order from top to bottom and it will look at the first argument for the pattern to match the path against.

```
urlpatterns = [
   path('', views.home, name='home'),
   path('adoption/<init:pet_id>/', views.pet_detail, name='pet_detail'),
]
```

If there's a match, the `views` function in the second argument is used. If there isn't a match, it will continue to the next path definition. If the end of this list is reached, Django will return a `404 response`.

Let's look more closely at the `path` function.

```
path('adoption/<init:pet_id>/', views.pet_detail, name='pet_detail'
```

It consists of three arguments starting with a `string` that defines the pattern it's looking for, called a `path converter`. Secondly, the `view` we intend to use for this pattern is passed in and there's also an optional third argument for the `name`. This `name` will be useful inside of templates when _we construct links_ to this `route`, and we'll see this as we implement templates later on. While the `name` is optional, **it is considered a best practice to always use it**.

### Examining the path converters more closely:

- Any part with a string such as `adoptions/` is matched literally. Therefore, the path converter in this example requires that the path being matched begins with `adoptions/`.
- Anything inside of **angled brackets** `< >` is called a `capture group`. And this can match different strings and it will treat this as a `variable`.
- Before the colon, we are using `int`, which is short for `integer` and this is our `converter type`. This is stating that we are expecting an integer number in the path. This will match `adoptions/` followed by one or some other number but it would not match if adoptions was followed by `slash` and then a `letter` or a `word`.
- After the colon, we have `pet_id`. And this defines how we want to name the resulting variable. As an example, a request to `adoptions/1` would call its `view` with a keyword argument of `pet_id` set to one.

> `Int` is a very common `converter type`, and the only one we need for our project. If you're interested in seeing more path converters, you can navigate to https://djangoproject.com and click "Documentation" in the header https://docs.djangoproject.com/en/3.1/topics/http/urls/.

Let's take a moment to review how our URL patterns will correspond with the flow of control we want in our application.

> Refer to flow_of_control_2.png image below paragraph

> Just to clarify, when running on our laptop, our project will be available at localhost:8000 rather than wisdompets.com which is a fictitious domain name we're using here just to represent how our site would behave if it was live.

A request to our site with an empty path will match our first `path converter ` which just uses an empty string. This would route to the home view, which in turn will use the home.html template.

```
path('', views.home, name='home')
```

A request with the path of `/adoptions/1` will call the _pet detail view_, passing in `pet_id` set as one as a _keyword argument_ and this `view` will use the _pet detail template_. Now that we've seen the concepts behind URL patterns, we're ready to implement them for our project.

```
path('adoption/<init:pet_id>/', views.pet_detail, name='pet_detail'
```

## Implement URL patterns

`<root>/<project_name>/urls.py`

```
from django.contrib import admin # default
from django.urls import path # default

from adoptions import views # import views from <app_dir>

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('adoptions/<int:pet_id>/', views.pet_detail, name='pet_detail'),
]

```

`<root>/<app_name>/views.py`

```
from django.shortcuts import render # default
from django.http import HttpResponse # import HttpResponse

# Create your views here.
def home(req):
   return HttpResponse('<p>Home View</p>')

def pet_detail(req, pet_id):
   return HttpResponse(f'<p>pet_detail view with id {pet_id}</p>')
```

`HttpResponse`: This class builds the response object that views are expected to return.

Now as a further test, change the URL to something bogus. Let's say `/vaccines/1` which is not a URL pattern that we've defined. Since Django settings have `debug` set to `true`, which is the default, Django gives us an error page that shows us our URL patterns in case we need to troubleshoot this. If instead, we change `debug` setting to `false` in `settings.py`, we'd see a 404 page without this debug information which is what we would expect users to see if we put this on a live site. More generally, if you see this page, you can use it to help troubleshoot your URL routing. We've now implemented our URL patterns and are ready to flesh out the rest of our project.

### Implement Django Views

`render`: The render function `render(args)` will pass the responsibility of rendering `HTML` onto the `templates` so that our view only has to be concerned with making the necessary database queries and passing that data into the template. **However, once we use the render function, our views will need template files in order to work.**

**render function's parameters:**

`request`: `render` takes as its `first argument` the object that's passed into the view. For the second argument, we pass a
`name of the template`: For the `second argument`, we pass a `string` for the `name of the template` we want to use. `E.g. home.html`
`dictionary with the data`: Next, it takes third argument as `dict data` that we want to make available inside of the template. The `keys` in this dictionary need to be `strings` and are used inside the template as variable names. To pass our `pets query set` that we have available here into the template, we'll use a dictionary with the **key** `pets`, and for the **value**, we'll use that `pets` _variable_.

To finish this `home function`, we'll return from this view with a call to `render`

`<root>/<app_name>/views.py`

```
...
def home(req):
   - return HttpResponse('<p>Home View</p>')
   + pets = Pet.objects.all()
   + return render( req, 'home.html', {'pets', pets,} )
...
```

To finish this `pet_detail function`, we'll return from this view with a call to `render`

`<root>/<app_name>/views.py`

```
...
def pet_detail(req, pet_id):
   - return HttpResponse(f'<p>pet_detail view with id {pet_id}</p>')
   + try:
   +     pet = Pet.objects.get(id=pet_id)
   + except Pet.DoesNotExit:
   +     raise Http404('Pet not found!')
   + return render(req, 'pet_detail.html', {'pet': pet,})
...
```

> At this this you would get `TemplateDoesNotExist at /adoptions/1/` error while browsing `http://127.0.0.1:8000/adoptions/1/`. That's because we haven't implemented the templates yet.

First, we'll create a `templates folder` inside the `adoptions folder`. Next, inside of this templates folder, we'll create files for each of our templates, `home.html` and `pet_detail.html`.

# Build Django Templates

Django templates are HTML files that have extra syntax. When a view calls the render function, it passes data into the template, and the template generates the HTML to show to the user.

The syntax for Django templates has `three` pieces: `variable` : `{{ variable }}`, `tag` : `{% tag %}` and `filter` : `{{ variable | filter}}`.

`{{ variable }}`: A `variable`'s value is shown when the variable name is used inside of double curly braces.

Example:

```
# In adoptions/templates/pet_details.html
<h3>{{ pet.name }}</h3>

# Resulting HTML
<h3>scooter</h3>
```

---

`{% tag %}`: A `template` tag is enclosed in curly braces with percent signs. And these are used for for loops, ifs, structural elements, as well as some other control logic.

Examples:

`for loop`: We use the for template tag to loop over each pet instance. Note that the `endfor` tag at the end of this snippet is necessary to mark the end of the loop. Inside the loop, we can use the pet variable, and here we are rending the pet's name in an `li` tag. The result is an `li` tag for each pet that's available for adoption, each showing their name.

```
# In adoptions/templates/home.html
{% for pet in pets %}
   <li>{{ pet.name | capfirst}}</li>
{% endfor %}

# Resulting HTML
<li>Scooter</li>
```

`url tempalte tag`: Some template tags don't have a corresponding _end tag_ and just render a string instead. Let's look at the `URL tag` as an example. This tag takes the name of the URL pattern as a required argument and returns the path to that pattern for use in a link. **This is where the name argument of a URL pattern becomes useful.** In below example, the URL tag with the argument home will generate the path to the `home` view, which is just a `slash`.

```
# In welovepets/urls.py
urlpatterns = [
   path('', views.home, name='home'),
]

# In adoptions/templates/home.html
{% url 'home' %}

# Resulting HTML
/
```

Now let's take a look at the URL pattern for our `pet_detail` view. Since this URL pattern has a capture group and passes the pet ID to its view, the URL tag requires this ID as an additional parameter. This URL tag renders the path to the `pet_detail` view for whatever ID is given. This example shows the result for a pet with an ID of `1`. So it generates `/adoptions/1/`.

```
# In welovepets/urls.py
urlpatterns = [
   path('adoptions/<int:pet_id>/', views.pet_detail, name='pet_detail'),
]

# In adoptions/templates/home.html
{% url 'pet_detail' pet.id %}

# Resulting HTML
/adoptions/1/
```

You might be asking why we might want to use the URL tag in this way instead of just hard coding `slash` for the home view or `/adoptions/` and putting the pet ID variable for links to the pet_detail view. **What this URL tag accomplishes is a bit of future-proofing. By using this tag instead, we can decide to change a URL pattern later, and the links we use in our templates would still be correct.**

---

`{{ variable | filter }}`: Lastly, a variable can have a pipe character after it to use a `template filter`. Template filters take a string as input and return a string as output and can be thought of much like the pipe in shell scripting. These are mostly used to take a string and change some formatting, such as `datetime` output formatting or forcing text into `title` or `uppercase`.

```

Example:

# In adoptions/templates/pet_details.html
<h3>{{ pet.name | capfirst}}</h3>

# Resulting HTML
<h3>Scooter</h3>
```

---

### Template Inheritance

For our final templating feature, let's take a quick look at `template inheritance` with the `extends` and `block` tags. To reduce repetition, Django projects implement in a `base template` with the elements that every template will use, such as metatags, any global CSS, or JavaScript and structural elements, such as a navigation bar.

In this example, we're defining some HTML boilerplate in the template file called `base`. In its body tag, we have a block template tag to provide a place for child templates to define their unique content.

For Example:

`base.html`

```
<!DOCTYPE html>
<html lang="en">
    <head>
    <!-- meta tags and so on... -->
    </head>
    <body>
        {% block content %}
        {% endblock content %}
    </body>
</html>
```

Moving to the `home` template, we use the `extends tag` with `base.html` as its parameter in order to make the home template extend from this base template.

> Note that this `extends` tag needs to be the first line of this template. After this, any block tags in this template will be used to indicate an area of content that will be overridden.

In this example, we're overriding the `block` called `content`. When rendered, the `home template` will have the HTML from the `base template`, and its body tag will be filled in with whatever's placed in the `content block`. In this example, we're putting an `h3` tag and then just an HTML comment. With this overview of template concepts in place, we're ready to implement some templates.

`home.html` template

```
{% extends "base.html" %}

{% block content %}
   <h3>Pets available for adoption</h3>
   <!--  more content.. -->
{% endblock content %}
```

## Creating Django template

Example #1:

`welovepets/adoptions/templates/home.html`

```
<div>
  {% for pet in pets %}
  <div class="petname">
      <a href="{% url 'pet_detail' pet.id %}">
         <h3>{{ pet.name | capfirst}}</h3>
      </a>
      <p>{{ pet.species }}</p>
      {% if pet.breed %}
      <p>Breed: {{ pet.breed }}</p>
      {% endif %}
      <p class="hidden">{{ pet.description }}</p>
  </div>
  {% endfor %}
</div>
```

Example #2:

`welovepets/adoptions/templates/home.html`

```
<div>
  <h3>{{ pet.name | capfirst}}</h3>

  <p>{{ pet.species }}</p>

  {% if pet.breed %}
  <p>Breed: {{ pet.breed }}</p>
  {% endif %} {% if pet.age %}
  <p>Age: {{ pet.age }}</p>
  {% endif %} {% if pet.sex %}
  <p>Sex: {{ pet.sex }}</p>
  {% endif %} {% if pet.vaccinations.all %}
  <p>Vaccinations for:</p>
  <ul>
      {% for vaccination in pet.vaccinations.all %} # 👈
      <div class="petname">
         <li>{{ vaccination.name }}</li>
      </div>
      {% endfor %}
  </ul>
  {% endif %}

  <p>Submitted by: {{ pet.submitter }}</p>
  <p>Submitted on: {{ pet.submission_date|date:"M d Y" }}</p> # 👈
  <p>{{ pet.description }}</p>
</div>

```

Note:

- 👉 As part of DJango template syntax, when using `dot` all or any other method that takes no arguments, we omit the `parentheses`.

> This submission date is a date time object that Python doesn't format very nicely by default.

- 👉 We'll need to use a `template filter` to format the date in the specific way that we want. After the submission date variable, add a pipe and then type date to use the date filter. This date filter is the first template filter we've seen that takes an argument. To pass an argument to a template filter, we use a `:` and then we pass the argument inside of double quotes. **Template filters always take a string as an argument.** For this string, use capital M, space, lowercase D, space, capital Y, which will format this date nicely into month, day, year format.

## Structure templates

Adding a base template to `<root>/adoptions/templates/base.html`

Modify the base.html template:

```
...
<div>
   <!-- Insert content here-->
   {% block content %}
   {% endblock content %}
</div>
...
```

Finally, we extend the `base.html` template in `home.html` and `pet_detail.html` templates.

In `home.html`

```
...
{% extends "base.html" %}

{% block content %}
<div>
   ...
</div>
{% endblock content %}
```

In `pet_detail.html`

```
{% extends "base.html" %}

{% block content %}
<div>
   ...
</div>
{% endblock content %}
```

# Integrate CSS and JavaScript

We'll should static assets into our templates. To make this possible, we first need to add a setting.

In your editor, navigate to the `wisdompets/settings.py` file and scroll down to the bottom. Add a setting here called `STATICFILES_DIRS`. All uppercase and set it equal to a `list`.

This setting provides a list of directories that Django will look in for serving static assets. To refer to the static folder at the top level of our project that we just pasted in, add an entry here that calls `os.path.join` with the arguments `BASE_DIR`, followed by the string `static`.

```
# In "wisdompets/settings.py"

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static')
]
```

`BASE_DIR`: is defined at the top of this file (wisdompets/settings.py) and refers to the directory where `manage.py` is, which is the base directory of our project.
`os.path.join`: is a python built-in function that provides a cross platform way to build file paths.

Now to _implement static assets in a template_, we'll use a static template tag.

> Unlike the built-in Django tags we've been using, we have to load this tag in first. Much like python files import python modules.

```
# In "adoptions/templates/base.html"

{% load static %}  <!--👈 -->
<html lang="en-US>
...
   <link
      rel="stylesheet"
      id="ample-style-css"
      - href="http://wisdompets.com/wp-content/themes/ample/style.css?ver=4.8.3"
      + href="{% static 'style.css' %}" <!--👈 -->
      type="text/css"
      media="all"
    />
...
   <div id="header-logo-image">
      <a href="/">
         <img
         - src="http://wisdompets.com/wp-content/uploads/2015/10/wisdom-pet-logo-single.png"
         + src="{% static 'logo.png' %}" <!--👈 -->
         alt="We Love Pets"
         />
      </a>
   </div>
...
   <img src="{% static 'header.jpg' %}" <!--👈 -->
      alt="We Love Pets" />
...

```
