'''

:Authors: Sana dev team
:Version: 2.0
'''
import logging

try:
    import threading
    threading_supported = True
except ImportError:
    threading_supported = False

__all__ = ['threading_supported', 'ThreadBufferedHandler']

class ThreadBufferedHandler(logging.Handler):
    """
    A logging handler that buffers records by thread.
    """
    
    def __init__(self):
        if not threading_supported:
            raise NotImplementedError("ThreadBufferedHandler cannot be used "
                "if threading is not supported.")
        logging.Handler.__init__(self)
        self.records = {} # Dictionary (Thread -> list of records)

    def emit(self, record):
        """ 
        Append the record to the buffer for the current thread. 
        
        Parameters:
            record 
                A log entry to append.
        """
        self.get_records().append(record)

    def get_records(self, thread=None):
        """
        Gets the log messages for a thread.
        
        Parameters:
            thread
                The thread to get messages for or the current thread if
                no thread is specified.
        """
        if not thread:
            thread = threading.currentThread()
        if thread not in self.records:
            self.records[thread] = []
        return self.records[thread]

    def clear_records(self, thread=None):
        """
        Clears the log messages for a thread.
        
        Parameters:
            thread 
                The thread to clear messages for or the current thread if
                no thread is specified.
        """
        if not thread:
            thread = threading.currentThread()
        if thread in self.records:
            del self.records[thread]