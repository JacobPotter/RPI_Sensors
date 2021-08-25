from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(name              = 'MDT_Sensors',
      version           = '1.0.0',
      author            = 'Jacob Potter',
      author_email      = 'pttr.jcb@gmail.com',
      description       = 'Python code to use the MCP3008 analog to digital converter with a Raspberry Pi or BeagleBone black. sends voltage values to influxdb',
      license           = 'MIT',
      classifiers=[

             # Indicate who your project is intended for
             'Intended Audience :: Agricultural and Industrial Monitoring/IOT',
             'Topic :: IOT :: Sensors',

             # Pick your license as you wish (should match "license" above)
              'License :: OSI Approved :: MIT License',

             # Specify the Python versions you support here. In particular, ensure
             # that you indicate whether you support Python 2, Python 3 or both.
             'Programming Language :: Python :: 2.7'   
         ],
      url               = 'https://github.com/adafruit/Adafruit_Python_MCP3008/',
      install_requires  = [
                            'Adafruit-GPIO>=0.6.5',
                            'Adafruit-MCP3008'
                        ],
      packages          = find_packages())
