FROM httpd:latest
WORKDIR /usr/local/apache2/htdocs/
RUN apt-get update \
    && apt-get install -y vim
    
COPY ["conventional/", "./"]
EXPOSE 80/tcp