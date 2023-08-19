from setuptools import setup

setup(
   name='cube-stability',
   version='1.0',
   description='cube stability',
   author='Lewis Clark',
   author_email='lewisclarkan@gmail.com',
   packages=['foo'],  #same as name
   install_requires=['numpy', 'pandas', 'plotly'], #external packages as dependencies
)