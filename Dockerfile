FROM python:3.9-buster
MAINTAINER Elico Corp <webmaster@elico-corp.com>

# Define build constants
ENV GIT_BRANCH=14.0 \
  PYTHON_BIN=python3 \
  SERVICE_BIN=odoo-bin

# Set timezone to UTC
RUN ln -sf /usr/share/zoneinfo/Etc/UTC /etc/localtime

# Generate locales
RUN apt update \
  && apt -yq install locales \
  && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
  && sed -i '/fr_CA.UTF-8/s/^# //g' /etc/locale.gen \
  && locale-gen \
  && rm -rf /var/lib/apt/lists/*

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Install dependencies
RUN set -x \
  && apt update \
  && apt install -yq \
    sudo \
    gnupg2 \
    fontconfig \
    git \
    libjpeg62-turbo-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libxml2-dev \
    libpq-dev \
    libxrender1 \
    libxslt1-dev \
    zlib1g-dev \
    dumb-init \
  # Use official PostgreSQL repos to get matching client to out version of PostgreSQL
  && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - \
  && echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" | sudo tee  /etc/apt/sources.list.d/pgdg.list \
  && apt update \
  && apt install -yq postgresql-client-13 \
  && rm -rf /var/lib/apt/lists/*

# Create the odoo user
RUN useradd --create-home --home-dir /opt/odoo --no-log-init odoo
USER odoo

# If the folders are created with "RUN mkdir" command, they will belong to root
# instead of odoo! Hence the "RUN /bin/bash -c" trick.
RUN /bin/bash -c "mkdir -p /opt/odoo/{etc,sources/odoo,additional_addons,local_addons,data,ssh}"

# Add Odoo sources and remove .git folder in order to reduce image size
WORKDIR /opt/odoo/sources
RUN git clone --depth=1 https://github.com/odoo/odoo.git -b $GIT_BRANCH && rm -rf odoo/.git

ADD sources/odoo.conf /opt/odoo/etc/odoo.conf
ADD bin/odoo-bin /opt/odoo/sources/odoo/odoo-bin
ADD auto_addons /opt/odoo/auto_addons

User 0

# Install Odoo python dependencies
RUN pip3 install -r /opt/odoo/sources/odoo/requirements.txt

# Install extra python dependencies
ADD sources/requirements.txt /opt/sources/requirements.txt
RUN pip3 install -r /opt/sources/requirements.txt

# Install wkhtmltopdf based on QT5
ADD https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
  /opt/sources/wkhtmltox.deb
RUN apt update \
  && apt install -yq xfonts-base xfonts-75dpi \
  && dpkg -i /opt/sources/wkhtmltox.deb \
  && rm -rf /var/lib/apt/lists/*

# Startup script for custom setup
ADD sources/startup.sh /opt/scripts/startup.sh

# Provide read/write access to odoo group (for host user mapping). This command
# must run before creating the volumes since they become readonly until the
# container is started.
RUN set -x \
    && chmod -R 775 /opt/odoo \
    && chown -R odoo:odoo /opt/odoo \
    && mkdir /var/lib/odoo/ \
    && chmod -R 775 /var/lib/odoo/ \
    && chown -R odoo:odoo /var/lib/odoo/ \
    && chmod +x  /opt/odoo/sources/odoo/odoo-bin

VOLUME [ \
  "/opt/odoo/etc", \
  "/var/lib/odoo/", \
  "/opt/odoo/local_addons/", \
  "/opt/odoo/additional_addons", \
  "/opt/odoo/ssh", \
  "/opt/scripts" \
]

# Use dumb-init as init system to launch the boot script
ADD bin/boot /usr/bin/boot
ENTRYPOINT [ "/usr/bin/dumb-init", "/usr/bin/boot" ]
CMD [ "start" ]

# Expose the odoo ports (for linked containers)
EXPOSE 8069 8072 8888
