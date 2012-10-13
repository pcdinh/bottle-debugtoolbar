import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
except:
    README = ''


setup(
    name='Bottle-DebugToolbar',
    version='0.3',
    url='http://github.com/sramana/bottle-debugtoolbar',
    license='BSD',
    author='Ramana Varanasi',
    author_email='ramana.varanasi@gmail.com',
    description='A port of the Django Debug Toolbar to Bottle',
    long_description=README,
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    packages=['bottle_debugtoolbar',
              'bottle_debugtoolbar.panels'
    ],
    install_requires=[
        'bottle>=0.11.2',
        'jinja2>=2.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
