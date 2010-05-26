from should_dsl import matcher
import re

@matcher
def equal_to():
    return (lambda x, y: x == y, "%r is %sequal to %r")

@matcher
def into():
    return (lambda item, container: item in container, "%r is %sinto %r")

@matcher
def greater_than():
    return (lambda x, y: x > y, "%r is %sgreater than %r")

@matcher
def greater_than_or_equal_to():
    return (lambda x, y: x >= y, "%r is %sgreater than or equal to %r")

@matcher
def less_than():
    return (lambda x, y: x < y, "%r is %sless than %r")

@matcher
def less_than_or_equal_to():
    return (lambda x, y: x <= y, "%r is %sless than or equal to %r")

def check_exception(expected_exception, callable_and_possible_params):
    if getattr(callable_and_possible_params, '__getitem__', False):
        callable = callable_and_possible_params[0]
        params = callable_and_possible_params[1:]
    else:
        callable = callable_and_possible_params
        params = []
    try:
        callable(*params)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

@matcher
def thrown_by():
    return (check_exception, "%r is %sthrown by %r")

@matcher
def throw():
    def local_check_exception(callable_and_possible_params, expected_exception):
        return check_exception(expected_exception=expected_exception,
                               callable_and_possible_params=callable_and_possible_params)
    return (local_check_exception, "%r %sthrows %r")

@matcher
def in_any_order():
    def contains_in_any_order(container, elements):
        for element in elements:
            if element not in container:
                return False
        return True
    return (contains_in_any_order, "%r does %shave in any order %r")

@matcher
def all_of():
    return (in_any_order()[0], "%r does %shave all of %r")

@matcher
def any_of():
    def have_any_of(container, elements):
        for element in elements:
            if element in container:
                return True
        return False
    return (have_any_of, "%r does %shave any of %r")

@matcher
def kind_of():
    return (lambda obj, kind: isinstance(obj, kind), "%r is %s a kind of %r")

@matcher
def instance_of():
    return (lambda obj, kind: isinstance(obj, kind), "%r is %s an instance of %r")

@matcher
def ended_with():
    return (lambda x, y: x.endswith(y), "%r is %sended with %r")

@matcher
def started_with():
    return (lambda x, y: x.startswith(y), "%r is %sstarted with %r")

@matcher
def like():
    return (lambda string, regex: re.match(regex, string) is not None, "%r is %slike %r")

@matcher
def equal_to_ignoring_case():
    return (lambda x, y: unicode(x, 'utf-8').lower() == unicode(y, 'utf-8').lower(), "%r is %sequal to %r ignoring case")

