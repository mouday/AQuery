# -*- coding: utf-8 -*-

import logging

logger = logging.Logger("aquery")

formatter = logging.Formatter(
    fmt="[%(name)s] %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    datefmt="%Y-%m%d %H:%m:%S"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
