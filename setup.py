#!/usr/bin/python2.7
from setuptools import setup
from subprocess import call

setup(name='PASM',
      version='1.0',
      description='PASM Linux assembler/disassembler',
      author='TheSecondSun',
      author_email='thescndsun@gmail.com'
     )

call("pip install -r requirements.txt", shell=True)
call("apt-get install radare2", shell=True)

