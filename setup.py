from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(name='bx24_orm',
      version='0.0.2',
      description='Easy to use Django-styled API wrapper for Bitrix 24',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/dmitriilazukov/bx24_orm',
      author='Dmitrii Lazukov',
      author_email='dmitriilazukov@gmail.com',
      license='MIT',
      packages=find_packages(where='.', exclude='bx24_settings'),
      entry_points={
          'console_scripts': ['bx24_cmd=bx24_orm.scripts.command_line:bx24_cmd'],
      },
      install_requires=[
          'requests',
          'six',
          'python-dateutil'
      ],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      zip_safe=False)
