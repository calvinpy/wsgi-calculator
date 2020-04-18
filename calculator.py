import math
import operator
import re
import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    answer = sum(map(int, args))
    return str(answer)


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    answer = int(args[0])
    for item in args[1:]:
        answer -= int(item)
    return str(answer)


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    answer = 1
    for item in args:
        answer *= int(item)
    return str(answer)


def divide(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    answer = int(args[0])
    try:
        for item in args[1:]:
            answer /= int(item)
    except ZeroDivisionError:
        raise ZeroDivisionError

    return str(answer)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {'': index, 'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide}
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args


def index():
    body = ['<h1>Calculator Instructions</h1>', '<ul>']
    body.append('<h2>Some instructions below:</h2><br>')
    body.append('Mulitply<br>')
    body.append('<li>http://localhost:8080/multiply/3/5  => 15</li>')
    body.append('<br>Add<br>')
    body.append('<li>http://localhost:8080/add/23/42  => 65</li>')
    body.append('<br>Subtract<br>')
    body.append('<li>http://localhost:8080/subtract/23/42  => -19</li>')
    body.append('<br>Divide<br>')
    body.append('<li>http://localhost:8080/divide/22/11  => 2</li>')
    body.append('</ul>')
    return '\n'.join(body)


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "200 OK"
        body = "<h1>Can Not divide by zero!</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
