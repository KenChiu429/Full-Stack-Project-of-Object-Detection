#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.middleware.access_middle import AccessMiddleware


def register_middleware(app) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AccessMiddleware)
