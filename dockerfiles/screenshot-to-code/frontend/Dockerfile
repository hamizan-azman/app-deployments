FROM node:22-bullseye-slim

WORKDIR /app

COPY package.json yarn.lock /app/

ENV PUPPETEER_SKIP_DOWNLOAD=true

RUN yarn install

COPY ./ /app/

RUN chown -R node:node /app

USER node

EXPOSE 5173

HEALTHCHECK --interval=15s --timeout=10s --start-period=30s --retries=3 \
    CMD node -e "const http = require('http'); const req = http.request({host:'localhost',port:5173,path:'/'}, (res) => { process.exit(res.statusCode < 500 ? 0 : 1); }); req.on('error', () => process.exit(1)); req.end();" || exit 1

CMD ["yarn", "dev", "--host", "0.0.0.0"]
