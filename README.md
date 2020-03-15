# Apify Actors specification proposal (WIP)

This is a work-in-progress document that contains
specification for Apify actors.
Note that some of the functionality is already implemented and available,
but some features or integrations not. This is not a documentation, 
it's rather a lighthouse where we want to get. 
Once we get there, this document will turn into a documentation.

## Table of Contents

<!-- toc -->

- [Introduction](#introduction)
- [Philosophy](#philosophy)
  * [UNIX program vs. Apify actor](#unix-program-vs-apify-actor)
- [Setup](#setup)
- [Programming interface](#programming-interface)
  * [Get input](#get-input)
  * [Set actor output](#set-actor-output)
  * [Main function](#main-function)
  * [Push data to dataset](#push-data-to-dataset)
  * [Exit an actor](#exit-an-actor)
  * [Abort an actor](#abort-an-actor)
  * [Update running actor status](#update-running-actor-status)
  * [Run an actor](#run-an-actor)
- [Metamorph](#metamorph)
- [Attach webhook to an actor run](#attach-webhook-to-an-actor-run)
  * [Pipe result of and actor to another](#pipe-result-of-and-actor-to-another)
  * [Read environment variables](#read-environment-variables)
  * [Watch system events](#watch-system-events)
  * [Get memory information](#get-memory-information)
  * [Key-value store](#key-value-store)
  * [Actor specification file (`actor.json`)](#actor-specification-file-actorjson)
  * [Documentation (`README.md`)](#documentation-readmemd)
- [Development](#development)
- [Sharing & Community](#sharing--community)
  * [User profile page](#user-profile-page)
  * [Shared actors](#shared-actors)

<!-- tocstop -->

## Introduction

Actors are serverless programs running in the cloud.
They can run as short or as long as necessary, even forever.
The actor can perform anything from a simple action such as filling
out a web form or sending an email, to complex operations such as crawling an entire website or removing duplicates from a large dataset.

Note that Actors are only loosely related to [Actor model](https://en.wikipedia.org/wiki/Actor_model) from computer science.
There are many differences.

## Philosophy

Actors are inspired by the **UNIX philosophy**:

1) Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new "features".

2) Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information.
Avoid stringently columnar or binary input formats. Don't insist on interactive input.

3) Design and build software, even operating systems, to be tried early, ideally within weeks.
Don't hesitate to throw away the clumsy parts and rebuild them.

4) Use tools in preference to unskilled help to lighten a programming task,
even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.

Actors are programs running in Docker containers in the cloud.
They take input, perform an action and generate an output.
Good ones have a documentation.
Each actor should do just one thing and do it well.
For complicated scenarios, combine more actors rather then building a large monolith.

### UNIX program vs. Apify actor

TODO: Add links here

| Program  | Actor |
|---|---|
| command-line options | input object |
| read stdin | read from dataset |
| write to stdout | push data to dataset, update actor status |
| write to stderr | set exit message |
| program exit code | actor exit code |
| file system | key-value store |

## Setup

You can start using actors
in [Apify console](https://my.apify.com/actors) without installing any local client.

**Node.js**

```
$ npm install apify
```

Use in JavaScript source files:

```js
import { Actor } from 'apify';
// OR? import Actor from 'apify-actor';
````

**CLI**
```
$ sudo npm install -g apify-cli
$ apify --version
```

**Slack**

TODO: Finish this

**API**
```
// https://api.apify.com/v2/key-value-stores/jancurn/test/records/OUTPUT
// https://api.apify.com/v2/actor-runs/ABCDEF/dataset -- this is better, can be accessed only via ID
// https://api.apify.com/v2/actor-runs/ABCDEF/key-value-store/records/OUTPUT
// https://api.apify.com/v2/key-value-stores/jancurn/test/OUTPUT.json
```

## Programming interface


### Get input

Get actor input in JSON format.

**UNIX equivalent**
```
$ command --option1=aaa --option2=bbb
int main (int argc, char *argv[])
```

**CLI**
```
# Emits JSON, but perhaps we could add some parsing helpers...
$ apify actor:get-input
> { "option1": "aaa", "option2": "bbb" }
```

**Node.js**
```js
const input = await Actor.getInput();
console.log(input.option1);
```

### Set actor output

`Actor.setOutput()` is like `Actor.setValue('OUTPUT')`,
but also checks that output conforms the schema defined in `actor.json`.
```js
await Actor.setOutput({
    flatResultsUrl: Actor.openDataset().getPublicUrl({
        clean: true,
        fields: 'url,results',
        unwind: 'url',
    }),
    allResultsUrl: Actor.openDataset().getPublicUrl({
        clean: true,
        fields: 'url,results',
    }),
});
```

### Main function

This is only helper.
TODO: Is this even needed? Perhaps just to call Apify.exit(1, 'Something failed'),
but that could be done by system (e.g. last line from stderr would go there or full).

**Node.js**
```js
Apify.main(async (input) => {
    // TODO: Really pass the input?
    // ...
});
```


### Push data to dataset

Save larger results to an append-only storage.

**UNIX equivalent**
```
$echo "Something" >> dataset.csv
```

**CLI**
```
# Text format
$ echo "someResult=123" | actor push-data
$ actor push-data someResult=123

# JSON format
$ echo '{ "someResult": 123 }' | actor push-data --json
$ actor push-data --json='{ "someResult": 123 }'
$ actor push-data --json=@result.json

# Push to a specific dataset
$ actor push-data --dataset=bob/election-data someResult=123
```

**Node.js**
```js
await Actor.pushData({
    someResult: 123,
});
```


### Exit an actor

**UNIX equivalent**
```
exit()
```

**CLI**
```
$ actor exit    # Success
$ actor exit 1
$ actor exit --message "Couldn't finish crawl" 1
```

**Node.js**
```js
// Apify.actor.abort() or Apify.Actor.abort() ?
Actor.exit(0, 'Succeeded, crawled 50 pages');
Actor.exit(1, `Couldn't finish crawl`);
await Actor.abort('RUN_ID');
// await Actor.kill('RUN_ID'); // TODO ?
```


### Abort an actor

**UNIX equivalent**
```
# Terminate a program
$ kill <pid>
```

**CLI**
```
$ apify actor:abort [RUN_ID]
# OR?
$ actor abort --token=123 [RUN_ID]
```

### Update running actor status

Periodically set a text-only status message to the running actor,
which is displayed to its users.

**CLI**
```
$ apify actor:update-status "Crawled 45 of 100 pages"
$ apify actor:update-status --run=[RUN_ID] --token=X "Crawled 45 of 100 pages"
```

**Node.js**
```js
await Actor.updateStatus('Crawled 45 of 100 pages');
await Actor.updateStatus('Crawled 45 of 100 pages', { runId: 123 });
```


### Run an actor

Apify NOTE: The system must enable overriding the default dataset, and e.g.
forwarding the data to another named dataset, that will be consumed by another actor.
Maybe the dataset should enable removal of records from beginning?

**UNIX equivalent**
```
# Run a program in the background
$ command <arg1>, <arg2>, … &

// Spawn another process
posix_spawn()
```

**CLI**
```
# On stdout, the commands emit actor output (in text or JSON format).
# TODO: Currently this doesn't work!
#  apify call --memory=1024 --build=beta apify/google-search-scraper
#   Error: ENOENT: no such file or directory, scandir 'apify_storage/key_value_stores/default'
# TODO: maybe keep "apify actor:call" or just "actor run" ?
$ apify actor:run apify/google-search-scraper queries='test\ntest2' countryCode='US'
$ apify actor:run --json apify/google-search-scraper '{ "queries": }'
$ apify actor:run --input=@data.json --json apify/google-search-scraper
$ apify actor:run --memory=1024 --build=beta apify/google-search-scraper
$ apify actor:run --output-record-key=SCREENSHOT apify/google-search-scraper

# Pass input from stdin
$ cat input.json | apify actor:run apify/google-search-scraper --json

# Call local actor during development
$ apify actor:run file:../some-dir someInput='xxx'

// Old TODOs:
// $ command <input.txt >my_output.txt 2>error_file
// $ actor call user/actor-name
// $ apify call user/actor-name | ???
```

**Slack**
```
apify run apify/google-search-scraper
```

**Node.js**
```
// Maybe Apify.runActor() ? that's more consistent with rest
const run = await Actor.call(
    'apify/google-search-scraper',
    { queries: 'test' },
    { memoryMbytes: 2048 },
);
console.log(`Received message: ${run.output.body.message}`);
// TODO: This would look better
// console.log(`Received message: ${run.output.results}`);

const run = await Actor.callTask(
    'jancurn/virtualrig-us-seo',
    { queries: 'test' },
    { memoryMbytes: 4096 },
);
```

**API**
```
[POST] https://api.apify.com/v2/actors/apify~google-search-scraper/run

[POST|GET] https://api.apify.com/v2/actors/apify~google-search-scraper/run-sync?
  token=rWLaYmvZeK55uatRrZib4xbZs&
  outputRecordKey=OUTPUT
  returnDataset=true
  Allow all dataset arguments: &format=json&clean=false&offset=0&limit=99&fields=myValue%2CmyOtherValue&omit=myValue%2CmyOtherValue&unwind=myValue&desc=true&attachment=true&delimiter=%3B&bom=false&xmlRoot=items&xmlRow=item&skipHeaderRow=true&skipHidden=false&skipEmpty=false&simplified=false&skipFailedPages=false
```


## Metamorph

Replace running actor's Docker image with another.
This is useful e.g. for repackaging an actor as a new actor
with its own settings and documentation.
Note that the originating actor can [set the output](#set-actor-output) before metamorphing.

**UNIX equivalent**
```
$ exec /bin/bash
```

**CLI**
```
$ apify actor:metamorph apify/web-scraper startUrls=http://example.com
$ apify actor:metamorph --input=@input.json --json --memory=4096 apify/web-scraper
```

**Node.js**
```js
// Or Apify.metamorphActor() or Apify.ActorMetamorph() ?
Actor.metamorph(
    'apify/web-scraper',
    { startUrls: [ "http://example.com" ] },
    { memoryMbytes: 4096 },
);

// TODO: Or maybe this way?
Actor.metamorph({
    actor: 'apify/web-scraper',
    input: {
        startUrls: []
    },
    options: {
        memoryMbytes: 4096,
    }
});
```

## Attach webhook to an actor run

Run another actor or an external HTTP API endpoint
after actor run finishes or fails.

**UNIX equivalent**
```
# Execute commands sequentially, based on their status
// $ command1; command2 (command separator)
// $ command1 && command2 ("andf" symbol)
// $ command1 || command2 ("orf" symbol)
```

**CLI**
```
apify add-webhook --actor-run-id=RUN_ID \\
  --event-types=SUCCEEDED,FAILED \\
  --request-url=https://api.example.com \\
  --payload-template='{ "test": 123" }'
actor add-webhook --event-types=SUCCEEDED \\
  --request-actor=apify/send-mail \\
  --memory=4096 --build=beta \\
  --payload-template=@template.json
```

**Node.js**
```js
// Or Apify.addWebhook() ?
await Actor.addWebhook({
    eventType: ['SUCCEEDED', 'FAILED'],
    // TODO: We don't have this now but we should, to enable adding webhooks to other runs
    attachToActorRunId: 'RUN_ID',
    requestUrl: 'http://api.example.com?something=123',
    payloadTemplate: `{
        "userId": {{userId}},
        "createdAt": {{createdAt}},
        "eventType": {{eventType}},
        "eventData": {{eventData}},
        "resource": {{resource}}
    }`
});

await Actor.addWebhook({
    eventType: ['SUCCEEDED', 'FAILED'],
    // Instead of requestUrl, we can call an actor. Internally, it's translated to requestUrl anyway.
    request: {
        actor: 'apify/send-email',
        options: {
            memoryMbytes: 512,
            token: null, // By default, using the Actor.addWebhook() caller's token
        },
        webhook: { }, // TODO: Recursively set other webhooks, to enable chaining
    },
    payloadTemplate: `{
        "to": "bob@example.com",
        "cc": {{user.email}},
        "html": "Hi there,<br><br>Here are Google Search results: {{resource.output.flatResults[format=html,limit=50]}}",
    }`,
    // TODO: Maybe in the future?
    payload: {
        body: 'xxxx',
        contentType: 'image/png'
    }
});
```

### Pipe result of and actor to another

**UNIX equivalent**
```
$ ls -l | grep "something" | wc -l
```

Apify has no direct equivalent, workaround is possible
- spin all 3 actors, and then pass messages between them.

Another option is having a new sotrage called Pipe - one actor would push from one side, second would consume,
it would only be launched on consmuption side (like SQS + Lambda)

```
// TODO: Support creating chains like this
// XXX:   actor call apify/google-search-scraper  => actor call apify/send-email queryTerms="aaa\nbbb"
// XXX:   actor call apify/web-scraper  => actor call lukaskrivka/upload-google-sheets sheeetId="abc"
```

### Read environment variables

**UNIX equivalent:**
```
$ echo $ACTOR_RUN_ID
```

Apify NOTE: These can be defined by actor owner during build,
but unlike traditional processes, they are not passed when calling another actor.
System passes various runtime info to actor using env vars.

See [Environment variables](#) in Actor documentation.

**CLI**
```
$ echo "$APIFY_ACTOR_RUN_ID started at $APIFY_ACTOR_RUN_STARTED_AT"
```

**Node.js**
```js
const env = await Actor.getEnv();
console.log(env.actorRunId);
```


### Watch system events

Receive system events e.g. CPU statistics of the running container
or information about imminent [migration to another server](#xxx).

**UNIX equivalent**

```
signal(SIGINT, handle_sigint);
```

**Node.js**
```js
Actor.events.on('cpuInfo', data => {
    if (data.isCpuOverloaded) console.log('Oh no, the CPU is overloaded!');
});
```

### Get memory information

Get information about the total and available memory
of the actor's container or local system.

**UNIX equivalent:**
```
# Print memory usage of programs
ps -a
```

**Node.js**
```js
const memoryInfo = await Apify.getMemoryInfo();
```

### Key-value store

**UNIX**
```
$ echo "hello world" > file.txt
$ cat file.txt
```

**Node.js**
```
await Actor.setValue('my-state', { something: 123 });
await Actor.setValue('screenshot', buffer, { contentType: 'image/png' });

const value = await Actor.getValue('my-state');
```

### Actor specification file (`actor.json`)

This is in `actor.json` file.
It combines legacy `apify.json`, `INPUT_SCHEMA.json` and adds output schema.

This file should be added to the source control, and links your project
with an Apify actor in the cloud.

```js
{
    "name": "bob/dataset-to-mysql",
    "version": "0.1",
    "buildTag": "latest",
    "env": {
        "MYSQL_USER": "my_username",
        "MYSQL_PASSWORD": "@mySecretPassword"
    },
    // TODO: Do we need this? "template": "basic",
    // Optional. If omitted, there is not input schema and checks.
    "input": {
        "description": "To update crawler to another site you need to change startUrls and pageFunction options!",
        // "type": "object",
        // "schemaVersion": 1,
        "properties": {
            "startUrls": {
                "title": "Start URLs",
                "type": "array",
                "description": "URLs to start with",
                "prefill": [
                    { "url": "http://example.com" },
                    { "url": "http://example.com/some-path" }
                ],
                "editor": "requestListSources"
            },
            "pageFunction": {
                "title": "Page function",
                "type": "string",
                "description": "Function executed for each request",
                "prefill": "async () => {\n  return $('title').text();\n\n}",
                "editor": "javascript"
            }
        },
        "required": ["startUrls", "pageFunction"]
    },
    // Optional. If omitted, there is no output schema.
    "output": {
        "properties": {
            "flatResultsUrl": {
                "title": "All organic results",
                "description": "Shows all organic Google Search results",
                "type": "string",
                // This says the app to render Dataset viewer for this info
                "viewer": "dataset"
            },
            "fullResultsUrl": {
                "title": "SERPs grouped by page",
                "type": "string",
                "viewer": "dataset",
                "groupCaption": "Advanced",
            },
        },
    },
};
```

### Documentation (`README.md`)

The README.md [Markdown](#vvv) file associated with the actor
is used as its documentation page. Good documentation makes good programmers!


## Development

High-level overview how to build new actors.

## Sharing & Community

### User profile page

For example:
```
https://apify.com/jancurn
```

To improve user and community engagement,
we should enable people to upload their custom cover photo
and long description in Markdown format (such as README.md) file.
The goal is to provide ability to 

For example, for our help with the COVID-19 pandemic,
we released a new page at https://apify.com/covid-19 with list
of relevant actors and datasets. Why not let people do the same? Anyone could create
a new team (e.g. called `covid-19`), change branding of the page a bit,
upload a Markdown with text content, and the system will automatically
show user's published actors, datasets and key-value stores.

On user account, there should be just one global setting
called `Make profile public` instead
of the current `Make profile picture publicly visible`

### Shared actors

For example:
```
https://apify.com/jancurn/some-scraper
```




