# ./actor/INPUT_SCHEMA.json

Changes to the previous version:
- `title` removed as it's not used anywhere
- `description` removed as there is no point in placing it at the top if we add a markdown text that can be placed
  add any position between the inputs. Or is it useful for internal notes?
- define what is required at field level instead of having a separate property `"required": ["startUrls", "pageFunction"]`

The basic structure of the input schema is:

```json
{
    "versionFormat": "2",
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

We have currently 5 input types:
- String
- Boolean
- Integer
- Object
- Array

and in order to make actors easy to pipeline we should also add `log`, `dataset`, `keyValueStore` and `requestQueue` types each optionally
restricted by referenced schema. For example:

```
    "inputDataset": {
        "title": "Input dataset,
        "type": "dataset",
        "description": "Select a dataset you want to process",
        "schema": "./INPUT_DATASET_SCHEMA.json"
    },
```

There are more reference types described in [README.md](./README.md).