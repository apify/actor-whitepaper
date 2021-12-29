# Input schema

A JSON object that defines structure of the input object accepted by the
actor (see [Get input](../README.md#get-input) for details).
The file is referenced from the main [actor file](ACTOR.md) using the `inputSchema` directive,
and it is typically stored in `./ACTOR/input_schema.json`.

**Backwards compatibility:** If the main actor file is missing,
the system uses the legacy [`INPUT_SCHEMA.json`](https://docs.apify.com/actors/development/input-schema) in actor's top-level directory (if present).

Changes to the legacy `INPUT_SCHEMA.json`:
- `inputSchemaVersion` instead of `schemaVersion`, to make it clear what is this file, as file names can be arbitrary.
- define what is required at field level instead of having a separate property `"required": ["startUrls", "pageFunction"]`

The basic structure of the input schema is:

```json
{
    "inputSchemaVersion": "2",
    "title": "My actor schema",
    "description": "....",
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
- String
- Boolean
- Integer
- Object
- Array

And in order to make actors easy to pipeline, we should also add `actor`, `actorRun` types and also
`dataset`, `keyValueStore` and `requestQueue` types, each optionally
restricted by the referenced schema to make sure that selected storage is compatible. For example:

```
    "inputDataset": {
        "title": "Input dataset,
        "type": "dataset",
        "description": "Select a dataset you want to process",
        "schema": "./INPUT_DATASET_SCHEMA.json"
    },
```

## TODOs
- JC: Do we really need `title`? What for? I'd skip it and keep just `description`, which is shown in the Input UI.
  Equally, for the output schema do the same...
- We should properly reconsider our current format.
  For example, the way we write string enum is suboptimal as the user has to separately
  name keys and values instead of a simple map that is error-prone. (JC: Yes please!)
