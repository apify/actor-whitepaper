# Apify's Actor Programming Model Specification [DRAFT]

**The new way to develop serverless microapss called _actors_
that are easy to ship to users,
integrate, and build upon. Actors are a reincarnation of the UNIX philosophy
for programs running in the cloud.**

**Note that this document is a specification of not-yet-existing framework,
not a documentation of an existing implementation.
[Learn more](#word-of-warning)**

By [Jan Čurn](https://apify.com/jancurn),
[Marek Trunkát](https://apify.com/mtrunkat),
[Ondra Urban](https://apify.com/mnmkng), Milan Lepík, and team.
January 2022.


### Contents

<!-- toc -->

- [Introduction](#introduction)
  * [Basic concept](#basic-concept)
  * [What actors are not](#what-actors-are-not)
  * [Word of warning](#word-of-warning)
- [Philosophy](#philosophy)
  * [UNIX programs vs. actors](#unix-programs-vs-actors)
  * [Design goals](#design-goals)
  * [Relation to the Actor model](#relation-to-the-actor-model)
  * [Why the name "actor" ?](#why-the-name-actor-)
- [Installation and setup](#installation-and-setup)
  * [Apify platform](#apify-platform)
  * [Node.js](#nodejs)
  * [Python](#python)
  * [Command-line interface (CLI)](#command-line-interface-cli)
- [Programming interface](#programming-interface)
  * [Get input](#get-input)
  * [Main function](#main-function)
  * [Push results to dataset](#push-results-to-dataset)
  * [Key-value store](#key-value-store)
  * [Exit actor](#exit-actor)
  * [Aborting other actor](#aborting-other-actor)
  * [Update actor status](#update-actor-status)
  * [Start an actor (without waiting for finish)](#start-an-actor-without-waiting-for-finish)
  * [Metamorph](#metamorph)
  * [Attach webhook to an actor run](#attach-webhook-to-an-actor-run)
  * [Pipe result of an actor to another (aka chaining)](#pipe-result-of-an-actor-to-another-aka-chaining)
  * [Environment variables](#environment-variables)
  * [Watch system events](#watch-system-events)
  * [Get memory information](#get-memory-information)
- [Actor definition files](#actor-definition-files)
  * [Docker build instructions (`./Dockerfile`)](#docker-build-instructions-dockerfile)
  * [Documentation (`./README.md`)](#documentation-readmemd)
  * [Actor definition directory (`./ACTOR`)](#actor-definition-directory-actor)
  * [Actor specification file (`.ACTOR/actor.json`)](#actor-specification-file-actoractorjson)
  * [Schemas (`.ACTOR/*.json`)](#schemas-actorjson)
- [Development](#development)
  * [Local development](#local-development)
  * [Development on Apify platform](#development-on-apify-platform)
  * [Repackaging existing software as actors](#repackaging-existing-software-as-actors)
- [Sharing & Community](#sharing--community)
  * [User profile page](#user-profile-page)
  * [Shared actors](#shared-actors)
- [TODOs](#todos)

<!-- tocstop -->

## Introduction

This document explains how to develop _actors_,
a new kind of serverless microapps for general-purpose language-agnostic computing and automation jobs.
The main design goal for actors is to make it easy for developers build and ship reusable
cloud software tools, which are also easy to run
and integrate by their potentially not-too-technical users.

The actors were first introduced by [Apify](https://apify.com/) in late 2017,
as a way to easily build, package, and ship web scraping and web automation tools to customers.
Over the four years, we kept developing the concept and applied
it successfully to thousands of real-world use cases in many business areas,
well beyond the domain of web scraping.

Drawing on our experience,
we're now releasing this formal specification of the actor programming model,
in a hope to make it a new standard and help community to more effectively
build and ship software automation tools,
as well as encourage new implementations of the model in other programming languages.

### Basic concept

Actors are serverless programs running in the cloud,
best suited for execution of batch operations.
They can perform anything from simple actions such as
filling out a web form or sending an email,
to complex operations such as crawling an entire website,
or removing duplicates from a large dataset.
Actors can run as short or as long as necessary, from seconds to hours, even infinitely.

Basically, actors are Docker images that additionally have:
- **Documentation** in a form of README.md file.
- **Input and output schemas** that describe what input the actor requires,
  and what results it produces.
- Access to an out-of-box **storage system** for actor data, results, and files
- **Metadata** such as the actor name, description, author and version.

The documentation and input/output schemas are the key ingredients
that make it possible for people to easily understand what the actor does,
enter the required inputs, and integrate the results of the actor into their other workflows.
Actors can easily call and interact with each other, enabling building more complex
tools on top of simple ones.

The actors can be published
on the [Apify platform](https://apify.com/store),
which automatically generates a rich website with documentation
and a practical user interface to encourage people to try the actor right away.
The platform takes care of securely hosting the actors' Docker containers
and scaling the computing, storage and network resources as needed,
so neither actor developers nor the users need to deal with the infrastructure.
It just works.

The Apify platform provides an open API, webhooks
and [integrations](https://apify.com/integrations)
to services such as Zapier or Integromat, which make it easy for users
to integrate actors into their existing workflows. Additionally, the actor developers
can set a price tag for the usage of their actors, and thus make
[passive income](https://blog.apify.com/make-regular-passive-income-developing-web-automation-actors-b0392278d085/)
to have an incentive to keep developing and improving the actor for the users.

The ultimate goal of the actor programming model is to make it as simple as possible
for people to develop, run and integrate software automation tools.

### What actors are not

Actors are best suited for batch operations that take an input, perform an isolated job for a user,
and potentially produce some results.
However, actors are currently not ideally suited for continuous computing or storage workloads, such
as running a live website, API backend, or database.

### Word of warning

Currently, the only available implementation of the actor model is provided by
[Apify SDK for Node.js](https://sdk.apify.com), but it uses a legacy API and syntax
that is not described in this document.
The goal of this document is to define the north star how Apify's and other implementations
of actor programming model should look like. Once we release the new implementations
for Node.js, Python or CLI, we'll release this document to the public
and make it part of Apify documentation.

## Philosophy

Actors are inspired by the **[UNIX philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)** from the 1970s:

1. **Make each program do one thing well**. To do a new job, build afresh rather than complicate old programs by adding new “features”.
2. Expect the **output of every program to become the input to another**, as yet unknown, program. Don’t clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don’t insist on interactive input.
3. Design and build software, even operating systems, to be **tried early**, ideally within weeks. Don’t hesitate to throw away the clumsy parts and rebuild them.
4. **Use tools in preference to unskilled help** to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you’ve finished using them.

The UNIX philosophy is arguably one of the most important software engineering paradigms
which, together with other favorable design choices of UNIX operating systems,
ushered the computer and internet revolution.
By combining smaller parts (programs)
that can be developed and used independently,
it suddenly became possible to build, manage and gradually evolve ever more complex computing systems.
Even today's modern mobile devices are effectively UNIX-based machines that run a lot of programs
interacting with each other, and provide a terminal
which looks very much like early UNIX terminals (actually terminal is just another program).

The UNIX-style programs represent a great way to package software for usage
on a local computer. The programs can be easily used stand-alone,
but also in combination and in scripts
in order to perform much more complex tasks than an individual program ever could,
which in turn can be packaged as new programs.

The idea of actors is to bring benefits of UNIX-style programs
from a local computer into an environment of cloud
where programs run on multiple computers
communicating over a network that is subject to latency and partitioning,
there is no global atomic filesystem,
and where programs are invoked via API calls rather than system calls.

Each actor should do just one thing and do it well.
Actors can be used stand-alone, as well as combined or scripted into more complex
systems, which in turn can become new actors.
Actors provide a simple user interface and documentation to help users interact with them.

### UNIX programs vs. actors

The following table shows equivalents of key concepts of UNIX programs and actors.

**TODO:** Add to the table links to the texts below

UNIX programs  | Actors 
|---|---
Command-line options |	Input object
Read stdin |	Read from a dataset
Write to stdout	| Push data to dataset, update actor status
Write to stderr	| Set exit message
Program exit code | Actor exit code
File system	| Key-value store

### Design goals

Make it really easy to use, i.e. generate the UI etc.

- Keep it as simple as possible, but not simpler
- Each actor should do just one thing, and have everything to run on its own
- TODO...

### Relation to the Actor model

Note that actors are only loosely related to
the **actor model** known from computer science.
According to [Wikipedia](https://en.wikipedia.org/wiki/Actor_model):

> The actor model in computer science is a mathematical model of concurrent computation
> that treats actor as the universal primitive of concurrent computation.
> In response to a message it receives, an actor can: make local decisions,
> create more actors, send more messages, and determine how to respond to the
> next message received. Actors may modify their own private state,
> but can only affect each other indirectly through messaging
> (removing the need for lock-based synchronization).

While the theoretical actor model is conceptually very similar to "our" actor programming model,
this similarity is rather coincidental. 
Our primary focus was always on practical software engineering utility, not an
implementation of a formal mathematical model.

For example, our actors
do not provide any standard message passing mechanism. The actors might communicate together
directly via HTTP requests (see live view - **TODO: Add link**),
manipulate each other's operation using the Apify platform API (e.g. abort another actor),
or affect each other by sharing some internal state or storage.
The actors simply do not have any formal restrictions,
and they can access whichever external systems they want.

### Why the name "actor" ?

In movies and theater, an _actor_ is someone who gets a script
and plays a role according to that script. 
Our actors also perform an act on someone's behalf, using a provided script,
and thus we considered the name "actor" as a good description.
Also, an "actor" evokes an idea of a person, which is a helpful way to think of and talk about
actors as independent entities.

Coincidentally, in the web automation world it became common to call libraries
using names related to theater, such as Puppeteer or Playwright,
confirming "actor" was a good choice.
Last but no least, our model of actors is similar
to the actor model known from the computer science.


## Installation and setup

Below are steps to start building actors in various languages and environments.

### Apify platform

You can develop and run actors in [Apify Console](https://console.apify.com/actors) without
installing any software locally. Just create a free account, and start building actors
in an online IDE.

### Node.js

To [apify](https://www.npmjs.com/package/apify) NPM package contains everything
that you need to start building actors locally in Node.js.
Just install the package to your project by running: 

```
$ npm install apify
```

### Python

To build actors in Python, simply install the [apify](https://pypi.org/project/apify/) PyPi package
to your project:

```python
pip3 install apify
```

### Command-line interface (CLI)

For local development of actors and management of the Apify platform,
it is useful to install Apify CLI.
You just need to install [Node.js](https://nodejs.org/en/download/)
and then the [apify-cli](https://www.npmjs.com/package/apify-cli) NPM package globally as follows:

```
$ sudo npm install -g apify-cli
```

To confirm the installation succeeded and to login to the Apify platform
with your username and API token, run the `login` command as follows:

```
$ apify login
```

The Apify CLI provides a number of commands, which can aid with actor development in two ways:

1. When developing actors using **Node.js or Python**, the CLI makes it easy to run the actors locally 
   or deploy them to the Apify platform, using commands such as `run` and `push`.
   For details, see [Local development](#local-development).
2. You can use the `actor` command to implement the actor logic in a **shell script**.
   This is useful for repackaging existing software tools written in an
   arbitrary language as an actor. You simply write a shell script that transforms 
   the actor input to command-line options needed by the existing software, launch it,
   and then store results as actor output.
   For details, see [Repackaging existing software as actors](#repackaging-existing-software-as-actors).
   
To get a help for a specific command, run:

 ```
$ apify help <command>
 ```

## Programming interface

By default, the following commands are expected to be called from within the actor's
context, either on Apify platform or the local environment.
The information about the current run is taken from `APIFY_ACTOR_RUN_ID`
environment variable.

For all commands,
this behavior can be overridden in options.
For example, in Node.js the options object in all commands has `actorRunId`
field. And CLI has the `--actor-run-id` flag.


### Get input

Get access to the actor input object passed by the user.
It is parsed from a JSON file, which is stored by the system in the actor's default key-value store
(usually called `INPUT`).
The input is an object with properties.
If the actor defines the [Input schema](#input-schema), the input object is guaranteed to conform to it.

#### Node.js

```jsx
import { Actor } from 'apify';

// TODO: Ondra's razor - We should instantiate new object,
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
# Emits a JSON object, which can be parsed e.g. using the "jq" tool
$ apify actor get-input | jq

> { "option1": "aaa", "option2": 456 }
```

#### UNIX equivalent

```
$ command --option1=aaa --option2=bbb
int main (int argc, char *argv[])
```

### Main function

This is an optional helper to wrap the body of the actor.

**TODO**: Is this even needed? Perhaps just to call `Actor.exit(1, ‘Something failed’)`, but that could be done by the system (e.g. the last line from stderr would go there or full). Let's see...
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

```c
int main (int argc, char *argv[]) {
  ...
}
```

### Push results to dataset

Larger results can be saved to append-only object storage called [Dataset](https://sdk.apify.com/docs/api/dataset).
When an actor starts, by default it is associated with a newly-created empty dataset.
The user can override it and specify another dataset when running the actor.

Note that Datasets can optionally be equipped with schema that ensures only certain kinds
of objects are stored in them. See [Dataset schema](#dataset-schema) bellow for more details.

#### Node.js

```jsx
// Append result object to the default dataset associated with the run
await Actor.pushData({
    someResult: 123,
});

// Append result object to a specific named dataset
const dataset = await Actor.openDataset('bob/poll-results-2019');
await dataset.pushData({ someResult: 123 });
```

#### Python

```python
# Append result object to the default dataset associated with the run
await actor.push_data({ some_result=123 })

# Append result object to a specific named dataset
dataset = await actor.open_dataset('bob/poll-results-2019')
await dataset.push_data({ some_result=123 })
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

```c
printf("Hello world\tColum 2\tColumn 3");
```


### Key-value store

Write and read arbitrary files using a storage
called [Key-value store](https://sdk.apify.com/docs/api/key-value-store).
When an actor starts, by default it is associated with a newly-created key-value store,
which only contains one file with input of the actor
(usually called `INPUT`, the exact key is defined in the `ACTOR_INPUT_KEY` environment variable).

The user can override this behavior and specify another key-value store or input key
when running the actor.

#### Node.js

```jsx
// Save object to store (stringified to JSON)
await Actor.setValue('my-state', { something: 123 });

// Save binary file to store with content type
await Actor.setValue('screenshot', buffer, { contentType: 'image/png' });

// Get record from store (automatically parsed from JSON)
const value = await Actor.getValue('my-state');
```

#### Python

```python
# Save object to store (stringified to JSON)
await actor.set_value('my-state', { something=123 })

# Save binary file to store with content type
await actor.set_value('screenshot', buffer, { contentType='image/png' })

# Get object from store (automatically parsed from JSON)
dataset = await actor.get_value('my-state')
```

#### UNIX

```
$ echo "hello world" > file.txt
$ cat file.txt
```


### Exit actor

Terminates the actor with a process exit code,
and sets a message for users telling them what happened, and how they could fix it.

#### Node.js

```jsx
// Actor will finish in 'SUCCEEDED' state
await Actor.exit(0, 'Succeeded, crawled 50 pages');

// Actor will finish in 'FAILED' state
await Actor.exit(1, `Could not finish the crawl, try increasing memory`);
```

#### Python

```python
# Actor will finish in 'SUCCEEDED' state
await actor.exit(0, 'Generated 14 screenshots')

# Actor will finish in 'FAILED' state
await actor.exit(1, 'Could not finish the crawl, try increasing memory')
```

#### CLI

```bash
# Actor will finish in 'SUCCEEDED' state
$ apify actor exit
$ apify actor exit --message "Email sent"

# Actor will finish in 'FAILED' state
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
await Actor.setStatusMessage('Everyone is well', { actorRunId: 123 });
```

### Start an actor (without waiting for finish)

Apify NOTE: The system must enable overriding the default dataset,
and e.g. forwarding the data to another named dataset,
that will be consumed by another actor.
Maybe the dataset should enable removal of records from beginning? Currently, actors need to implement it themselves.

**TODO:** We should have consistent naming, “call” is bit confusing, “run” is what it si. But will that work together with “apify run” that runs locally? In the new client we have "start"

DECISION (add explanation): "run" is for initiating the run, call is for "run" and wait.
See https://github.com/apify/actor-specs/pull/5#discussion_r775381024

**TODO:** Enable overriding of dataset to use by the actor? Perhaps it’s enough to have an utility actor (e.g. `apify/publish-dataset`), you will webhook it to actor run, and on finish, it will take the default dataset, publish it and atomically rename it (e.g. `jancurn/london-denstists`). But this way we’d lose all dataset settings (e.g. permissions, name, description), maybe Datasets should have an operation “swap” that would enable atomic replace of dataset data while keeping its ID and settings.

DECISION: We will allow users to override default dataset. Atomic rename will be a seperate feature. 
See https://github.com/apify/actor-specs/pull/5#discussion_r775382312

#### Node.js

```js
// Run actor and wait for it to finish
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

#### CLI

```
# On stdout, the commands emit actor run object (in text or JSON format),
# we shouldn't wait for finish, for that it should be e.g. "execute"
# TODO: Currently this doesn't work!
#  apify call --memory=1024 --build=beta apify/google-search-scraper
#   Error: ENOENT: no such file or directory, scandir 'apify_storage/key_value_stores/default'
# TODO: maybe keep "apify actor:call" or just "actor run" ?
#  Decision "apify actor xxx" !!!

$ apify actor call apify/google-search-scraper queries='test\ntest2' \
  countryCode='US'
$ apify actor call --json apify/google-search-scraper '{ "queries": }'
$ apify actor call --input=@data.json --json apify/google-search-scraper
$ apify actor call --memory=1024m --build=beta apify/google-search-scraper
$ apify actor call --output-record-key=SCREENSHOT apify/google-search-scraper

# Pass input from stdin
$ cat input.json | apify actor:start apify/google-search-scraper --json

# Call local actor during development
$ apify actor:start file:../some-dir someInput='xxx'
```

#### Slack

It will also be possible to run actors from Slack app.
The following command starts the actor, and then prints the messages to a Slack channel.

```
/apify run bob/google-search-scraper startUrl=afff
```

#### API

```
[POST] https://api.apify.com/v2/actors/apify~google-search-scraper/run

[POST|GET] https://api.apify.com/v2/actors/apify~google-search-scraper/run-sync?
  token=rWLaYmvZeK55uatRrZib4xbZs&
  outputRecordKey=OUTPUT
  returnDataset=true
```

#### UNIX equivalent

```
# Run a program in the background
$ command <arg1>, <arg2>, … &

// Spawn another process
posix_spawn()
```

### Metamorph

Replace running actor’s Docker image with another.
This is useful e.g. for repurposing an actor as a new actor with its own settings and documentation.

When metamorphing into another actor, the system checks
that the other actor has compatible input/output schemas,
and throws an error if not.

The target actor inherits the default storages used by the calling actor.

#### Node.js

```
await Actor.metamorph(
    'bob/web-scraper',
    { startUrls: [ "http://example.com" ] },
    { memoryMbytes: 4096 },
);
```

#### CLI

```
$ apify actor metamorph bob/web-scraper startUrls=http://example.com
$ apify actor metamorph --input=@input.json --json --memory=4096 \
  bob/web-scraper
```

#### UNIX equivalent

```
$ exec /bin/bash
```

### Attach webhook to an actor run

Run another actor or an external HTTP API endpoint after actor run finishes or fails.


#### Node.js

```js
await Actor.addWebhook({
    eventType: ['SUCCEEDED', 'FAILED'],
    requestUrl: 'http://api.example.com?something=123',
    payloadTemplate: `{
        "userId": {{userId}},
        "createdAt": {{createdAt}},
        "eventType": {{eventType}},
        "eventData": {{eventData}},
        "resource": {{resource}}
    }`,
    // Again, it's possible to attach webhook to another running actor.
    actorRunId: 'RUN_ID',
});
```

#### CLI

```
apify actor add-webhook --actor-run-id=RUN_ID \\
  --event-types=SUCCEEDED,FAILED \\
  --request-url=https://api.example.com \\
  --payload-template='{ "test": 123" }'

apify actor add-webhook --event-types=SUCCEEDED \\
  --request-actor=apify/send-mail \\
  --memory=4096 --build=beta \\
  --payload-template=@template.json

# Or maybe have a simpler API for self-actor?
apify actor add-webhook --event-types=SUCCEEDED --request-actor=apify/send-mail 
```

#### UNIX equivalent

```
# Execute commands sequentially, based on their status
// $ command1; command2 (command separator)
// $ command1 && command2 ("andf" symbol)
// $ command1 || command2 ("orf" symbol)
```



### Pipe result of an actor to another (aka chaining)

Actor can start other actors and
pass them its own dataset or key-value store.
For example, the main actor can produce files
and the spawned others can consume them, from the same storages.

In the future, we could let datasets be cleaned up from the beginning,
effectively creating a pipe, with custom rolling window.
Webhooks can be attached to storage operations,
and so launch other actors to consume newly added items or files.

#### UNIX equivalent

```
$ ls -l | grep "something" | wc -l
```

```
// TODO: Support creating chains like this
// XXX:   actor call apify/google-search-scraper
  => actor call apify/send-email queryTerms="aaa\nbbb"
// XXX:   actor call apify/web-scraper
  => actor call lukaskrivka/upload-google-sheets sheeetId="abc"
```

See note from Marek: https://github.com/apify/actor-specs/pull/5#discussion_r775390067 


### Environment variables

Actors have access to standard process environment variables.

The platform sets information about the actor execution context through
environment variables such as `APIFY_TOKEN` or `APIFY_ACTOR_RUN_ID` -
see the [Apify documentation](https://docs.apify.com/actors/development/environment-variables) for the full list.

<!-- TODO: We should provide the full list here eventually, for a complete reference. -->

Custom-defined environment variables (potentially secured with encryption)
that are then passed to the actor process both on Apify platform and in local development.
These are defined in the [.actor/ACTOR.json](/pages/ACTOR.md) file.

**Node.js**

For convenience, rather than using environment vars directly, we provide a helper function
that returns an object, with TypeScript-defined type.

```
const env = await Actor.getEnv();
console.log(env.actorRunId);
```

**CLI**

```
$ echo "$APIFY_ACTOR_RUN_ID started at $APIFY_ACTOR_RUN_STARTED_AT"
```


#### UNIX equivalent:

```
$ echo $ACTOR_RUN_ID
```

Apify NOTE: These can be defined by actor owner during build, but unlike traditional processes, they are not passed when calling another actor. System passes various runtime info to actor using env vars.

See [Environment variables](about:blank#) in Actor documentation.


### Watch system events

Receive system events e.g. CPU statistics of the running container or information about imminent [migration to another server](about:blank#xxx).

In the future, this can be extended to custom events and messages.

#### Node.js

```
Actor.events.on('cpuInfo', data => {
    if (data.isCpuOverloaded) console.log('Oh no, the CPU is overloaded!');
});
```

#### UNIX equivalent

```
signal(SIGINT, handle_sigint);
```

### Get memory information

Get information about the total and available memory of the actor’s container or local system.
For example, this is useful to auto-scale a pool
of workers used for crawling large websites.

#### Node.js

```
const memoryInfo = await Actor.getMemoryInfo();
```

#### UNIX equivalent

```
# Print memory usage of programs
$ ps -a
```


## Actor definition files

The actor platform supports the following special files.

### Docker build instructions (`./Dockerfile`)

Instructions for the platform how to build the actor Docker image and run it.
This is how actors are started. [Learn more](https://docs.docker.com/engine/reference/builder/) about Dockerfiles.

### Documentation (`./README.md`)

The README.md [Markdown](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) file associated with the actor
is used as its documentation page.

A great explanation for users what the actor does and how it works.
Good documentation makes good programmers!

[Learn more](https://docs.apify.com/actors/publishing/seo-and-promotion) how to write great SEO-optimized READMEs.

### Actor directory (`./ACTOR`)

This is the main directory with definition files of the actor.
It links your source code with an Apify actor in the cloud.
The entire directory should be added to the source control.

Files in this directory are used by Apify CLI to get defaults for the `apify push` command.

### Actor specification file (`.ACTOR/actor.json`)

This replaces the legacy `actor.json` file,
and defines references to input and output schemas.

For details, see [.ACTOR/actor.json](./pages/ACTOR.md)

### Schemas (`.ACTOR/*.json`)



OUTPUT schema


## Development

High-level overview how to build new actors.

### Local development

Actors can be developed and run locally. To support running other actors, we need to define mapping
of `username/actor` to local directories with `.actor` sub-directory.

Explain basic workflow with "apify" - create, run, push etc.

TODO: Maybe using environment variable with the mapping?

### Development on Apify platform

....

### Repackaging existing software as actors



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

- Cluster the operations into sections like Input/output, Chaining operations etc. For chaining, we have 3 ways: call, metamorhp, webhooks, describe the difference between them (e.g. first two need to be developed by author of the actor, the last one not)
- Mention CI/CD, e.g. how to integrate with GiHub etc.
- IDEA: How about having an "event log" for actors?
  They would be shown in UI, and tell user what happened in the actor. This can be done either in API or by special message to log, which will be parsed. **Or with the notifications/messaging API**
