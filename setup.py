from setuptools import setup, Extension

module = Extension('config', sources=['password_manager/config.pyx'])

setup(
    name='password-manager',
    version='0.0.1',
    packages=['dynaconf==3.1.7'],
    url='',
    license='',
    author='Alexander Karateev',
    author_email='administrator@gintr1k.space',
    description='',
    ext_modules=[module],
)
