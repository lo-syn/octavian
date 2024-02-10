from scipy.io import wavfile
import numpy as np

class DataWrapper(object):

    '''
    Accepts data and returns it as an Object
    This is mainly just to allow all processing functions to work

    Parameters
    ----------
    file_path : str
        Path for file

    Returns
    -------
    file : DataWrapper.signal
        Returns a list of arrays with audio file signal

    time_axis : DataWrapper.time_axis
        Returns a 1D array with the time axis

    Examples
    --------
    >>> wrapped_data = DataWrapper(data)

    .. plot::

    '''

    def __init__(self, 
                data: list,
                ):
        DataWrapper._check_parameters(data)
        self.run()
    
    def wrap_data(self):
        '''
        This function wraps data
        '''
        pass

    def run(self):
        self.wrap_data()
        
    @staticmethod
    def _check_parameters(data):
        """Checks the parameters for data, raises exceptions if necessary."""
        pass # Should add a check that data is ok