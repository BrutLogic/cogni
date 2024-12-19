# endpoint.py
from flask import Flask, request, jsonify
from functools import wraps
from typing import Callable, Dict, Any, List

from typing import List, Dict, Any, Callable, Union, TypeVar, overload

T = TypeVar('T', bound=Callable[..., Any])


class Endpoint:
    """
    A class to register and serve decorated functions as Flask endpoints.
    """
    _endpoints: List[Dict[str, Any]] = []

    @classmethod
    @overload
    def decorate(cls, http_method: str) -> Callable[[T], T]: ...

    @classmethod
    @overload
    def decorate(cls, http_method: str) -> Callable[[
        str], Callable[[T], T]]: ...

    @classmethod
    def decorate(cls, http_method: str) -> Union[Callable[[T], T], Callable[[str], Callable[[T], T]]]:
        """
        Decorator to register a function as a Flask endpoint.
        Supports both @get and @get('/path') patterns.

        Args:
            http_method (str): HTTP method for the endpoint (e.g., 'GET', 'POST').

        Returns:
            Callable: The decorator.
        """
        def decorator(func_or_path: Union[T, str]) -> Union[T, Callable[[T], T]]:
            # If decorator is used with path argument (@get('/path'))
            if isinstance(func_or_path, str):
                def inner_decorator(func: T) -> T:
                    endpoint_info = {
                        'func': func,
                        'method': http_method.upper(),
                        'endpoint': func_or_path if func_or_path.startswith('/') else f'/{func_or_path}',
                        'registered':False,
                    }
                    cls._endpoints.append(endpoint_info)
                    return func
                return inner_decorator

            # If decorator is used without path argument (@get)
            func = func_or_path
            endpoint_info = {
                'func': func,
                'method': http_method.upper(),
                'endpoint': f"/{func.__name__}".replace('_', '/'),
                'registered': False,
                
            }

            if endpoint_info['endpoint'] == '/root':
                endpoint_info['endpoint'] = '/'
            cls._endpoints.append(endpoint_info)
            return func

        return decorator

    @classmethod
    def register_endpoints(cls, app: Flask) -> None:
        """
        Register all collected endpoints with a Flask application.

        Args:
            app: Flask application instance
        """
        for endpoint in cls._endpoints:
            if endpoint['registered']: continue
            app.add_url_rule(
                endpoint['endpoint'],  # URL rule
                view_func=endpoint['func'],  # View function
                methods=[endpoint['method']]  # HTTP methods
            )
            
            endpoint['registered'] = True

get = Endpoint.decorate('GET')
post = Endpoint.decorate('POST')
endpoint = get