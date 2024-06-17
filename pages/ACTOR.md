# Actor File

This JSON file must be present at `.actor/actor.json` and contains the main definition of the Actor.

It looks as follows:

```jsonc
{
  "actorSpecification": 2, // required
  "name": "google-search-scraper",
  "title": "Google Search Scraper",
  "description": "The 200-char description",
  "version": "0.0", // required
  "buildTag": "latest", // if omitted, builds with "latest" tag
  "environmentVariables": {
    "MYSQL_USER": "my_username",
    "MYSQL_PASSWORD": "@mySecretPassword"
  },
  "dockerfile": "./Dockerfile", // if omitted, it checks "./Dockerfile" and "../Dockerfile"
  "readme": "./ACTOR.md", // if omitted, it checks "./ACTOR.md" and "../README.md"
  "input": "./input_schema.json",
  "output": "./output_schema.json",
  "minMemoryMbytes": 128, // optional number, min memory in megabytes allowed for running this Actor
  "maxMemoryMbytes": 4096, // optional number, max memory in megabytes allowed for running this Actor
  "storages": {
    "keyValueStore": "./key_value_store_schema.json",
    "dataset": "../shared-schemas/dataset_schema.json",
    "requestQueue": "./request_queue_schema.json"
  }
}
```

The `.actor/actor.json` replaces the legacy `apify.json` file.
Here are the notes comparing the format to the previous version:

- We removed the `template` property as it's not needed for anything, it only stored the original template
- There's a new `title` field for a human-readable name of the Actor.
  We're moving towards having human-readable names shown for actors everywhere,
  so it makes sense to define `title` directly in the source code.
- Similarly, we added `description` for the short description of what the Actor does.
- When calling `actor push` and the `title` or `description` are already set
  on the Actor (maybe SEO-optimized versions from copywriter),
  by default we do not overwrite them
  unless `apify push` is called with options `--force-title` or `--force-description`.
- The `name` doesn't contain username, so that the Actor can be easily deployed
  to any user account. This is useful for tutorials and examples, as well as
  pull requests done externally to create actors from existing source code files
  owned by external developers
  (the developer might not have Apify account yet, and we might want to show them deployment
  to some testing account).
  Note that `apify push` has option `--target=eva/my-actor:0.0` that allows
  deployment of the Actor under a different user account, using permissions
  and personal API token of the current user.
  We should also add options to override only parts of this, 
  like `--target-user` (ID or username), `--name`, `--build-tag` and `--version`,
  it would be useful e.g. in CI for beta versions etc.
- Note that `version` and `buildTag` are shared across Actor deployments to
  all user accounts, similarly as with software libraries,
  and hence they are part of `actor.json`.
- The `dockerfile` property points to a Dockerfile that is to be used to build the
  Actor image. If not present, the system looks for Dockerfile in the `.actor` directory
  and if not found, then in Actor's top-level
  directory. This setting is useful if the source code repository has some
  other Dockerfile in the top-level directory, to separate Actor Docker image from the
  other one. Note that paths in Dockerfile are ALWAYS relative to the Dockerfile's location.
  When calling `apify run`, the system runs the Actor using the Dockerfile.
- `env` was renamed to `environmentVariables` for more clarity. `apify build` or `apify run`
  could have an option `--apply-env-vars-to-build` like we have it on platform.
- The `dockerfile` and `readme` directives are optional, the system falls back to reasonable
  defaults, first in `.actor` directory and then in the top-level directory.

TODOs (@jancurn):
- The above text needs reformatting, make it more like a reference


- Add "scripts" section, see https://apifier.slack.com/archives/C04HB9V90DT/p1672826248186569 
