FROM mcr.microsoft.com/vscode/devcontainers/python:1-3.11

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    setuptools \
    poetry \
    && rm -rf /tmp/pip-tmp

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
