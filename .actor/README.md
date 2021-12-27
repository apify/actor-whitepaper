# Contents of the `.actor` directory

Please first check the following files for the context:
- [ACTOR.md](./ACTOR.md) description of `.actor/ACTOR.json`
- [DATASET_SCHEMA.md](./DATASET_SCHEMA.md)
- [KEY_VALUE_STORE_SCHEMA.md](./KEY_VALUE_STORE_SCHEMA.md)
- [REQUEST_QUEUE_SCHEMA.md](./REQUEST_QUEUE_SCHEMA.md)

These files describes the main `.actor/ACTOR.json` and format for storage schemas. Each actor has one `.actor/ACTOR.json` file and
may have any number of storage schema files. What is missing now is the description of input and output of the actor described by

- `.actor/INPUT_SCHEMA.json` (see [ACTOR.md](./INPUT_SCHEMA.md)) - not done yet
- `.actor/OUTPUT_SCHEMA.json` (see [OUTPUT_SCHEMA.md](./OUTPUT_SCHEMA.md)) - not done yet

## Input schema

Input schema as described in our [docs](https://docs.apify.com/actors/development/input-schema#fields) should be simplified and extended
by a couple of new field types. For example `dataset`, `request_queue`, `key_value_store`, `log`, ... . This will allow to ensure that for
example the dataset passed on input is compatible and so will allow easier pipelining of actors later:

```js
{
    "title": "Google Search ads extractor",
    "description": "Takes a result of google search scraper and extracts ads",
    "type": "object",
    "formatVersion": 2,
    "properties": {
        "dataset": {
            "title": "Input dataset,
            "type": "dataset",
            "description": "Select a dataset of Google Search Scraper actor",
            "schema": "TODO"
        },
        ...
```

where as schema should be possible to link a local file `./INPUT_DATASET_SCHEMA.json` or certain build of actor `apify/google-search-scraper@latest/default` or even a certain dataset (I don't know how as the naming is not unique across dataseta/actors/tasks/...).

## Output schema

Is a list of different output types of the actor consiting of:

- dataset defined by schema (default, some named that is being reused, in the future another unnamed linked to the run)
- key-value store defined by schema (-||-)
- request queue defined by schema (-||-)
- live-view which should say if it's HTML page or API defined by Swagger doc or other
- log (do we need it here?)
- ... maybe more in the future

With format close to Honza's https://github.com/apify/actor-specs/blob/master/Schema%20Experiments%20by%20jan/google_search_scraper/.actor/OUTPUT_SCHEMA.json

## Run UI in Apify Console

Now what is missing is the description of the main run view tab. What do we need here?

- For the majority of actors we want to see the dataset with new records being added in realtime
- For [Google Spreadsheet Import](https://apify.com/lukaskrivka/google-sheets) we want to first display Live View for user to set up OAUTH and once 
this is set up then we want to display the log next time.
- For technical actors it's log
- For [HTML to PDF convertor](https://apify.com/jancurn/url-to-pdf) it's a single record from key-value store
- For [Monitoring](https://apify.com/apify/monitoring-runner) it's log during the runtime and single HTML record in iframe in the end
- For actor that has failed it's log

So I think that ideally we need:
- Default value
- Optionally the value for different states
- Be able to pragmatically changes this using API by actor itself

I am not 100% convinced if this belongs to `OUTPUT_SCHEMA.json` or to `ACTOR.json`. But it could look like the following:

TODO

## Other notes

- I'd make all schemas weak. I.e. for example some deduplication actor could require each dataset item to have a `uuid: 'string'` field but does not care about anything else. And similarly for key-value stores - schema expects something to be there but does not care about other values.
- How to integrate output schema with `const { output } = await Apify.call(...)`?
