The web-crawler crawls the web and builds the graph of web documents' urls.

TODOs:

* Process only specific media type: `text/html`

    * Possible solution: request a resource with `GET` and consider the `Content-Type` header
    * Possible solution: request only a header with `HEAD` request. Needs to be proved if there are servers which don't implement the method

* Find urls in the `text/html` document. At the moment the only reasonable source of uls is the `<a href="url">` html tag.

* Handle relative urls within the document.

* Handle url parameters. Since one url may accept parameters the generated pages may be infinite

    * For example, a hotel reservation system may have the url `www.travel-example.com/query?from=2014-07-14&until=2014-08-01`.
    Possible parameters `from` and `until` may accept a wide range of dates. It needs to be understood how to handle such urls.