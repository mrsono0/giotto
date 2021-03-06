.. _ref-view_classes:

============
View Classes
============

View classes take in data that the model returns, and returns data that is viewable.
For instance, if the model returns a simple dictionary:

    {'x': 3, 'y': 10, 'result': 30}

The the view's job is to take this data and return a visual representation, such as::

    3 * 10 == 30

or::

    <!DOCTYPE html>
    <html>
        <body>
            <p>3 * 10 == 30</p>
        </body>
    </html>

Creating View Classes
---------------------

All view classes must descent from ``giotto.views.BaseView``.
Each class needs to implement at least one mimetype method::

    from giotto.views import BaseView

    class MyView(BaseView):
        @renders('text/plain')
        def plaintext(self, result):
            return "%(x)s * %(y)s == %(result)s" % result

Each method can be named whatever you want, and must be decorated with the ``@renders`` decorator.
The ``renders`` decorator takes multiple string arguments representing the mimetype that method renders.
When creating views, make sure there is no 'impedance mismatch' between the data that the model returns,
and the data the view is written to take in.
For instance, the above mimetype method is designed to display a dictionary with three keys (``x``, ``y``, and ``result``).
If the model was changed to return a list, this view method will crash.

Return values
-------------

Each mimetype render method should return either a string::

    return "return a string"

or a dictionary with body and mimetype tags::

    return {'body': "this is whats returned, 'mimetype': 'text/plain'}

If the method returns just a string, the controller wil treat the content as the
first mimetype passed into the ``renders`` decorator:::

    @renders('text/plain', 'text/html', 'text/x-cmd')
    def multi_render(self, result):
        return "text"

This content will be treated as ``text/plain`` by the controller.

Persisting data
---------------

Sometimes, instead of mearly displaying model-generated values to the user, 
you want to persist that value.
An example of this is saving session data to a cookie instead of displaying it in the HTML.
To do this, add the data to the ``persist`` key in the dictionary the render function returns::

    {'body': "this is whats returned, 'mimetype': 'text/plain', 'persist': {'cookie_name': 'cookie value'}}

BasicView
---------

There is a view class called ``BasicView`` that was created to be a quick and dirty way to view most any data.
While developing your application, it is a good idea to use ``BaseView`` until you have settled on a consistent data type that your model returns. Also you should inherit all custom views from ``BasicView`` for convenience.

Overriding Renderers
--------------------

In the manifest file, you can override a renderer by passing in the renderer function as a keyword argument to the view class::

    manifest = Manifest({
        'multiply': Program(
            model=[multiply],
            view=BasicView(
                html=lambda m: str(m)
            ),
        ),
    })

This program will output a string representation of the model output when viewed in an HTML context.
When viewed in a json context, the output will be the json renderer defined in ``BasicView``.

Renderer functions
------------------

Renderer functions take two arguments, the first argument is the object that the model returns,
and the second argument is the errors that may have came from a previous invocation.
The second argument is optional.
Renderer functions can be either defined as a method on the view class, or passed in to the view class constructor.