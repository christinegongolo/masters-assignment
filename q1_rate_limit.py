"""
Question 1: Rate-limited caching decorator - bug analysis and fix.

BUG 1 (UnboundLocalError):
Inside wrapper(), the line:
    calls = [t for t in calls if now - t < period]
both reads and reassigns the name `calls`. Because there is an assignment
to `calls` anywhere in wrapper()'s body, Python treats `calls` as a local
variable for the *entire* function scope (this is decided at compile
time, not at runtime). So when the list comprehension tries to *read*
`calls` on the right-hand side, Python looks for a local `calls` that
has not been assigned yet -> UnboundLocalError. The closure over the
outer `calls` from decorator() is never reached because the local
assignment shadows it.

BUG 2 (state persistence across instances / decorated methods):
`calls = []` is created once, in the enclosing `decorator()` scope, when
the module is imported and the decorator is applied. If rate_limit is
used on a class method, that single `calls` list is shared by every
instance of the class - one instance can "use up" the rate limit for
every other instance, which is almost never the intended behaviour.
The fix is to key call history per-instance (or more generally, per
distinct set of arguments) instead of using one shared list.

FIX:
- Mutate the outer `calls`/`timestamps` list's *contents* in place
  (timestamps[:] = ...) rather than rebinding the name. This avoids the
  UnboundLocalError without even needing `nonlocal` (fixes Bug 1).
- Track call timestamps in a dictionary keyed on the identity of `self`
  when the wrapped function is an instance method (detected by its first
  parameter being named "self"), so each instance gets its own
  independent rate-limit window instead of sharing one global list
  (fixes Bug 2). Plain functions keep the original single shared window.
"""

import time
import functools


def rate_limit(max_calls: int, period: int):
    """Limit `func` to `max_calls` invocations per `period` seconds.

    When decorating a plain function, all calls share one window (the
    historical/expected behaviour). When decorating an instance method,
    call history is tracked per-instance (keyed on `self`'s identity),
    so each instance gets its own independent rate limit window instead
    of sharing a single counter across every instance of the class.
    """

    def decorator(func):
        call_history = {}  # key -> list[timestamps]
        # Heuristic: a plain function's first parameter is never named
        # "self"; a method's first parameter conventionally is. This
        # lets one shared key be used for functions and a per-instance
        # key be used for methods, without requiring the caller to
        # declare which kind func is.
        params = func.__code__.co_varnames[: func.__code__.co_argcount]
        is_method = bool(params) and params[0] == "self"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = id(args[0]) if (is_method and args) else "__shared__"

            timestamps = call_history.setdefault(key, [])
            # Mutate in place (no rebinding) -> avoids UnboundLocalError
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) >= max_calls:
                raise Exception("Rate limit exceeded")

            timestamps.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limit(max_calls=3, period=10)
def fetch_user_data(user_id):
    return f"Data for {user_id}"


if __name__ == "__main__":
    for i in range(3):
        print(fetch_user_data(i))
    try:
        fetch_user_data(99)
    except Exception as e:
        print(f"Expected failure: {e}")
