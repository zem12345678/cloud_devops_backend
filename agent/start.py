#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

"""
main 函数，程序入口文件
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir)))

import argparse
from agent.core.staring import DaemonAgent

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config')
parser.add_argument('-d', '--daemon', dest='daemon', default='false')
parser.add_argument('module')
args = parser.parse_args()


def main():
    if args.module == "agent":
        daemon_agent = DaemonAgent(args)
        daemon_agent._judge_logfile()
        if args.daemon == 'true':
            daemon_agent._daemon()
        elif args.daemon == 'false':
            daemon_agent._console()
        else:
            raise Exception("The daemon parameter must be true or false.")
    else:
        raise Exception("The module parameter must be agent.")


if __name__ == '__main__':
    main()