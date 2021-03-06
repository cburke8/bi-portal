ARG VARIANT="3.8"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
# FROM python:${VARIANT}

# define the user that is not root
ARG NB_USER=regularuser
ARG NB_UID=1000
ARG NB_GID=999
ARG APP_DIR=mainsite

USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install --no-install-recommends make rsync \
    && pip install pipenv \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# add a script that we will use to correct permissions after running certain commands
COPY ./docker/fix-permissions /usr/local/bin/fix-permissions
RUN chmod +x /usr/local/bin/fix-permissions

# install dependencies
COPY ./requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY ./mainsite /mainsite
RUN  fix-permissions "/mainsite"
RUN chmod +x /mainsite/bootstrap.sh

# create a user that is not root
RUN \
    groupadd -g $NB_GID $NB_USER && \
    useradd -u $NB_GID -g $NB_USER -G sudo -m -s /bin/bash $NB_USER && \
    sed -i /etc/sudoers -re 's/^%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^root.*/root ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^#includedir.*/## **Removed the include directive** ##"/g' && \
    echo "$NB_USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "Customized the sudoers file for passwordless access to the $NB_USER user!" && \
    chown $NB_USER:$NB_GID "/mainsite" && \
    chmod g+w /etc/passwd

ENTRYPOINT /mainsite/bootstrap.sh

WORKDIR /mainsite
EXPOSE 8888
USER $NB_USER


