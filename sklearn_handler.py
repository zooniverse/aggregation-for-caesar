import os
import ctypes
from zappa.handler import LambdaHandler

for d, _, files in os.walk('lib'):
    for f in files:
        if f.endswith('.a'):
            continue
        ctypes.cdll.LoadLibrary(os.path.join(d, f))


def handler(event, context):
    return LambdaHandler.lambda_handler(event, context)
