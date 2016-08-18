"""Tracker handles all user-specific processes and tasks."""

from collections import defaultdict


class Tracker(defaultdict):
    """Maps usernames to threads.

    Whenever a user process is started, the thread should be added to this
    tracker. Whenever a user process finishes, that thread should be removed
    from this tracker.
    """

    def __missing__(self, key):
        self[key] = None
        return self[key]

tracker = Tracker()
