#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin

import os
import sys
from agent import Agent
from configparser import ConfigParser
from logging.config import fileConfig
import daemon


class DaemonAgent:
    @classmethod
    def __init__(self, args):
        self.args = args

    def _console(self):
        """ 前台输出 """

        home = os.path.abspath(os.path.dirname(sys.argv[0]))

        if os.path.exists(os.path.join(home, "conf/logging.ini")):
            fileConfig(os.path.join(home, "conf/logging.ini"))

        config = ConfigParser()
        if self.args.config:
            config.read(self.args.config)
        else:
            config.read(os.path.join(home, "conf/config.ini"))

        workspace = config.get("agent", "workspace")
        if not os.path.isabs(workspace):
            workspace = os.path.join(home, workspace)
        agent = Agent(config.get("agent", "host"), config.getint("agent", "port"), workspace)
        try:
            agent.start()
        except KeyboardInterrupt:
            agent.shutdown()

    def _daemon(self):
        """ 启动为守护进程 """

        context = daemon.DaemonContext(working_directory=os.path.abspath(os.path.dirname(sys.argv[0])),)
        context.open()
        with context:
            self._console()

    def _judge_logfile(cls):
        """ 判断日志文件是否存在 """

        logdir = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "logs")
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        if not os.path.exists(os.path.join(logdir, "agent.log")):
            os.mknod(os.path.join(logdir, "agent.log"))
