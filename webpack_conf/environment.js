const path = require("path");

module.exports = {
  paths: {
    /* Path to source files directory */
    assets: path.resolve(__dirname, "../assets/"),

    entry: path.resolve(__dirname, "../assets/webpack_entry_points"),
    /* Path to built files directory */
    output: path.resolve(__dirname, "../src/"),
  },
  server: {
    //host: "127.0.0.1",
    port: 9000,
    devMiddleware: {
      index: true,
      serverSideRender: true,
      publicPath: "/static/",
      writeToDisk: true, //	Instructs the module to write files to the configured location on disk
    },
    proxy: {
      // proxy all request except (static files) to django dev server
      "!/static/": {
        target: "http://localhost:8000/", // points to django dev server
        changeOrigin: true, // The origin of the host header is kept when proxying by default
      },
    },
  },
  limits: {
    /* Image files size in bytes. Below this value the image file will be served as DataURL (inline base64). */
    images: 8192,

    /* Font files size in bytes. Below this value the font file will be served as DataURL (inline base64). */
    fonts: 8192,
  },
};
