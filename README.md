The web-crawler crawls the web and builds the graph of web documents' urls.

TODOs:

* DONE<s>Process only specific media type: `text/html`</s>

    * Possible solution: request a resource with `GET` and consider the `Content-Type` header
    * <s>Possible solution: request only a header with `HEAD` request. Needs to be proved if there are servers which don't implement the method</s> Some servers do not answer to `HEAD` requests.

* Find urls in the `text/html` document. At the moment the only reasonable source of uls is the `<a href="url">` html tag.
    * Unable to parse data from [http://maps.google.de/maps?hl=de&tab=wl], error [line 41: htmlParseEntityRef: no name]

* Handle relative urls within the document.

* Handle url parameters. Since one url may accept parameters the generated pages may be infinite

    * For example, a hotel reservation system may have the url `www.travel-example.com/query?from=2014-07-14&until=2014-08-01`.
    Possible parameters `from` and `until` may accept a wide range of dates. It needs to be understood how to handle such urls.

* Persist the url graph periodically and implement possibility to start with the persisted graph

* Create configuration file and a small library to access it
    * Separate the configuration for tests and production