Introduction
============
*QENSlibrary* is a repository containing models (mathematical functions) that
could be used to fit Quasi Elastic Neutron Scattering (QENS) data.


Installation
============

Support Python 2.7 and 3 (**to check and specify**)


Requirements
------------

Python modules:
- [numpy](http://www.numpy.org/)

How to install?
------------
Download or clone the repository following the instructions given at [link](https://github.com/QENSlibrary/QENSmodels)


To install the package, type the following 
command in a terminal::

```
pip install -e . path/to/QENSlibrary_folder
```

Testing installation, **to be added**

How to build documentation?
------------

In a terminal, move to the */docs* folder and type::

   make html
   
This command will generate html files in the subfolder *_build/html*.

Documentation
=============

How to use?
-----------
```python
import QENSmodels
value= QENSmodels.lorentzian(1,1,1,1)

```
or copy and paste the script.

The scripts can be found in the [git repository](https://github.com/QENSlibrary/QENSmodels)

How to cite?
------------
Add reference or ...

Need help / report a problem / found a bug
------------------------------------------

Add link to websites, email addresses...


TODO
====
- structure of library: folders and contents
- complete README.md files
- add license
- add other models
- add examples: jupyter notebook / python scripts
- add instructions in Contributing
- add tests
- add instruction in installation / setup.py
