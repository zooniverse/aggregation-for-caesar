'''
Intro2Astro Extractor
------------------
This module provides a function that converts the pixel annotation to wavelength and uses the subject metadata
to precalculate values required by students to use Hubble's Law to compute galactic velocity.
'''
import json
import sys
from .extractor_wrapper import extractor_wrapper

def get_annotation(classification):
    # Gets the first (only) task's annotation's 'values', pulling the first from lists when required
    annotation_values = next(iter(classification['annotations'].values()))[0]['value'][0]

    xleft = annotation_values['x']
    width = annotation_values['width']
    nw = classification['metadata']['subject_dimensions'][0]['naturalWidth']
    return {'xleft': xleft, 'width': width, 'nw': nw}

def get_galaxy_metadata(metadata):
    ra = metadata['RA']
    dec = metadata['Dec']
    z = float(metadata['#Published_Redshift'])
    galID = metadata['SVG_filename'].replace(".svg", "")
    elliptical = bool(metadata['elliptical'])
    url = metadata['URL']
    return {'ra': ra, 'dec': dec, 'z': z, 'galID': galID, 'elliptical': elliptical, 'url': url}

def calc_lambda_central(annotation):
    # Input is a annotation dictionary with x_left, width, and natural window width
    xleft = annotation['xleft']
    width = annotation['width']
    nw = annotation['nw']
    xmin = int((108. / 1152.) * nw)  # These hardcoded pixel values represent the default window sizes
    xmax = int((1081. / 1152.) * nw)  # If the actual window was sized differently, the factor of 'nw' scales the result appropriately
    lambdamin = 380.
    lambdamax = 500.
    lamperpix = (lambdamax - lambdamin) / (xmax - xmin)
    lambdacen = (xleft + (width / 2.) - xmin) * lamperpix + lambdamin
    return lambdacen

@extractor_wrapper
def i2a_extractor(classification, **kwargs):
    # import pdb; pdb.set_trace()
    response = {}
    if len(classification['annotation']) > 0:
        annotation = get_annotation(classification)
        galaxy_metadata = get_galaxy_metadata(classification['subject']['metadata'])
        lambdacen = calc_lambda_central(annotation)

        redshift = (lambdacen - 393.37) / 393.37
        velocity = 300000 * redshift
        dist = galaxy_metadata['z'] * 3e5 / 68

        response['galaxy_id'] = galaxy_metadata['galID']
        response['url'] = galaxy_metadata['url']
        response['RA'] = galaxy_metadata['ra']
        response['dec'] = galaxy_metadata['dec']
        response['dist'] = dist
        response['redshift'] = redshift
        response['velocity'] = velocity
        response['lambdacen'] = lambdacen

    return response
