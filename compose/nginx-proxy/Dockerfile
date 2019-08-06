FROM nginx:latest

COPY compose/nginx-proxy/nginx.conf /etc/nginx/nginx.conf
COPY compose/nginx-proxy/files /files
COPY compose/nginx-proxy/ssl /ssl
COPY compose/nginx/static_production /static
COPY compose/nginx/static_root_data /static_root_data
COPY compose/nginx/dist /static_root_data/dist

RUN mkdir -p /tmp/cache
RUN chmod -R 777 /tmp
EXPOSE 80
EXPOSE 443
EXPOSE 8282