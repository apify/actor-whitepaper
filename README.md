# Apify Actors Specification (WIP)

Written by: [Jan Čurn](https://apify.com/jancurn), [Marek Trunkát](https://apify.com/mtrunkat), [Ondra Urban](https://apify.com/mnmkng)

December 2021

This is a work-in-progress document that contains the specification for Apify actors.
Note that some of the functionality is already implemented and available,
but some features or integrations not.
This is not documentation, it’s rather a lighthouse where we want to get over time.
Once we get there, this document will turn into documentation.

## Table of Contents

<!-- toc -->

- [Introduction](#introduction)
- [Philosophy](#philosophy)
  * [UNIX program vs. Apify actor](#unix-program-vs-apify-actor)
- [Installation and setup](#installation-and-setup)
  * [Node.js](#nodejs)
  * [Python](#python)
  * [Command-line interface (CLI)](#command-line-interface-cli)
  * [Slack](#slack)
- [Programming interface](#programming-interface)
  * [Get input](#get-input)
  * [Main function](#main-function)
  * [Push results to dataset](#push-results-to-dataset)
  * [Exit actor](#exit-actor)
  * [Aborting other actor](#aborting-other-actor)
  * [Update actor status](#update-actor-status)
  * [Start an actor (without waiting for finish)](#start-an-actor-without-waiting-for-finish)
  * [Metamorph](#metamorph)
  * [Attach webhook to an actor run](#attach-webhook-to-an-actor-run)
  * [Pipe result of an actor to another (aka chaining)](#pipe-result-of-an-actor-to-another-aka-chaining)
  * [Read environment variables](#read-environment-variables)
  * [Watch system events](#watch-system-events)
  * [Get memory information](#get-memory-information)
  * [Key-value store (aka File store)](#key-value-store-aka-file-store)
  * [Actor specification file (`actor.json`)](#actor-specification-file-actorjson)
  * [Documentation (`README.md`)](#documentation-readmemd)
- [Development](#development)
  * [Local debugging](#local-debugging)
  * [On Apify platform](#on-apify-platform)
- [Sharing & Community](#sharing--community)
  * [User profile page](#user-profile-page)
  * [Shared actors](#shared-actors)
- [TODOs](#todos)

<!-- tocstop -->

## Introduction

Actors are serverless programs running in the cloud.
They can run as short or as long as necessary, even forever.
The actor can perform anything from a simple action such as
filling out a web form or sending an email, to complex operations such as crawling an entire website or removing duplicates from a large dataset.

Basically, actors are Docker containers with a documentation in README.md, input and output schema. nice user interface.

Note that actors are only loosely related to the [Actor model](https://en.wikipedia.org/wiki/Actor_model) from computer science. There are many differences.

## Philosophy

Actors are inspired by the **[UNIX philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)**:

1. **Make each program do one thing well**. To do a new job, build afresh rather than complicate old programs by adding new “features”.
2. Expect the **output of every program to become the input to another**, as yet unknown, program. Don’t clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don’t insist on interactive input.
3. Design and build software, even operating systems, to be **tried early**, ideally within weeks. Don’t hesitate to throw away the clumsy parts and rebuild them.
4. **Use tools in preference to unskilled help** to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you’ve finished using them.

Actors are programs running in Docker containers in the cloud. They take input, perform an action and generate an output. Good ones have documentation. Each actor should do just one thing and do it well. For complicated scenarios, combine more actors rather than building a large monolith.

### UNIX program vs. Apify actor

TODO: Add links to the texts in table

------
command-line options |	input object
read stdin |	read from dataset
write to stdout	| push data to dataset, update actor status
write to stderr	| set exit message
program exit code | 	actor exit code
file system	| key-value store
--------

## Installation and setup

You can start using actors in [Apify Console](https://console.apify.com/actors) without installing any local client.

Below are steps to install Apify libraries and start using actors locally on your machine, in various languages and environemnts.

### Node.js

```
$ npm install apify
```

### Python

```python
pip3 install apify
```

```python
from apify import actor 
```

### Command-line interface (CLI)

```
$ sudo npm install -g apify-cli
$ apify --version
```

### Slack

Install Apify app for Slack.

## Programming interface

The following commands are expected to be called from within the actor's Docker container, either on Apify platform or the local environment.

### Get input

Get access to the actor input object passed by the user.
It is parsed from a JSON file, stored in the actor's default key-value store (usually called `INPUT`).

#### Node.js

```jsx
import { Actor } from 'apify';

// Ondra's razor: We should instantiate new object,
//  to avoid require-time side-effects

const input = await Actor.getInput();
console.log(input.option1);

// prints: { "option1": "aaa", "option2": 456 }
```

#### Python

```python
from apify import actor

input = actor.get_input()
print(input)
```

#### CLI

```
# Emits a JSON object, which can be parsed using "jq" tool

apify actor get-input | jq

> { "option1": "aaa", "option2": 456 }
```

#### UNIX equivalent

```
$ command --option1=aaa --option2=bbb
int main (int argc, char *argv[])
```

### Main function

This is an optional helper to wrap the body of the actor.

**TODO**: Is this even needed? **PROBABLY NOT** Perhaps just to call `Actor.exit(1, ‘Something failed’)`, but that could be done by the system (e.g. the last line from stderr would go there or full). Let's see...
How else would we initialize web server to listen for events? Maybe some "subscribe" function?**
Advantage of `main()` function: Kills actor even if you forgot `setTimeout()`

#### Node.js

```jsx
import { Actor } from 'apify';

Actor.main(async () => {
  const input = await Actor.getInput();
  // ...
});
```

#### UNIX equivalent

```jsx
int main (int argc, char *argv[]) {
  ...
}
```

### Push results to dataset

Save larger results to append-only storage called [Dataset](https://sdk.apify.com/docs/api/dataset).
When an actor starts, by default it is associated with a newly-created empty dataset.
The user can override when running the actor.

#### Node.js

```jsx
await Actor.pushData({
    someResult: 123,
});

const dataset = await Apify.openDataset('bob/poll-results-2019');
await dataset.pushData({ someResult: 123 });
```

#### Python

```python
await actor.push_data({ some_result=123 })
```

#### CLI

```bash
# Text format
$ echo "someResult=123" | apify actor push-data
$ apify actor push-data someResult=123

# JSON format
$ echo '{ "someResult": 123 }' | actor push-data --json
$ apify actor push-data --json='{ "someResult": 123 }'
$ apify actor push-data --json=@result.json

# Push to a specific dataset in the cloud
$ apify actor push-data --dataset=bob/election-data someResult=123

# Push to dataset on local system
$ apify actor push-data --dataset=./my_dataset someResult=123
```

#### UNIX equivalent

```
$echo "Something" >> dataset.csv
```

### Exit actor

Terminate the actor and tell users what happened.

#### Node.js

```jsx
await Actor.exit(0, 'Succeeded, crawled 50 pages');
await Actor.exit(1, `Couldn't finish the crawl`);
```

#### Python

```python
await actor.exit(0, 'Generated 14 screenshots')
```

#### CLI

```bash
# Success
$ apify actor exit
$ apify actor exit --message "Email sent"

# Actor failed 
$ apify actor exit --code=1 --message "Couldn't fetch the URL"
```


#### UNIX equivalent

```c
exit(1)
```

### Aborting other actor

Abort itself or other running actor on the Apify platform, setting it to `ABORTED` state. 

#### Node.js

```jsx
await Actor.abort({ message: 'Job was done,', runId: 'RUN_ID' });
```

#### CLI

```bash
$ apify actor abort --run=[RUN_ID] --token=123 
```


#### UNIX equivalent

```
# Terminate a program
$ kill <pid>
```

### Update actor status

Periodically set a text-only status message to the currently running actor, to tell users what is it doing.

#### CLI

```bash
$ apify actor set-status-message "Crawled 45 of 100 pages"
$ apify actor set-status-message --run=[RUN_ID] --token=X "Crawled 45 of 100 pages"
```

#### Node.js

```jsx
await Actor.setStatusMessage('Crawled 45 of 100 pages');

// Setting status message to other actor externally is also possible
await Actor.setStatusMessage('Everyone is well', { runId: 123 });
```

### Start an actor (without waiting for finish)

Apify NOTE: The system must enable overriding the default dataset,
and e.g. forwarding the data to another named dataset,
that will be consumed by another actor.
Maybe the dataset should enable removal of records from beginning? Currently, actors need to implement it themselves.

**TODO:** We should have consistent naming, “call” is bit confusing, “run” is what it si. But will that work together with “apify run” that runs locally? In the new client we have "start"

**TODO:** Enable overriding of dataset to use by the actor? Perhaps it’s enough to have an utility actor (e.g. `apify/publish-dataset`), you will webhook it to actor run, and on finish, it will take the default dataset, publish it and atomically rename it (e.g. `jancurn/london-denstists`). But this way we’d lose all dataset settings (e.g. permissions, name, description), maybe Datasets should have an operation “swap” that would enable atomic replace of dataset data while keeping its ID and settings.

**UNIX equivalent**

```
# Run a program in the background
$ command <arg1>, <arg2>, … &

// Spawn another process
posix_spawn()
```

**CLI**

```
# On stdout, the commands emit actor run object (in text or JSON format),
# we shouldn't wait for finish, for that it should be e.g. "execute"
# TODO: Currently this doesn't work!
#  apify call --memory=1024 --build=beta apify/google-search-scraper
#   Error: ENOENT: no such file or directory, scandir 'apify_storage/key_value_stores/default'
# TODO: maybe keep "apify actor:call" or just "actor run" ?

$ apify actor:start apify/google-search-scraper queries='test\ntest2' \
  countryCode='US'
$ apify actor:start --json apify/google-search-scraper '{ "queries": }'
$ apify actor:start --input=@data.json --json apify/google-search-scraper
$ apify actor:start --memory=1024m --build=beta apify/google-search-scraper
$ apify actor:start --output-record-key=SCREENSHOT apify/google-search-scraper

# Pass input from stdin
$ cat input.json | apify actor:start apify/google-search-scraper --json

# Call local actor during development
$ apify actor:start file:../some-dir someInput='xxx'

// Old TODOs:
// $ command <input.txt >my_output.txt 2>error_file
// $ actor call user/actor-name
// $ apify call user/actor-name | ???
```

**Slack**

```
NOTE: In Slack it just starts the actor, and then prints the message to channel,
any time later
/apify start apify/google-search-scraper startUrl=afff
```

**Node.js**

```
// Maybe Apify.runActor() ? that's more consistent with rest
// TODO: Actor should be for self, this is more like API client thing
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

### Metamorph

Replace running actor’s Docker image with another. This is useful e.g. for repackaging an actor as a new actor with its own settings and documentation. Note that the originating actor can [set the output](about:blank#set-actor-output) before metamorphing.

**UNIX equivalent**

```
$ exec /bin/bash
```

**CLI**

```
$ apify actor metamorph apify/web-scraper startUrls=http://example.com
$ apify actor metamorph --input=@input.json --json --memory=4096 \
  apify/web-scraper
```

**Node.js**

```
// Or Apify.metamorphActor() or Apify.ActorMetamorph() ?
await Actor.metamorph(
    'apify/web-scraper',
    { startUrls: [ "http://example.com" ] },
    { memoryMbytes: 4096 },
);

// TODO: Or maybe this way?
await Actor.metamorph({
    actor: 'apify/web-scraper',
    input: {
        startUrls: []
    },
    options: {
        memoryMbytes: 4096,
    }
});
```

### Attach webhook to an actor run

Run another actor or an external HTTP API endpoint after actor run finishes or fails.

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

apify add-webhook --event-types=SUCCEEDED \\
  --request-actor=apify/send-mail \\
  --memory=4096 --build=beta \\
  --payload-template=@template.json

# Or maybe have a simpler API for self-actor?
apify actor:add-webhook --event-types=SUCCEEDED --request-actor=apify/send-mail 
```

**Node.js**

```
// Or Apify.addWebhook() ?
await Actor.addWebhook({
    eventType: ['SUCCEEDED', 'FAILED'],
    // TODO: We don't have this now but we should,
    // to enable adding webhooks to other runs
    attachToActorRunId: 'RUN_ID',
    requestUrl: 'http://api.example.com?something=123',
    payloadTemplate: `{
        "userId": {{userId}},
        "createdAt": {{createdAt}},
        "eventType": {{eventType}},
        "eventData": {{eventData}},
        "resource": {{resource}}
    }`});

await Actor.addWebhook({
    eventType: ['SUCCEEDED', 'FAILED'],
    // Instead of requestUrl, we can call an actor.
    // Internally, it's translated to requestUrl anyway.
    request: {
        actor: 'apify/send-email',
        options: {
            memoryMbytes: 512,
            token: null, // By default, using the Actor.addWebhook() 
              // caller's token        },        webhook: { }, // TODO: Recursively set other webhooks, to enable chaining    },    payloadTemplate: `{        "to": "bob@example.com",        "cc": {{user.email}},        "html": "Hi there,<br><br>Here are Google Search results: {{resource.output.flatResults[format=html,limit=50]}}",    }`,    // TODO: Maybe in the future?    payload: {        body: 'xxxx',        contentType: 'image/png'    }});
```

### Pipe result of an actor to another (aka chaining)

**UNIX equivalent**

```
$ ls -l | grep "something" | wc -l
```

Apify has no direct equivalent, workaround is possible - spin all 3 actors, and then pass messages between them.

Another option is having a new storage called Pipe - one actor would push from one side, second would consume, it would only be launched on consumption side (like SQS + Lambda)

NOTE: Probably it doesn't make sense to support the co-running actors in parallel, it would be too inefficient.

```
// TODO: Support creating chains like this
// XXX:   actor call apify/google-search-scraper
  => actor call apify/send-email queryTerms="aaa\nbbb"
// XXX:   actor call apify/web-scraper
  => actor call lukaskrivka/upload-google-sheets sheeetId="abc"
```

### Read environment variables

**UNIX equivalent:**

```
$ echo $ACTOR_RUN_ID
```

Apify NOTE: These can be defined by actor owner during build, but unlike traditional processes, they are not passed when calling another actor. System passes various runtime info to actor using env vars.

See [Environment variables](about:blank#) in Actor documentation.

**CLI**

```
$ echo "$APIFY_ACTOR_RUN_ID started at $APIFY_ACTOR_RUN_STARTED_AT"
```

**Node.js**

```
// TODO: Maybe we don't need this, use process.env
const env = await Actor.getEnv();
console.log(env.actorRunId);
```

### Watch system events

Receive system events e.g. CPU statistics of the running container or information about imminent [migration to another server](about:blank#xxx).

Perhaps we could add custom events in the future.

**UNIX equivalent**

```
signal(SIGINT, handle_sigint);
```

**Node.js**

```
Actor.events.on('cpuInfo', data => {
    if (data.isCpuOverloaded) console.log('Oh no, the CPU is overloaded!');
});
```

### Get memory information

Get information about the total and available memory of the actor’s container or local system.

**UNIX equivalent:**

```
# Print memory usage of programs
ps -a
```

**Node.js**

```
const memoryInfo = await Apify.getMemoryInfo();
```

### Key-value store (aka File store)

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

This is in `actor.json` file. It combines legacy `apify.json`, `INPUT_SCHEMA.json` and adds output schema.

**TODO**: The biggest question here is whether we should apply description, name and options from `actor.json` file and how (e.g. this is how NPM does it) or rather let people to update these things only manually (e.g. GitHub repo description or Docker Hub image info). The latter usually leads to outdated info, but e.g. allows admins to easily update things without access to source code and necessity to rebuild the actor.

**TODO**: Some (most) people argue that having one long JSON file is hell to edit. An option is to use directory (e.g. `/.actor`) that could contains several JSON files, e.g. INPUT_SCHEMA.json, OUTPUT_SCHEMA.json and ACTOR.json)... Let's discuss

**TODO**: Consider how it will work with metamorph, the second actor can set output. Mara says workflows and actor connections can replace metamorph in many cases

**NOTE**: Devs should only call setOutput once, and we need to be able to show something to users right after start of actor before actor starts and setOutput has a chance to run, hence calling setOutput in loop doesn't make sense, plus it's slow. The output schema needs to provide info how to render output right away, basically pre-generate OUTPUT on the fly. The dev might not even need to call setOutput, and we generate it ourselves from output schema.

This file should be added to the source control, and links your project with an Apify actor in the cloud.

```jsx
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
								"datasetViewParams": {
                  "unwind": ...
                  "defaultDataset",
								}
                // This says the app to render Dataset viewer for this info
                "viewer": "dataset"
            },
            "fullResultsUrl": {
                "title": "SERPs grouped by page",
                "type": "string",
                "viewer": "dataset",
                "groupCaption": "Advanced",
            },
						"screenshotUrl": {
							  "xxx": "{DEFAULT_KEY_VALUE_STORE}/screenshot.png"
								
						}
        },
    },
};
```

OUTPUT schema

```jsx
{     
   
    "products": {
      mainView: true,
      "title": "Foudn product",
      "type": "Dataset",

	    "datasetSchema": {
	        // dataset field
	        "price": {
	           "_type": "number|null",
	           "amount": {},
	           "currency": {}, 
	        },
	        "productSummary": {
						
	        } 
	
	        "url": { },
	
	         // "files":
	     }
     },

"status": {
   mainView: true,
   title: "View status of crawler",
   type: "liveview",
   

},

"files": {
}
	
"LiveView"
  
 
        "flatResultsUrl": {
            "title": "All organic results",
            "description": "Shows all organic Google Search results",
            "type": "dataset",
            "fields": {
              "price": "number",
              "...": ...
            ],
						"datasetViewParams": {
              "unwind": ...
              "defaultDataset",
						}
            // This says the app to render Dataset viewer for this info
            "viewer": "dataset"
        },
        "fullResultsUrl": {
            "title": "SERPs grouped by page",
            "type": "string",
            "viewer": "dataset",
            "groupCaption": "Advanced",
        },
				"screenshotUrl": {
					  "xxx": "{DEFAULT_KEY_VALUE_STORE}/screenshot.png"
						
				}
    },
};
```

### Documentation (`README.md`)

The README.md [Markdown](about:blank#vvv) file associated with the actor is used as its documentation page. Good documentation makes good programmers!

## Development

High-level overview how to build new actors.

### Local debugging

Actors can be developed and run locally. To support running other actors, we need to define mapping
of `username/actor` to local directories with `.actor` sub-directory.

TODO: Maybe using environment variable with the mapping?

### On Apify platform

....

## Sharing & Community

### User profile page

For example:

```
https://apify.com/jancurn
```

To improve user and community engagement, we should enable people to upload their custom cover photo and long description in Markdown format (such as README.md) file. The goal is to provide ability to

For example, for our help with the COVID-19 pandemic, we released a new page at https://apify.com/covid-19 with list of relevant actors and datasets. Why not let people do the same? Anyone could create a new team (e.g. called `covid-19`), change branding of the page a bit, upload a Markdown with text content, and the system will automatically show user’s published actors, datasets and key-value stores.

On user account, there should be just one global setting called `Make profile public` instead of the current `Make profile picture publicly visible`


### Shared actors

For example:

```
https://apify.com/jancurn/some-scraper
```



## TODOs

- Define and articulate log for CLI/SDK convention. E.g. use `actor:xxx` only when specific thing is only related to an actor, but nothing else.
- General commands e.g. `apify publish` can be used for actors and storages, so no point to have `apify actor:publish` and `apify dataset:publish`. E.g. the “actor” prefix should be used whenever it’s related to a specific actor run, or maybe when you’re inside of the run.
- How to show progress of actor run? Probably live view is best way to go!
- Support use cases like e.g. one actor pushes data to dataset, so enable another actor to push the results to google sheet (probably using webhooks)
- Cluster the operations into sections like Input/output, Chaining operations etc. For chaining, we have 3 ways: call, metamorhp, webhooks, describe the difference between them (e.g. first two need to be developed by author of the actor, the last one not)
- Mention CI/CD, e.g. how to integrate with GiHub etc.
- IDEA: How about having an "event log" for actors? They would be shown in UI, and tell user what happened in the actor. This can be done either in API or by special message to log, which will be parsed. Note - or notifications/messaging API
