FROM nginx

COPY compose/nginx/nginx.conf /etc/nginx/nginx.conf
COPY compose/nginx/static_production /static
COPY compose/nginx/uwsgi_params /uwsgi_params
COPY compose/nginx/static_root_data /static_root_data
COPY compose/nginx/dist /dist
COPY compose/nginx/glossary /glossary
COPY compose/nginx/glossary/old-statics /old-statics

RUN mkdir -p /tmp/cache
RUN chmod -R 777 /tmp
EXPOSE 80
EXPOSE 8282
