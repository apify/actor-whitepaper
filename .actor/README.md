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

## Storage schema referencing

In both `INPUT_SCHEMA.json` and `OUTPUT_SCHEMA.json` you can reference storage schemas. There are 3 ways how to reference a schema:
- Local file: `./MY_DATASET_SCHEMA.json`
- Schema of existing dataset: `dataset:mtrunkat/my-datasey` or `dataset:jkq3Smioe54dcqp4b`
- Dataset from output or input schema of an actor: `actor:mtrunkat/my-actor/output.defaultDataset` or certain build `actor:mtrunkat/my-actor@1.2.4/input.adsDataset`

The prefixes such as `dataset:` are not nice but unfortunately we don't have names unique actors all user resources.

## Other notes

- I'd make all the storage schemas "weak" (allowing more fields to be added) as for example some deduplication actor could require each dataset
  item to have a `uuid: 'string'` field but does not care about anything else. And similarly, for key-value stores - schema expects something
  to be there but does not care about other values.
- How to integrate output schema with `const { output } = await Apify.call(...)`?
