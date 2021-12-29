# Main `.ACTOR` directory

Directory `./actor` must be placed at actor's top-level directory and contains the specification of the actor:
- Main properties such as name or description
- The input
- The output

The only required file is `.ACTOR/actor.json,` and all the other files are optional. In addition to `ACTOR.json`, most actors also implement `INPUT_SCHEMA.json`, `OUTPUT_SCHEMA.json`, and a couple of storage schemas.

For file specifying actor iself, see:
- [ACTOR.json](./ACTOR.md)
- [INPUT_SCHEMA.json](./INPUT_SCHEMA.md)
- [OUTPUT_SCHEMA.json](./OUTPUT_SCHEMA.md)

And for storage schemas see:
- [DATASET_SCHEMA.json](./DATASET_SCHEMA.md)
- [KEY_VALUE_STORE_SCHEMA.json](./KEY_VALUE_STORE_SCHEMA.md)
- [REQUEST_QUEUE_SCHEMA.json](./REQUEST_QUEUE_SCHEMA.md)

One common attribute for each of these files is `formatVersion`, which allows making format changes without breaking older code.

## Other notes

- All the storage schemas are "weak" (allowing more fields to be added) as for example some deduplication actor could require each dataset
  item to have a `uuid: 'string'` field but does not care about anything else. And similarly, for key-value stores - schema expects something
  to be there but does not care about other values.
- How to integrate output schema with `const { output } = await Apify.call(...)`?
    - @jancurn: 

    > Same as we show Output in UI, we need to autogenerate the OUTPUT in API e.g. JSON format. There would be properties like in the output_schema.json file, with e.g. URL to dataset, log file, kv-store, live view etc. So it would be an auto-generated field "output" that we can add to JSON returned by the Run API enpoints (e.g. https://docs.apify.com/api/v2#/reference/actor-tasks/run-collection/run-task)
    - Also see: https://github.com/apify/actor-specs/pull/5#discussion_r775641112
    - `output` will be a property of run object generated from `OUTPUT_SCHEMA.json`
