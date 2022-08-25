#Build environment
FROM node:14-alpine3.10

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Set node in path
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# TODO: abstract dev mock infra from prod

# Copy over dependencies & install
COPY package.json /usr/src/app/package.json
# TODO: yarn install --production
RUN yarn install

# Copy all project files over & build
COPY . /usr/src/app
RUN yarn build

ENV PORT 80
EXPOSE 80
