# Actor file specification

This JSON file must be present at `.actor/actor.json` and defines core properties of a single web Actor.

The file contains a single JSON object with the following properties:

```jsonc
{
  // Required field, indicates that this is an Actor definition file and the specific version of the Actor specification.
  "actorSpecification": 1,
  
  // Required "technical" name of the Actor, must be a DNS hostname-friendly text.
  "name": "google-search-scraper",

  // Human-friendly name and description of the Actor.
  "title": "Google Search Scraper",
  "description": "A 200-char description",

  // Required, indicates the version of the Actor. Since actor.json file is commited to Git, you can have different Actor
  // versions in different branches.
  "version": "0.0",

  // Optional tag that is applied to the builds of this Actor. If omitted, it defaults to "latest".
  "buildTag": "latest",
  
  // An optional object with environment variables expected by the Actor.
  // Secret values are prefixed by @ and their actual values need to be registered with the CLI, for example:
  // $ apify secrets add mySecretPassword pwd1234
  "environmentVariables": {
    "MYSQL_USER": "my_username",
    "MYSQL_PASSWORD": "@mySecretPassword"
  },
  
  // Optional field. If true, the Actor indicates it can be run in the Standby mode,
  // to get started and be kept alive by the system to handle incoming HTTP REST requests by the Actor's web server.
  "usesStandbyMode": true,
 
  // An optional metadata object enabling implementations to pass arbitrary additional properties.
  // The property values can be arbitrary objects.
  "meta": {
    "something": "bla bla",
    "somethingElse": {
      "subObject": "works"
    }
  },

  // Optional minimum and maximum memory for running the Actor.
  "minMemoryMbytes": 128,
  "maxMemoryMbytes": 4096,

  // When user doesn't specify memory when starting an Actor run, the system will use this amount.
  // The goal of this feature is to optimize user experience vs. compute costs.
  // The value might reference properties of the Actor run object (e.g. `{{actorRun.options.maxTotalChargeUsd}}`)
  // or Actor input (e.g. `{{actorRun.input}}`), similar to Output schema. It can also use basic arithmetic expressions.
  // The value will be clamped between `minMemoryMbytes` and `maxMemoryMbytes` (if provided), and rounded up to the nearest higher power of 2.
  // If the variable is undefined or empty, the behavior is undefined and the system will select memory arbitrarily.
  // In the future, we might change this behavior.
  "defaultMemoryMbytes": "{{actorRun.input.maxParallelRequests}} * 256 + 128",
  
  // Optional link to the Actor Dockerfile.
  // If omitted, the system looks for "./Dockerfile" or "../Dockerfile"
  "dockerfile": "./Dockerfile",
  
  // Optional link to the Actor README file in Markdown format.
  // If omitted, the system looks for "./ACTOR.md" and "../README.md"
  "readme": "./README.md",

  // Optional link to the Actor changelog file in Markdown format.
  "changelog": "../../../shared/CHANGELOG.md",
  
  // Optional link to Actor input or output schema file, or inlined schema object,
  // which is a JSON schema with our extensions. For details see ./INPUT_SCHEMA.md or ./OUTPUT_SCHEMA.md, respectively.
  // BACKWARDS COMPATIBILITY: "inputSchema" used to be called "input", all implementations should support this.
  "inputSchema": "./input_schema.json",
  "outputSchema": "./output_schema.json",
  
  // Optional path to Dataset or Key-value Store schema file or inlined schema object for the Actor's default dataset or key-value store. 
  // For detail, see ./DATASET_SCHEMA.md or ./KEY_VALUE_STORE_SCHEMA.md, respectively.
  // BACKWARDS COMPATIBILITY: "datasetSchema" used to be "storages.keyValueStore" sub-object, all implementations should support this.
  "datasetSchema": "../shared_schemas/generic_dataset_schema.json",
  "keyValueStoreSchema": "./key_value_store_schema.json",
   
  // Optional path or inlined schema object of the Actor's web server in OpenAPI format.
  "webServerSchema": "./web_server_openapi.json",
  
  // Optional URL path and query parameters to the Model Context Protocol (MCP) server exposed by the Actor web server.
  // If present, the system knows the Actor provides an MCP server, which can be used by the platform
  // and integrations to integrate the Actor with various AI/LLM systems.
  "webServerMcpPath": "/mcp?version=2",

  // Scripts can be used by tools like the CLI to do certain actions based on the commands you run.
  // The presence of this object in your Actor config is optional, but we recommend always defining at least the `run` key.
  "scripts": {
    // The `run` script is special - it defines *the* way to run your Actor locally. While tools can decide
    // to implement mechanisms to detect what type of project your Actor is, and how to run it, you can choose to
    // define this as the source of truth.
    //
    // This should be the same command you run as if you were at the root of your Actor when you start it locally.
    // This can be anything from an npm script, as shown below, to a full chain of commands (ex.: `cargo test && cargo run --release`).
    //
    // CLIs may opt to also request this command when initializing a new Actor, or to automatically migrate and add it in the first time
    // you start the Actor locally.
    "run": "npm start"
  }
}
```

## Notes

- The `name` doesn't contain the developer username, so that the Actor can be easily deployed
  to any user account. This is useful for tutorials and examples, as well as
  pull requests done externally to create Actors from existing source code files
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
- When calling `actor push` and the `title` or `description` are already set
  on the Actor (maybe SEO-optimized versions from copywriter),
  by default we do not overwrite them
  unless `apify push` is called with options `--force-title` or `--force-description`.

## Changes from the legacy `apify.json` file

The `.actor/actor.json` replaces the legacy `apify.json` file. Here are main changes from the previous version:

- We removed the `template` property as it's not needed for anything, it only stored the original template
- There's a new `title` field for a human-readable name of the Actor.
  We're moving towards having human-readable names shown for Actors everywhere,
  so it makes sense to define `title` directly in the source code.
- Similarly, we added `description` for the short description of what the Actor does.
- `env` was renamed to `environmentVariables` for more clarity. `apify build` or `apify run`
  could have an option `--apply-env-vars-to-build` like we have it on platform.
- The `dockerfile` and `readme` directives are optional, the system falls back to reasonable
  defaults, first in `.actor` directory and then in the top-level directory.
- `scripts` section was added
