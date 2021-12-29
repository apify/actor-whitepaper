# Input Schema File

A JSON object that defines structure of the input object accepted by the
actor (see [Input and Output](../README.md#input-and-output) for details).
The file is referenced from the main [actor file](ACTOR.md) using the `inputSchema` directive,
and it is typically stored in `./ACTOR/input_schema.json`.

**Backwards compatibility:** If the main actor file is missing,
the system uses the legacy [`INPUT_SCHEMA.json`](https://docs.apify.com/actors/development/input-schema) in actor's top-level directory (if present).

Changes to the legacy `INPUT_SCHEMA.json`:
- We removed `title`, it is largely useless.
- Using `actorInputSchemaVersion` instead of `schemaVersion`, to make it clear what is this file,
  as file names can be arbitrary.
- define what is required at field level instead of having a separate
  property `"required": ["startUrls", "pageFunction"]`.

The basic structure of the input schema is:

```json
{
    "actorInputSchemaVersion": 2,
    "description": "Text that is shown in the Input UI",
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "URLs to start with",
            "prefill": [
                { "url": "http://example.com" },
                { "url": "http://example.com/some-path" }
            ],
            "editor": "requestListSources",
            "required": true
        },
        "pageFunction": {
            "title": "Page function",
            "type": "string",
            "description": "Function executed for each request",
            "prefill": "async () => {return $('title').text();}",
            "editor": "javascript"
        },
        ...
    }
}
```

We have currently five input types:
- `String`
- `Boolean`
- `Integer`
- `Object`
- `Array`

And in order to make actors easy to pipeline, we should also add `actor`, `actorRun` types and also
`dataset`, `keyValueStore` and `requestQueue` types, each optionally
restricted by the referenced schema to make sure that selected storage is compatible.

TODO JC: Not sure how `actor` and `actorRun` are supposed to work? For example, if `actor`
is a reference to other actor to be called, why not use webhook?
And how about `actorRun` ???

For example:

```json
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
    // Specify records groups from the schema that actor is interested in.
    // Note that a recordGroup can be a single file too!
    "recordGroups": ["screenshots", "images"]
  }
```

This example would be rendered in Input UI as a search/dropdown that would only list named
datasets or key-value stores with matching schema. This feature will make it easy to integrate actors,
and pipe results from one to another.

Note that the actor's default dataset cannot be used as input, as it doesn't exist before the 
actor is started. That's quite logical. But it also means that if the actor wants
the default dataset to be set certain schema, this needs to be done in Output schema.

## TODOs
- We should properly reconsider our current schema format.
  For example, the way we write string enum is suboptimal as the user has to separately
  name keys and values instead of a simple map that is error-prone. (JC: Yes please!)
