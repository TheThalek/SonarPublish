import numpy as np

def llh2ecef(l, mu, h):
    """

    Function originally in matlab code, found  in https://github.com/cybergalactic/MSS/blob/master/GNC/llh2ecef.m
    Translated myself to python


    Converts geodetic coordinates (longitude, latitude, and height) to 
    Earth-Centered, Earth-Fixed (ECEF) coordinates.
    
    Parameters:
    - l: Longitude in radians.
    - mu: Latitude in radians.
    - h: Height above the WGS-84 ellipsoid in meters.
    
    Returns:
    - x, y, z: ECEF coordinates.
    """
    r_e = 6378137  # Radius of the Earth at the equator in meters (WGS-84)
    r_p = 6356752.3142  # Polar radius in meters (WGS-84)

    e = 0.08181979099211  # Eccentricity
    N = r_e**2 / np.sqrt((r_e * np.cos(mu))**2 + (r_p * np.sin(mu))**2)
    
    x = (N + h) * np.cos(mu) * np.cos(l)
    y = (N + h) * np.cos(mu) * np.sin(l)
    z = (N * (r_p/r_e)**2 + h) * np.sin(mu)

    return x, y, z

