from setuptools import setup, find_packages

PACKAGES = find_packages(where='.', exclude='bx24_settings')

setup(name='bx24_orm',
      version='0.0.1',
      description='Easy to use Django-styled API wrapper for Bitrix 24',
      url='https://github.com/dmitriilazukov/bx24_orm',
      author='Dmitrii Lazukov',
      author_email='dmitriilazukov@gmail.com',
      license='MIT',
      packages=PACKAGES,
      entry_points={
          'console_scripts': ['bx24_cmd=bx24_orm.scripts.command_line:bx24_cmd'],
      },
      install_requires=[
          'requests',
          'six',
          'python-dateutil'
      ],
      zip_safe=False)
