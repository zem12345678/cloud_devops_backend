#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ZhangEnmin

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bsc.production_settings")
django.setup()

