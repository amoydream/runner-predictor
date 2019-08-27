FROM node:8.10.0-alpine
# vue-cli reqires 8.10.0+ 

RUN npm install -g @vue/cli

WORKDIR /app

EXPOSE 8080
ENV HOST=0.0.0.0
ENV CHOKIDAR_USEPOLLING=true
USER node


CMD [ "npm", "run", "dev"]