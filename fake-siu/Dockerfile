FROM node:alpine

COPY package.json package.json
RUN npm install

WORKDIR /app

COPY . .

EXPOSE 3000
ENTRYPOINT ["npm", "start"]
