# Main `.actor` directory

Directory `./actor` must be placed at actor's top-level directory and contains the specification of the actor:
- Main properties such as name or description
- The input
- The output

The only required file is `.actor/ACTOR.json,` and all the other files are optional. In addition to `ACTOR.json`, most actors also implement `INPUT_SCHEMA.json`, `OUTPUT_SCHEMA.json`, and a couple of storage schemas.

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

- I'd make all the storage schemas "weak" (allowing more fields to be added) as for example some deduplication actor could require each dataset
  item to have a `uuid: 'string'` field but does not care about anything else. And similarly, for key-value stores - schema expects something
  to be there but does not care about other values.
- How to integrate output schema with `const { output } = await Apify.call(...)`?
