"""
Question 2: Lightweight Event Dispatcher using the Observer Pattern.

- subscribe(event_type, callback): registers callback for event_type.
- unsubscribe(event_type, callback): removes it.
- dispatch(event_type, *args, **kwargs): calls every registered callback
  for event_type, in registration order, passing through *args/**kwargs.
  If a callback raises, the error is logged/printed and dispatch
  continues with the remaining callbacks.
"""

from collections import defaultdict


class EventDispatcher:
    def __init__(self):
        # dict preserves insertion order in Python 3.7+, which is what
        # guarantees callbacks run in the order they were registered.
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type: str, callback: callable) -> None:
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: callable) -> None:
        subscribers = self._subscribers.get(event_type)
        if not subscribers:
            return
        try:
            subscribers.remove(callback)
        except ValueError:
            pass  # callback wasn't registered; nothing to do

    def dispatch(self, event_type: str, *args, **kwargs) -> None:
        for callback in list(self._subscribers.get(event_type, [])):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"[EventDispatcher] error in callback for "
                      f"'{event_type}': {e}")


if __name__ == "__main__":
    dispatcher = EventDispatcher()

    def on_login(user):
        print(f"1: welcome {user}")

    def on_login_broken(user):
        raise RuntimeError("boom")

    def on_login_last(user):
        print(f"3: audit log for {user}")

    dispatcher.subscribe("login", on_login)
    dispatcher.subscribe("login", on_login_broken)
    dispatcher.subscribe("login", on_login_last)

    dispatcher.dispatch("login", "andrew")

    dispatcher.unsubscribe("login", on_login_broken)
    print("--- after unsubscribe ---")
    dispatcher.dispatch("login", "andrew")
