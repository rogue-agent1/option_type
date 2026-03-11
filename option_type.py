#!/usr/bin/env python3
"""option_type — Option/Result monads for safe error handling. Zero deps."""

class Option:
    def __init__(self, value=None, _none=False):
        self._value = value
        self._is_none = _none or (value is None and not isinstance(value, int))

    @staticmethod
    def some(value): return Option(value)
    @staticmethod
    def none(): return Option(_none=True)

    @property
    def is_some(self): return not self._is_none
    @property
    def is_none(self): return self._is_none

    def unwrap(self):
        if self._is_none: raise ValueError("Unwrap on None")
        return self._value

    def unwrap_or(self, default):
        return default if self._is_none else self._value

    def map(self, fn):
        return Option.none() if self._is_none else Option.some(fn(self._value))

    def flat_map(self, fn):
        return Option.none() if self._is_none else fn(self._value)

    def filter(self, pred):
        if self._is_none or not pred(self._value): return Option.none()
        return self

    def __repr__(self):
        return "None" if self._is_none else f"Some({self._value!r})"

class Result:
    def __init__(self, value=None, error=None):
        self._value, self._error = value, error
        self._is_ok = error is None

    @staticmethod
    def ok(value): return Result(value=value)
    @staticmethod
    def err(error): return Result(error=error)

    @property
    def is_ok(self): return self._is_ok

    def unwrap(self):
        if not self._is_ok: raise ValueError(f"Unwrap on Err: {self._error}")
        return self._value

    def unwrap_err(self):
        if self._is_ok: raise ValueError("unwrap_err on Ok")
        return self._error

    def map(self, fn):
        return Result.ok(fn(self._value)) if self._is_ok else self

    def flat_map(self, fn):
        return fn(self._value) if self._is_ok else self

    def map_err(self, fn):
        return self if self._is_ok else Result.err(fn(self._error))

    def __repr__(self):
        return f"Ok({self._value!r})" if self._is_ok else f"Err({self._error!r})"

def safe_div(a, b):
    return Result.err("division by zero") if b == 0 else Result.ok(a / b)

def main():
    print("Option Monad:")
    x = Option.some(42)
    print(f"  {x}.map(x*2) = {x.map(lambda v: v*2)}")
    print(f"  None.map(x*2) = {Option.none().map(lambda v: v*2)}")
    print(f"  {x}.filter(>50) = {x.filter(lambda v: v > 50)}")
    chain = Option.some(10).map(lambda x: x+5).flat_map(lambda x: Option.some(x*2) if x > 10 else Option.none())
    print(f"  Chain: {chain}")

    print("\nResult Monad:")
    print(f"  10/3 = {safe_div(10, 3)}")
    print(f"  10/0 = {safe_div(10, 0)}")
    chain = safe_div(100, 4).flat_map(lambda x: safe_div(x, 5))
    print(f"  100/4/5 = {chain}")
    chain2 = safe_div(100, 0).flat_map(lambda x: safe_div(x, 5))
    print(f"  100/0/5 = {chain2}")

if __name__ == "__main__":
    main()
