from os import supports_follow_symlinks
import unittest
import threading
import pytest
import mock
from time import sleep
from hm_pyhelper.lock_singleton import ecc_lock, LockSingleton, ResourceBusyError

# https://gist.github.com/sbrugman/59b3535ebcd5aa0e2598293cfa58b6ab
@pytest.fixture(autouse=True, scope="function")
def error_on_raise_in_thread():
    """
    Replaces Thread with a a wrapper to record any exceptions and re-raise them after test execution.
    In case multiple threads raise exceptions only one will be raised.
    """
    last_exception = None

    class ThreadWrapper(threading.Thread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def run(self):
            try:
                super().run()
            except BaseException as e:
                nonlocal last_exception
                last_exception = e

    with mock.patch('threading.Thread', ThreadWrapper):
        yield
        if last_exception:
            raise last_exception

class TestLockSingleton(unittest.TestCase):
    def test_ecc_lock(self):
        """
        Start a slow thread then a fast thread in parallel.
        Excpect them to execute consecutively because 
        of @ecc_lock
        """
        slow_task_running_lock = threading.Lock()
        fast_task_running_lock = threading.Lock()

        @ecc_lock
        def slow_task():
            self.assertTrue(slow_task_running_lock.locked())
            self.assertTrue(fast_task_running_lock.locked())
            sleep(0.001)
            self.assertTrue(slow_task_running_lock.locked())
            self.assertTrue(fast_task_running_lock.locked())
            slow_task_running_lock.release()

        @ecc_lock
        def fast_task():
            self.assertFalse(slow_task_running_lock.locked())
            self.assertTrue(fast_task_running_lock.locked())
            sleep(0.00001)
            self.assertFalse(slow_task_running_lock.locked())
            self.assertTrue(fast_task_running_lock.locked())
            fast_task_running_lock.release()
        
        slow_thread = threading.Thread(target=slow_task, daemon=True)
        fast_thread = threading.Thread(target=fast_task, daemon=True)

        slow_task_running_lock.acquire()
        fast_task_running_lock.acquire()

        slow_thread.start()
        fast_thread.start()

    def test_lock_singleton_failure(self):

        lock = LockSingleton('test')

        # def slow_task():
        #     sleep(0.01)
        #     lock.release()
        #     return True

        # slow_thread = threading.Thread(target=slow_task, daemon=True)

        lock.acquire()
        self.assertTrue(True)
        # slow_thread.start()

        # expected_exception = False
        # try: 
        #     pass
        #     # lock.acquire(timeout=0.00001)
        # except ResourceBusyError:
        #     expected_exception = True

        # self.assertTrue(expected_exception)
