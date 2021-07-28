# pull base image
FROM nginx:1.19.0-alpine
EXPOSE 8004
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
