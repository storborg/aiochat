from __future__ import print_function

from setuptools import setup, find_packages


setup(name='aiochat',
      version='0.0.1.dev',
      description='Asyncio Chat Example',
      long_description='',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='asyncio chat websockets realtime async',
      url='https://github.com/storborg/aiochat',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'sqlalchemy',
          'aiomysql',
          'websockets',
          'asyncio_redis',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      aiochat-server = aiochat.server:main
      aiochat-client = aiochat.client:main
      """)
