FROM python:3.5.2

# Install Java 8 (in order to run the Permission Checker)
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" | tee /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -t jessie-backports openjdk-8-jre-headless -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install Nginx + UWSGI + 7z
RUN apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get -y install \
    nginx \
    supervisor \
    uwsgi \
    p7zip-full

# Define JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Copy SSL certificates (only when enabling SSL on the server)
# COPY riskindroid.pem /etc/ssl/

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
RUN 7z x /var/www/app/database/permission_db.7z -o/var/www/app/database/ -y

CMD ["/usr/bin/supervisord"]
