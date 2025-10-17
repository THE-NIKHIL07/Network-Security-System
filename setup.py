'''
the setup.py file is an essential part of packaging and distributing Python projects
.It is used by setuptools (or distutils in older python versions) to define the config
of your project,such as its metadata,dependencies,and more
'''

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str] :
    '''
    this fn will return list of requirements
    '''
    requirement_lst:List[str]=[]
    try :
        with open('requirements.txt','r') as file :
            #read lines from the file
            lines=file.readlines()
            #process each lines
            for line in lines:
                requirement=line.strip()
                #ignore empty lines and  -e .
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError :
        print("requirements.txt file not found")                

    return requirement_lst


setup(
    name="Network Security",
    version="0.0.1",
    author="Nikhil Bisht",
    author_email="nikhilbsiht058@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
