from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='pleiades.notredame',
      version=version,
      description="Theme for Plone 3 with color scheme based on new Plone Logo",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone theme',
      author='Sean Gillies',
      author_email='sean.gillies@gmail.com',
      url='http://atlantides.org/trac/pleiades/browser/pleiades.notredame',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pleiades'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
