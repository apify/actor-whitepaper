
# OUTPUT_SCHEMA.json

```js
{
    "formatVersion": 1,
    "outputs": {
        // Default dataset contains all the scraped products
        "currentProducts": {
            "id": "@default",
            "type": "dataset",
            "schema": "./PRODUCTS_DATASET_SCHEMA"
        },

        // Actor uses persistent request queue and named dataset to store all historical products
        "historicalProducts": {
            "id": "~historical-products",
            "type": "dataset",
            "schema": "./PRODUCTS_DATASET_SCHEMA"
        },
        "historicalProductsQueue": {
            "id": "~historical-products",
            "type": "requestQueue"
            // Does not enforce a schema for this storage
        },

        "productImages": {
            "type": "keyValueStore",
            "schema": "./PRODUCT_IMAGES_KEY_VALUE_STORE_SCHEMA.json"
        }

        // Actor can link also schema published by other actor as its input or output
        "images": {
            "id": "@default",
            "type": "keyValueStore",
            "schema": "actor:mtrunkat~image-processor/input.imagesKeyValueStore"
        },

        // Live view
        "apiServer": {
            "type": "liveView",
            "schema": "TODO" // We should perhaps link a swagger file describing the API somehow?
        }
    }
}
```

## Examples of ideal actor run UI

- For the majority of actors we want to see the dataset with new records being added in realtime
- For [Google Spreadsheet Import](https://apify.com/lukaskrivka/google-sheets) we want to first display Live View for user to set up OAUTH and once 
this is set up then we want to display the log next time.
- For technical actors it's log
- For [HTML to PDF convertor](https://apify.com/jancurn/url-to-pdf) it's a single record from key-value store
- For [Monitoring](https://apify.com/apify/monitoring-runner) it's log during the runtime and single HTML record in iframe in the end
- For actor that has failed it's log

## How to define actor run UI

I think that ideally we need:
- Default setup, i.e. what output components should be displayed at default run tab
- Optionally the setup for different states
- Be able to pragmatically changes this using API by actor itself

TODO

## TODOs
- We have a `title` and `description` in schemas. Perhaps it's not needed there and we can have it just here?