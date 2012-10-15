.. _ref-tutorial:

===========================
Getting Started with Giotto
===========================

First, install giotto::

    $ pip install giotto

Now create a "Concrete Controller" file::

    $ giotto_controller --http-dev --cmd --demo

This "Concrete Controller" is an instance of a "Controller Class"
which will act as a gateway between your application and the outside world.
The file generated will be called 'giotto'.

The ``--http-dev`` and ``--cmd`` flags tells giotto to include the plumbing for those
two controller classes into the concrete controller file.
Your application can now be interacted with from the command line
or through HTTP dev server.
If you only want to interact with you app through the command line,
then you could leave off the ``--http-dev`` (and vice versa).
The option ``--demo`` tells giotto to include a simple "multiply" program to demonstrate how giotto works.

Inside the `giotto` file, you will see the following (plus some extra plumbing 
at the bottom)::

    class ColoredMultiplyView(GiottoTemplateView):
        def text_plain(self, result):
            return "{{ obj.x }} * {{ obj.y }} == {{ obj.product }}"

        def application_json(self, result):
            import json
            return json.dumps(result)

        def text_html(self, result):
            return """<!DOCTYPE html>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>
            <html>
                <body>
                    <span style="color: blue">{{ obj.x }} * {{ obj.y }}</span> == 
                    <span style="color: red">{{ obj.product }}</span>
                </body>
            </html>"""

        def text_cmd(self, result):
            from colorama import init, Fore
            init()
            return "{blue}{x} * {y}{reset} == {red}{product}{reset}".format(
                blue=Fore.BLUE,
                red=Fore.RED,
                reset=Fore.RESET,
                x=result['x'],
                y=result['y'],
                product=result['product'],
            )

        def text_irc(self, result):
            return "{blue}{x} * {y}{reset} == {red}{product}{reset}".format(
                blue="\x0302",
                red="\x0304",
                reset="\x03",
                x=result['x'],
                y=result['y'],
                product=result['product'],
            )


    def multiply(x, y):
        return {'x': int(x), 'y': int(y), 'product': int(x) * int(y)}


    class Multiply(GiottoProgram):
        name = "multiply"
        controllers = ('http-get', 'cmd', 'irc')
        model = [multiply]
        view = [ColoredMultiplyView]


The first class, the one that inherits from ``GiottoTemplateView`` is the view object,
the function ``multiply`` is the model,
and the last class (the one that subclasses `GiottoProgram`) is called the "program".
A "program" acts as an atomic unit of a giotto application that binds a group of controllers to a model and view.
Each program contains a controller, a model (optional) and a view.
You can also add middleware and cache (among other things), but we'll deal with those later.

To see our example ``multiply`` program in action, run the http-dev server by running
the following command::

    $ python giotto http-dev

This will run the development server (you must have werkzeug installed).
Now lets take a look at the ``multiply`` program.
Point your browser to: http://localhost:5000/multiply?x=4&y=8

The browser should now be displaying `4 * 8 == 32`. With the part before the `==`
in blue, and the part after in red.

The following order of events are occuring:

1. HTTP request comes into the dev server.
2. HTTP request gets passed into the giotto wsgi application.
3. Giotto inspects the request and dispatches the request off to the ``Multiply`` program.
   Giotto knows to dispatch the request to the Multiply program
   because:
    a. The program is configured to use the 'http-get' controller, and this is a HTTP GET request.
    b. The url matches the ``name`` attribute on the program class.
4. Calls the model with the arguments from the GET vars.
5. Takes the output from the model and passes it into the view object.
6. Calls the appropriate rendering method on the view class, depending on (in this case) the ``Accept`` headers.

Now, open up your browser's javascript console (firebug if you're a firefox user).
Type in the following::

    $.ajax({url: window.location.href, success: function(a) {console.log(a)}})

You should see a json representation of the page. The HTTP controller automatically
changes the return mimetype to "application/json" when the request comes from
ajax.

Lets take a look at this program as viewed from the command line. Press `ctrl+c`
to stop the dev server.

Form the shell, run the following command::

    $ python giotto multiply --x=4 --y=8

The output should be exactly the same. It should say `4 * 8 == 32` with the `32`
in red and the `4 * 8` in blue. 
The model that is being called here is exactly the same as we saw being called from the browser.
The only difference is the way the result is visualized,
and the way data moves between the user and the computer.

-----------
Using Mocks
-----------

On the GiottoProgram class, add a ``model_mock`` attribute::

    class Multiply(GiottoProgram):
        name = "multiply"
        controllers = ('http-get', 'cmd', 'irc')
        model = [multiply]
        model_mock = {'x': 10, 'y': 10, 'product': 100}
        view = [ColoredMultiplyView]

When you run the dev server include the ``--model-mock`` flag:

    % python giotto http-dev --model-mock

Now no matter what arguments you place in the url, the output will always be ``10 * 10 == 100``.
This feature is useful for front end designers who do not need to run the full model stack.

-----
Cache
-----

Add a ``cache`` attribute to the program::

    class Multiply(GiottoProgram):
        name = "multiply"
        controllers = ('http-get', 'cmd', 'irc')
        model = [multiply]
        model_mock = {'x': 10, 'y': 10, 'product': 100}
        cache = 3600
        view = [ColoredMultiplyView]

Restart the cache server (this time leave off the ``--model-mock`` flag).
Also, add a pause to the model method::

    def multiply(x, y):
        import time; time.sleep(5)
        return {'x': int(x), 'y': int(y), 'product': int(x) * int(y)}

This will simulate a heavy calculating model.
You also need to have either Redis or Memcache installed and running.
Configure the cache by uncommenting the ``cache`` variable in the concrete controller file::

    from giotto.cache import CacheWithMemcache

    cache = CacheWithMemcache(
        host='localhost'
    )

To use the redis cache, change the class to ``CacheWithRedis``.
Now when you load a page, it will take 5 seconds for the first render, and subsequent renders will be served from cache.





















