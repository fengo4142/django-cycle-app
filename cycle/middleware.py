import sys

class ExceptionMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        from main.models import error_logging

        exc_type, exc_value, tb = sys.exc_info()

        import traceback
        stack = traceback.extract_tb(tb)

        print("hook start part")

        for path, lineno, func, line in stack:
            if 'lib/python' in path or 'settings.py' in path:
                continue

            X = error_logging()
            X.file_name = path
            X.line_number = lineno
            X.class_name = func
            X.message = line
            X.save()

            print('File "%s", line %d, in %s' % (path, lineno, func))
            print('  %s' % line)

        print("logging end")