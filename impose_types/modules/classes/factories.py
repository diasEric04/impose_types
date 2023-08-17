# flake8: noqa
from abc import ABC, abstractmethod
from typing import Callable, Any
import numpy as np
from modules.exeptions.decorator import (ArgsLengthDontMatch, TypesDontMatch, 
                                         KwargsKeysDontMatch)
from modules.classes.types import Optional


class Decorator(ABC):
    @classmethod
    @abstractmethod
    def decorate(cls, *args, **kwargs) -> Callable: pass
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any: pass


class ImposeTypesDecorator(Decorator):
    # args e kwargs do metodo da classe decorator
    def __init__(self, func, *typed_args, **typed_kwargs):
        self.func = func
        self.typed_args = typed_args
        self.typed_kwargs = typed_kwargs
    
    @classmethod
    def decorate(cls, *args, **kwargs) -> Callable:
        def decorator(func):
            return cls(func, *args, **kwargs)
        return decorator
    
    # args e kwargs da funcao decorada
    def __call__(self, *args, **kwargs) -> Any:
        func_returned_value = self.func(*args, **kwargs)

        self.verify_args_shape(args, kwargs)
        self.verify_args_types(args, kwargs)
        self.verify_kwargs_keys(kwargs)
        
        return func_returned_value

    def verify_args_shape(self, args: tuple, kwargs: dict):
        
        args_len = len(args)
        kwargs_len = len(kwargs)
        
        typed_args_len = len(self.typed_args)
        typed_kwargs_len = len(self.typed_kwargs)
        
        ndarray_typed_args = np.array(self.typed_args)
        ndarray_typed_kwargs = np.array(list(self.typed_kwargs.values()))
        
        args_len += np.where(ndarray_typed_args == Optional, 1, 0).sum()
        kwargs_len += np.where(ndarray_typed_kwargs == Optional, 1, 0).sum()

        if args_len != typed_args_len:
            raise ArgsLengthDontMatch(
                'positional args', args_len, typed_args_len
            )

        if kwargs_len != typed_kwargs_len:
            raise ArgsLengthDontMatch(
                'keyword args', kwargs_len, typed_kwargs_len
            )

    def verify_args_types(self, args: tuple, kwargs: dict):
        typed_args_ndarray = np.array(self.typed_args)
        typed_kwargs_ndarray = np.array(list(self.typed_kwargs.values()))
        
        args_ndarray = np.array([type(arg) for arg in args])
        kwargs_ndarray = np.array([type(kwarg) for kwarg in kwargs.values()])
        
        if Optional not in typed_args_ndarray:
            cond_args = np.array(args_ndarray not in typed_args_ndarray)
            if cond_args.any() or Optional in typed_args_ndarray:
                raise TypesDontMatch(
                    'positional args', typed_args_ndarray, args_ndarray
                )
                
        if Optional not in typed_kwargs_ndarray:
            cond_kwargs = np.array(kwargs_ndarray not in typed_kwargs_ndarray)
            if cond_kwargs.any():
                raise TypesDontMatch(
                    'keyword args', typed_kwargs_ndarray, kwargs_ndarray
                )
    
    def verify_kwargs_keys(self, kwargs: dict):
        if Optional not in np.array(list(self.typed_kwargs.values())):
            if kwargs.keys() != self.typed_kwargs.keys():
                raise KwargsKeysDontMatch(
                    kwargs.keys(), self.typed_kwargs.keys()
                )

    
class DecoratorFactory:
    def __init__(self, which_decorator):
        self.__decorator = self.create_decorator(which_decorator)

    @staticmethod
    def create_decorator(which_decorator: str) -> Callable:
        match which_decorator:
            case 'impose_types':
                return ImposeTypesDecorator.decorate
        raise ValueError(f'Decorator: {which_decorator} do not exists')
    
    
    def get_decorator(self):
        return self.__decorator

