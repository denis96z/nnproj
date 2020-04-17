FROM node:13.14.0 as base
WORKDIR /tmp
COPY . .
RUN npm install && npm run build --prod

FROM nginx:1.19.0
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=base /tmp/dist/nnproj /var/www
