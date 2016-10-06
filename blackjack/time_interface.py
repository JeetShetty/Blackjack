import time


class Time(object):
    """A wrapper for time operations."""

    def sleep(self, x):
        """Sleeps for a specified amount of time.

        Args:
            x: Number of seconds to sleep.
        """
        time.sleep(x)
