# Actor input schema file specification 1.0

This JSON file defines the schema and description of the input object accepted by the
Actor (see [Input](../README.md#input) for details).
The file is referenced from the main [Actor file (.actor/actor.json)](ACTOR_FILE.md) using the `input` directive,
and it is typically stored in `.actor/input_schema.json`.

It defines input properties for an Actor, including documentation, default value, and user interface definition.

## Example Actor input schema

```jsonc
{
    "actorInputSchemaVersion": 1,
    "title": "Input schema for Website Content Crawler",
    "description": "Enter the start URL(s) of the website(s) to crawl, configure other optional settings, and run the Actor to crawl the pages and extract their text content.",
    "type": "object",
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "One or more URLs of the pages where the crawler will start. Note that the Actor will additionally only crawl sub-pages of these URLs. For example, for the start URL `https://www.example.com/blog`, it will crawl pages like `https://example.com/blog/article-1`, but will skip `https://example.com/docs/something-else`.",
            "editor": "requestListSources",
            "prefill": [{ "url": "https://docs.apify.com/" }]
        },
        "crawlerType": {
            "sectionCaption": "Crawler settings",
            "title": "Crawler type",
            "type": "string",
            "enum": ["playwright:chrome", "cheerio", "jsdom"],
            "enumTitles": ["Headless web browser (Chrome+Playwright)", "Raw HTTP client (Cheerio)", "Raw HTTP client with JS execution (JSDOM) (experimental!)"],
            "description": "Select the crawling engine:\n- **Headless web browser** (default) - Useful for modern websites with anti-scraping protections and JavaScript rendering. It recognizes common blocking patterns like CAPTCHAs and automatically retries blocked requests through new sessions. However, running web browsers is more expensive as it requires more computing resources and is slower. It is recommended to use at least 8 GB of RAM.\n- **Raw HTTP client** - High-performance crawling mode that uses raw HTTP requests to fetch the pages. It is faster and cheaper, but it might not work on all websites.",
            "default": "playwright:chrome"
        },
        "maxCrawlDepth": {
            "title": "Max crawling depth",
            "type": "integer",
            "description": "The maximum number of links starting from the start URL that the crawler will recursively descend. The start URLs have a depth of 0, the pages linked directly from the start URLs have a depth of 1, and so on.\n\nThis setting is useful to prevent accidental crawler runaway. By setting it to 0, the Actor will only crawl start URLs.",
            "minimum": 0,
            "default": 20
        },
        "maxCrawlPages": {
            "title": "Max pages",
            "type": "integer",
            "description": "The maximum number pages to crawl. It includes the start URLs, pagination pages, pages with no content, etc. The crawler will automatically finish after reaching this number. This setting is useful to prevent accidental crawler runaway.",
            "minimum": 0,
            "default": 9999999
        },
        // ...
    }
}
```

## Random notes

To make Actors easier to pipeline, we could add e.g. 
`dataset`, `keyValueStore` and `requestQueue` types, each optionally
restricted by the referenced schema to make sure that selected storage is compatible.

Another idea is to add type `actor`. The use case could be for example a testing Actor with 3 inputs:
- Actor to be tested
- test function containing for example Jest unit test over the output
- input for the Actor

...and the testing Actor would call the given Actor with a given output and in the end execute tests if the results are correct.



For example:

```jsonc
  "inputDataset": {
    "title": "Input dataset",
    "type": "dataset",
    "schema": "./input_dataset_schema.json",
    "description": "Dataset to be processed",
  },

  "inputScreenshots": {
    "title": "Input screenshots",
    "type": "keyValueStore",
    "description": "Screenshots to be compressed",
    "schema": "./input_key_value_store_schema.json",
    // Specify records groups from the schema that Actor is interested in.
    // Note that a recordGroup can be a single file too!
    "recordGroups": ["screenshots", "images"]
  }
```

This example would be rendered in Input UI as a search/dropdown that would only list named
datasets or key-value stores with matching schema. This feature will make it easy to integrate Actors,
and pipe results from one to another.
Note from Franta: It would be cool to have an option in the dropdown to create a
new dataset/key-value store with the right schema,
if it's the first time you're running some Actor,
and then in the next runs you could reuse it.
