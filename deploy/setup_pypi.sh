#!/bin/bash

cat > $HOME/.pypirc <<EOF
[distutils]
index-servers =
    pypi

[pypi]
username:${PYPI_USER}
password:${PYPI_PASSWORD}
EOF