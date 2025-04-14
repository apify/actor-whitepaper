# Actor input schema file specification 1.0

This JSON file defines the schema and description of the input object accepted by the
Actor (see [Input](../README.md#input) for details).
The file is referenced from the main [Actor file (.actor/actor.json)](ACTOR_FILE.md) using the `input` directive,
and it is typically stored in `.actor/input_schema.json`.

The file is a JSON schema with our extensions describing a single Actor input object
and its properties, including documentation, default value, and user interface definition.

**For full reference, see [Input schema specification](https://docs.apify.com/platform/actors/development/actor-definition/input-schema/specification/v1) in Apify documentation.**

<!-- TODO: Move the full specs including JSON meta schema to this repo -->
<!-- TODO: Consider renaming "editor" values to camelCase, for consistency -->

## Example Actor input schema

```jsonc
{
  "actorInputSchemaVersion": 1,

  "title": "Input schema for an Actor",
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

    // The input value is another Dataset. The system can generate an UI to make it easy to select the dataset.
    "processDatasetId": {
      "title": "Input dataset",
      "type": "string",
      "resourceType": "dataset",
      "description": "Dataset to be processed by the Actor",
      // Optional link to dataset schema, used by the system to validate the input dataset
      "schema": "./input_dataset_schema.json"
    },
    
    "screenshotsKeyValueStoreId": {
      "title": "Screenshots to process",
      "type": "string",
      "resourceType": "keyValueStore",
      "description": "Screenshots to be compressed",
      "schema": "./input_key_value_store_schema.json"
    },
    
    "singleFileUrl": {
      "title": "Some file",
      "type": "string",
      "editor": "fileupload",
      "description": "Screenshots to be compressed",
      "schema": "./input_key_value_store_schema.json"
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
    }
     
  }
}
```

## Random notes


We could also add an `actor` resource type. The use case could be for example a testing Actor with three inputs:
- Actor to be tested
- test function containing for example Jest unit test over the output
- input for the Actor

...and the testing Actor would call the given Actor with a given output and in the end execute tests if the results are correct.

