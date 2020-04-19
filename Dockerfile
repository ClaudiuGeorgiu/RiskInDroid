FROM python:3.8.2-slim-buster

# Install the needed tools.
RUN bash -c 'for i in {1..8}; do mkdir -p "/usr/share/man/man$i"; done' && \
    apt update && apt install --no-install-recommends -y \
    openjdk-11-jre-headless nginx supervisor p7zip-full gcc libc6-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Setup Supervisor.
RUN mkdir -p /var/log/supervisor/
COPY ./config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup Nginx.
COPY ./config/nginx-flask.conf /etc/nginx/sites-available/
RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/nginx-flask.conf /etc/nginx/sites-enabled/nginx-flask.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

# Install and setup uWSGI.
RUN pip3 install --no-cache-dir --upgrade uwsgi pip
COPY ./config/uwsgi.ini /var/www/app/

# Copy requirements and install.
COPY ./requirements.txt /var/www/app/
RUN pip3 install --no-cache-dir -r /var/www/app/requirements.txt

# Copy application.
COPY ./app /var/www/app/

# Extract the compressed database.
RUN 7z x /var/www/app/database/permission_db.7z -o/var/www/app/database/ -y

# The app doesn't run as root, make sure it can access the files.
RUN chmod -R a+rw /var/www/app/

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
