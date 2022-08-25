module.exports = {
    // serverRuntimeConfig: {
    //     // Will only be available on the server side
    //     mySecret: 'secret',
    //     secondSecret: process.env.SECOND_SECRET, // Pass through env variables
    //   },
    env: {
        // TODO: dev vs prod
        USER_AUTH_URL: "http://127.0.0.1:5001/api/v0.1/",
        CRUD_SERVICE_URL: "http://127.0.0.1:5002/api/v0.1/",
        GEOCODE_SERVICE_URL: "http://127.0.0.1:5003/api/v0.1/geocode",
        DEPOT_SERVICE_URL: "http://127.0.0.1:5004/api/v0.1/depot",
        ROUTE_SERVICE_URL: "http://127.0.0.1:5005/api/v0.1/route",
    },
    webpackDevMiddleware: config => { // TODO: dev-specific
        config.watchOptions = {
          poll: 800,
          aggregateTimeout: 300,
        }
        return config
      },
};
