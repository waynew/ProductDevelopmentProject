import os
from setuptools import setup, find_packages

install_requires = [
    'flask',
    'flask-sqlalchemy',
]
setup(
    name='risks',
    version='0.1.0',
    author='Wayne Werner',
    author_email='waynejwerner@gmail.com',
    url='TODO',
    entry_points = {
        'console_scripts': [
            'risks=risks:run',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
)
