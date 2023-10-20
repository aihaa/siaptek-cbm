import dash
import pandas as pd
import numpy as np
from netCDF4 import Dataset
import xarray as xr
import scipy.fft as fft
from scipy import signal
import base64
import io
import pymysql

connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "17200bc10B1_",
    database = "cbm_system"
)

cursor = connection.cursor()

# Opens a netCDF file and returns an object that represents the opened file (nc_handler)
def get_handle(file):
    nc_handle = Dataset(file, 'r')
    return nc_handle


# Takes file handle and a variable name as input (key), retrieves the data associated with the variable from the file, 
#            and return the data as numpy array along with the variable object itself
def get_variable_data(nc_handle, key):
    # for key in nc_handle.variables.keys():
    return np.array(nc_handle[key][:]), nc_handle[key]



# It decodes contents, identifies the file type based on its extension, and uses appropriate libraries (pandas and xarray) to read and parse the file's data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    # print(decoded)
    # print(contents)
    print(filename)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'nc' in filename:
            # Assume that the user uploaded a netCDF file
            # temp = xr.open_dataset(io.BytesIO(decoded),engine='h5netcdf').load()
            ncdata = Dataset("in-mem-file",mode='r',memory=decoded)
            temp = xr.open_dataset(xr.backends.NetCDF4DataStore(ncdata))
            # print(temp)
            df = temp
            # print(df)
        return df
    except ReferenceError:
        pass
    except Exception as e:
        raise dash.exceptions.PreventUpdate

# It calculates the absolute values of the FFT coefficients and generates corresponding frequency values. 
#           The results are stored in a pandas DataFrame and returned, representing the amplitude spectrum of the input signal.
def calculate_fft(array1, nfft, fs):

    
    fs = int(fs)                                                        # Convert the sampling frequency to an integer
    nfft = int(nfft)                                                    # Convert the number of FFT points to an integer

    fft_abs = pd.DataFrame(np.abs(fft.fft(array1, nfft)))               # Calculate the FFT of the input array and obtain the absolute values

    fft_abs.columns = ['Amplitude']                                     # Set the column name of the absolute values as 'Amplitude'
    fft_abs['Frequency'] = np.linspace(0, fs, int(fs / (fs / nfft)))    # Generate frequency values based on the sampling frequency and number of FFT points

    # Return the first half of the FFT values (up to nfft/2)
    return fft_abs.head(int(nfft / 2))




# Generates filter taps (coefficients) for different types of filters based on provided parameters
#               The function determines the filter type (lowpass, highpass, bandpass)
#               And computes the cutoff frequencies in normalized units
def get_ftaps(f_type, f_order, fc_1, fc_2, fs):
    if fc_1 != 0 and fc_2 != 0:                         # Check if both fc_1 and fc_2 are non-zero
        pass_zero = 'bandpass'                          # Set pass_zero to 'bandpass' if it's a bandpass filter
        cut_off = [x / (fs / 2) for x in [fc_1, fc_2]]  # Compute the normalized cutoff frequencies for the bandpass filter

    elif fc_1 != 0:                                     # Check if fc_1 is non-zero
        pass_zero = True                                # Set pass_zero to True if it's a highpass or lowpass filter
        cut_off = fc_1 / (fs / 2)                       # Compute the normalized cutoff frequency for the highpass or lowpass filter

    elif fc_2 != 0:                                     # Check if fc_2 is non-zero
        pass_zero = False                               # Set pass_zero to False if it's a lowpass or highpass filter
        cut_off = fc_2 / (fs / 2)                       # Compute the normalized cutoff frequency for the lowpass or highpass filter

    return signal.firwin(f_order, cut_off, window=f_type, pass_zero=pass_zero)


'''
- retrieve data from memory1 table
'''
def retrieve_files():
    cursor.execute("SELECT filename FROM memory1")
    result = cursor.fetchall()
    cursor.close()
    return [row[0] for row in result]
    # return result