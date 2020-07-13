#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin
# @Software: PyCharm

import threading


lock = threading.RLock()
event = threading.Event()
