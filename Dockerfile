FROM python:3.5.2

# Nginx + UWSGI + 7z
RUN apt-get update && \
    apt-get -y install \
    nginx \
    supervisor \
    uwsgi \
    p7zip-full

# Setup Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY config/flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY config/uwsgi.ini /var/www/app/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup Supervisor
RUN mkdir -p /var/log/supervisor
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy requirements and install
COPY requirements.txt /var/www/app
RUN pip3 install -r /var/www/app/requirements.txt
 
# Copy application
COPY ./app /var/www/app

# Extract database
RUN 7z x /var/www/app/database/permission_db.7z -o/var/www/app/database/

CMD ["/usr/bin/supervisord"]
