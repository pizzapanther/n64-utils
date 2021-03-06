#!/usr/bin/env python3

import platform
import subprocess
import sys

OSes = {
  'amazon': {
    'sudo': True,
    'cmds': [
      'yum -y groupinstall development',
      'yum -y install {pkgs}',
      'pip-3.6 install neutron-beam',
    ],
    'pkgs': [
      'yum-utils',
      'python36',
      'python36-pip',
    ],
  },
  'deb': {
    'sudo': True,
    'cmds': [
      'apt update',
      'apt install -y {pkgs}',
      'pip3 install neutron-beam',
    ],
    'pkgs':[
      'build-essential',
      'python3',
      'python3-apt',
      'python3-pip',
      'python3-dev',
      'python3-setuptools',
      'python3-wheel',
    ]
  },
  'centos': {
    'sudo': True,
    'cmds': [
      'yum -y install https://centos7.iuscommunity.org/ius-release.rpm',
      'yum -y groupinstall development',
      'yum -y install {pkgs}',
      'pip3.6 install neutron-beam',
    ],
    'pkgs': [
      'yum-utils',
      'python36u',
      'python36u-pip',
    ],
  },
  'termux': {
    'sudo': False,
    'cmds': [
      'pkg install -y {pkgs}',
      'pip3 install neutron-beam',
    ],
    'pkgs': [
      'python',
      'clang',
      'python-dev',
      'libcrypt-dev'
    ],
  }
}

def run_cmd (cmd, context, sudo=True):
  run_cmd = cmd.format(**context)
  if sudo:
    run_cmd = 'sudo -H ' + run_cmd

  print('Command:', run_cmd)
  ret = subprocess.call(run_cmd, shell=True)
  if ret:
    print('!!! Error in installation !!!')
    sys.exit(ret)

def install(os):
  pkgs = ' '.join(OSes[os]['pkgs'])
  context = {'pkgs': pkgs}
  for cmd in OSes[os]['cmds']:
    run_cmd(cmd, context, OSes[os]['sudo'])

def run ():
  os = 'unknown'
  linux = platform.linux_distribution()[0]
  if 'ubuntu' in linux.lower():
    os = 'deb'
  elif 'debian' in linux.lower():
    os = 'deb'
  elif 'centos' in linux.lower():
    os = 'centos'

  if os == 'unknown':
    pform = platform.platform()
    if 'amzn' in pform:
      os = 'amazon'

    try:
      subprocess.call('termux-info')

    except:
      pass

    else:
      os = 'termux'

  if os == 'unknown':
    print('Unkwown OS, try manual installation')
    sys.exit(1)

  install(os)

  print("--- Installation Complete ---")
  print("Run: nbeam setup_local, nbeam setup_remote, or nbeam setup_termux to continue")

if __name__ == '__main__':
  run()
