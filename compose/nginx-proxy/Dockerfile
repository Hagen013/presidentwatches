FROM nginx:latest

COPY compose/nginx-proxy/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /tmp/cache
RUN chmod -R 777 /tmp
EXPOSE 80
EXPOSE 443
EXPOSE 8282