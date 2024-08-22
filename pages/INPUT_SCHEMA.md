# Actor input schema file specification

This JSON file defines the schema and description of the input object accepted by the
Actor (see [Input](../README.md#input) for details).
The file is referenced from the main [Actor file (.actor/actor.json)](ACTOR_FILE.md) using the `input` directive,
and it is typically stored in `.actor/input_schema.json`.

NOTE: Currently the Apify platform only supports [input schema version 1](https://docs.apify.com/Actors/development/input-schema),
this document describes how the version 2 should look like, but it's not implemented yet.

**Backwards compatibility:** If the main Actor file is missing,
the system uses the legacy [`INPUT_SCHEMA.json`](https://docs.apify.com/Actors/development/input-schema) in Actor's top-level directory (if present).


## Older ideas that might never materialize

Changes to the legacy `INPUT_SCHEMA.json`:
- We removed `title`, it is largely useless.
- Using `actorSpecification` instead of `schemaVersion`, to make it clear what is this file,
  as file names can be arbitrary.
- define what is required at field level instead of having a separate
  property `"required": ["startUrls", "pageFunction"]`.

The basic structure of the input schema is:

```jsonc
{
    "actorInputSchemaVersion": 1,
    "description": "Text that is shown in the Input UI",
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "Array",
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
            "type": "String",
            "description": "Function executed for each request",
            "prefill": "async () => {return $('title').text();}",
            "editor": "javascript"
        },
        ...
    }
}
```

We have currently five input types:
- `String` / `string`
- `Boolean` / `boolean`
- `Integer` / `integer`
- `Object` / `object`
- `Array` / `array`

Other types like `DefaultDataset` must start with upper case.

And in order to make Actors easy to pipeline, we should also add `actor`, `actorRun` types and also
`dataset`, `keyValueStore` and `requestQueue` types, each optionally
restricted by the referenced schema to make sure that selected storage is compatible.


NOTE from Mara: The idea was that we should have an input type for any system resource,
so perhaps even for the user. But it's a super low priority.

The use case for `actor` could be for example a testing Actor with 3 inputs:
- Actor to be tested
- test function containing for example Jest unit test over the output
- input for the Actor

and the testing Actor would call the given Actor with a given output and in the end execute tests if the results are correct.
Similarly you could have a `runId` on input but maybe there is no good usecase.


TODO JC: Not sure how `actor` and `actorRun` are supposed to work? For example, if `actor`
is a reference to other Actor to be called, why not use webhook?
And how about `actorRun` ???




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

Note that the Actor's default dataset cannot be used as input, as it doesn't exist before the 
Actor is started. That's quite logical. But it also means that if the Actor wants
the default dataset to be set certain schema, this needs to be done in Output schema.

## TODOs
- This file should be a complete reference for the input schema...
- We should properly reconsider our current schema format.
  For example, the way we write string enum is suboptimal as the user has to separately
  name keys and values instead of a simple map that is error-prone. (JC: Yes please!)
- Also, e.g. change "editor: requesltListSoruces " to type: requesltListSoruces ... let's do this
