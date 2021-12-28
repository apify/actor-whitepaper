# ./actor/INPUT_SCHEMA.json

Changes to the previous version:
- `formatVersion` instead of `schemaVersion`
- define what is required at field level instead of having a separate property `"required": ["startUrls", "pageFunction"]`

The basic structure of the input schema is:

```json
{
    "formatVersion": "2",
    "title": "My actor schema",
    "description": "....",
    "properties": [
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
    ]
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
- We should properly reconsider our current format. For example, the way we write string enum is suboptimal as the user has to separately name keys and values instead of a simple map that is error-prone.
