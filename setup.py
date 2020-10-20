import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='hydra_ml',  
     version='0.25',
     scripts=[] ,
     author="Michał Pogoda",
     author_email="michalpogoda@hotmail.com",
     description="Utility library for allowing to embedd ray tune samplers in hydra config",
     long_description=long_description,
   long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
