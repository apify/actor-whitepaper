# The Actor Programming Model Whitepaper [DRAFT]

**The whitepaper describes new concept for building serverless microapps called _actors_,
which are easy to develop, share, integrate, and build upon.
Actors are a reincarnation of the UNIX philosophy
for programs running in the cloud.**

Written by [Jan Čurn](https://apify.com/jancurn),
[Marek Trunkát](https://apify.com/mtrunkat),
[Ondra Urban](https://apify.com/mnmkng), and the Apify team
in January 2023.


## Contents

<!-- toc -->

- [Introduction](#introduction)
  * [Overview](#overview)
- [Basic concepts](#basic-concepts)
  * [Input](#input)
  * [Run](#run)
  * [Output](#output)
  * [Storage](#storage)
  * [Integrations](#integrations)
  * [Monetization](#monetization)
  * [What actors are not](#what-actors-are-not)
- [Philosophy](#philosophy)
  * [UNIX programs vs. actors](#unix-programs-vs-actors)
  * [Design principles](#design-principles)
  * [Relation to the Actor model](#relation-to-the-actor-model)
  * [Why the name "actor" ?](#why-the-name-actor-)
- [Installation and setup](#installation-and-setup)
  * [Apify platform](#apify-platform)
  * [Node.js](#nodejs)
  * [Python](#python)
  * [Command-line interface (CLI)](#command-line-interface-cli)
- [Programming interface](#programming-interface)
  * [Actor initialization](#actor-initialization)
  * [Get input](#get-input)
  * [Key-value store access](#key-value-store-access)
  * [Push results to dataset](#push-results-to-dataset)
  * [Exit actor](#exit-actor)
  * [Environment variables](#environment-variables)
  * [Actor status](#actor-status)
  * [System events](#system-events)
  * [Get memory information](#get-memory-information)
  * [Start another actor](#start-another-actor)
  * [Metamorph](#metamorph)
  * [Attach webhook to an actor run](#attach-webhook-to-an-actor-run)
  * [Abort another actor](#abort-another-actor)
  * [Live view web server](#live-view-web-server)
- [Actor definition files](#actor-definition-files)
  * [Actor file](#actor-file)
  * [Dockerfile](#dockerfile)
  * [README](#readme)
  * [Schema files](#schema-files)
  * [Backward compatibility](#backward-compatibility)
- [Development](#development)
  * [Local development](#local-development)
  * [Deployment to Apify platform](#deployment-to-apify-platform)
  * [Repackaging existing software as actors](#repackaging-existing-software-as-actors)
  * [Continuous integration and delivery](#continuous-integration-and-delivery)
- [Sharing & Community](#sharing--community)
  * [Shared actors](#shared-actors)
- [TODOs (@jancurn)](#todos-jancurn)

<!-- tocstop -->

## Introduction

This document explains how to develop _actors_,
a new kind of serverless microapps for general-purpose language-agnostic computing and automation jobs.
The main design goal for actors is to make it easy for developers build and ship reusable
cloud software tools, which are also easy to run
and integrate by potentially not-too-technical users.

The actors were first introduced by [Apify](https://apify.com/) in late 2017,
as a way to easily build, package, and ship web scraping and web automation tools to customers.
Over the next years, Apify kept developing the concept and applied
it successfully to thousands of real-world use cases in many business areas,
well beyond the domain of web scraping.

Drawing on this experience,
we're releasing this specification of the actor programming model to the public,
in a hope to make it a new open standard, and to help community to more effectively
build and ship software automation tools,
as well as encourage new implementations of the model in other programming languages.

The goal of this document is to be the north star showing what the
actor programming model is and what its implementations should support.
Currently, the most complete implementation of actor model is provided
by the Apify platform, with SDKs for 
[Node.js](https://sdk.apify.com/) and
[Python](https://pypi.org/project/apify/),
and a [command-line interface](https://docs.apify.com/cli).
Beware that these implementations do not support all features yet. This is work in progress. 


### Overview

Actors are serverless programs running in the cloud.
They can perform anything from simple actions such as
filling out a web form or sending an email,
to complex operations such as crawling an entire website,
or removing duplicates from a large dataset.
Actors can run as short or as long as necessary, from seconds to hours, even infinitely.

Basically, actors are programs packaged as Docker images,
which accept a well-defined JSON input, perform
an action, and optionally produce a well-defined JSON output.

Actors have the following elements:
- **Dockerfile** which specifies where is the actor's source code,
  how to build it, and run it
- **Documentation** in a form of README.md file
- **Input and output schemas** that describe what input the actor requires,
  and what results it produces
- Access to an out-of-box **storage system** for actor data, results, and files
- **Metadata** such as the actor name, description, author, and version

The documentation and the input/output schemas make it possible for people to easily understand what the actor does,
enter the required inputs both in user interface or API,
and integrate the results of the actor into their other workflows.
Actors can easily call and interact with each other, enabling building more complex
systems on top of simple ones.

The actors can be published
on the [Apify platform](https://apify.com/store),
which automatically generates a rich website with documentation
and a practical user interface, in order to encourage people to try the actor right away.
The Apify platform takes care of securely hosting the actors' Docker containers
and scaling the computing, storage and network resources as needed,
so neither actor developers nor the users need to deal with the infrastructure.
It just works.

The Apify platform provides an open API, cron-style scheduler, webhooks
and [integrations](https://apify.com/integrations)
to services such as Zapier or Make, which make it easy for users
to integrate actors into their existing workflows. Additionally, the actor developers
can set a price tag for the usage of their actors, and thus make
[passive income](https://blog.apify.com/make-regular-passive-income-developing-web-automation-actors-b0392278d085/)
to have an incentive to keep developing and improving the actor for the users.

Currently, actors can run locally or on the Apify platform. However, one of the goals of this open 
specification is to motivate creation of new runtime environments outside of Apify.

The ultimate goal of the actor programming model is to make it as simple as possible
for people to develop, run, and integrate software automation tools.


## Basic concepts

This section describes core features of actors, what they are good for,
and how actors differ from other serverless computing platforms. 

### Input

Each actor accepts an **input object**, which tells it what it should do.
The object is passed in JSON format, and its properties have
a similar role as command-line arguments when running a program in a UNIX-like operating system.

For example, an input object for an actor `bob/screenshot-taker` can look like this:

```json
{
  "url": "http://www.example.com",
  "width": 800,
  "height": 600
}
```

The input object represents a standardized way for the caller to control the actor's activity,
whether starting it using API, in user interface, CLI, or scheduler.
The actor can access the value of the input object using the [Get input](#get-input) function.

In order to specify what kind of input object an actor expects,
the actor developer can define an [Input schema file](./pages/INPUT_SCHEMA.md).
For example, the input schema for actor `bob/screenshot-taker` will look like this:

```json
TODO
```

The input schema is used by the system to:

- Validate the passed input JSON object on actor run,
  so that actors don't need to perform input validation and error handling in their code.
- Render user interface for actors to make it easy for users to run and test them manually
- Generate actor API documentation and integration code examples on the web or in CLI, 
  making actors easy for users to integrate the actors.
- Simplify integration of actors into automation workflows such as Zapier or Make, by providing smart connectors
  that smartly pre-populate and link actor input properties

**TODO: Show screenshots with web interface, API docs, and code examples**

### Run environment

The actors run within an isolated Docker container with access to local file system and network,
and they can perform an arbitrary computing activity or call external APIs.
The **standard output** of the actor's program (stdout and stderr) is printed out and logged,
which is useful for debugging.

In order to inform the users about the progress, the actors might set a [**status message**](#actor-status),
which is then displayed in the user interface and also available via API.

Running actors can also launch a [**live-view web server**](#live-view-web-server),
which is assigned a unique local or public URL to receive HTTP requests. For example,
this is useful for messaging and interaction between actors, for running request-response REST APIs, or 
providing a full-featured website.

The actors can store their working data or results into specialized **storages**
called [Key-value store](#key-value-store) and [Dataset](#dataset) storages,
from which they can be easily exported using API or integrated in other actors.

### Output

While the input object provides a standardized way to invoke actors,
the actors can also generate an **output object**, which is a standardized way to display, consume and integrate
actors' results.

The actor results are typically fully available only once the actor run finishes,
but the consumers of the results might want to access partial results during the run.
Therefore, the actors don't generate the output object directly, but rather
define an [Output schema file](./pages/OUTPUT_SCHEMA.md), which contains
instruction how to generate the output object. The output object is stored
to the Actor run object under the `output` property, and returned via API immediately after
the actor is started, without the need to wait for it to finish or generate the actual results.

TODO: Consider storing the object also to key-value store...

The output object is similar to input object, as it contains properties and values.
For example, for the `bob/screenshot-taker` actor the output object can look like this:

```json
TODO
```

The output object is generated automatically by the system based on the output schema file,
which can look as follows:

```json
TODO
```

The output schema and output object can then be used by callers of actors to figure where to find
actor results, how to display them to users, or simplify plugging of actors in workflow automation pipelines.

### Storage

The actor system provides two specialized storages that can be used by actors for storing files and results:
**Key-value store** and **Dataset**, respectively. For each actor run,
the system automatically creates both these storages 
in empty state, and makes them readily available for the actor.

Besides these default storages, actors are free to create new or
access other existing key-value stores and datasets, either by ID or a name that can be set to them.
The storages are accessible through an API and SDK also externally, for example,
to download results when the actor finishes.

Note that the actors are free to access any other external storage through any third-party API.

#### Key-value store

The key-value store is a simple data storage that is used for saving and reading
files or data records. The records are represented by a unique text key and the data associated with a MIME content type.
Key-value stores are ideal for saving things like screenshots, web pages, PDFs, or to persist the state of actors.

Each actor run is associated with a default empty key-value store, which is created exclusively for the run.
The [actor input](#input) is stored as JSON file into the default key-value store under the key defined by
the `ACTOR_INPUT_KEY` environment variable (usually `INPUT`).
The actor can read this object using the [Get input](#get-input) function.

The actor can read and write records to key-value stores using the API. For details,
see [Key-value store access](#key-value-store-access).


Output + schema...


#### Dataset

Dataset storage allows you to store a series of data objects such as results from web scraping, crawling or data processing jobs. You can export your datasets in JSON, CSV, XML, RSS, Excel or HTML formats.

The Dataset represents a store for structured data where each object stored has the same attributes,
such as online store products or real estate offers. You can imagine it as a table, where each object is
a row and its attributes are columns. Dataset is an append-only storage - you can only add new records to
it but you cannot modify or remove existing records. Typically it is used to store crawling results.

Larger results can be saved to append-only object storage called [Dataset](https://sdk.apify.com/docs/api/dataset).
When an actor starts, by default it is associated with a newly-created empty default dataset.
The actor can create additional datasets or access existing datasets created by other actors,
and use those as needed.

### Integrations

Describe chaining, webhooks, running another, metamorph etc.


### Publishing & Monetization

....Charging money - basic info?

### What actors are not

Actors are best suited for batch operations that take an input, perform an isolated job for a user,
and potentially produce some output.
However, actors are currently not best suited for continuous computing or storage workloads, such
as running a live website, API backend, or database.

As actors are based on Docker, it takes certain amount of time to spin up the container
and launch its main process. Doing this for every small HTTP transaction (e.g. API call) is not efficient,
even for highly-optimized Docker images. For long-running jobs, actor execution might be migrated
to another machine, making it unsuitable for running databases.

## Philosophy

Actors are inspired by the **[UNIX philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)** from the 1970s:

1. **Make each program do one thing well**. To do a new job, build afresh rather than complicate old programs by adding new “features”.
2. Expect the **output of every program to become the input to another, as yet unknown, program**. Don’t clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don’t insist on interactive input.
3. Design and build software, even operating systems, to be **tried early**, ideally within weeks. Don’t hesitate to throw away the clumsy parts and rebuild them.
4. **Use tools in preference to unskilled help** to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you’ve finished using them.

The UNIX philosophy is arguably one of the most important software engineering paradigms
which, together with other favorable design choices of UNIX operating systems,
ushered the computer and internet revolution.
By combining smaller parts
that can be developed and used independently (programs),
it suddenly became possible to build, manage and gradually evolve ever more complex computing systems.
Even today's modern mobile devices are effectively UNIX-based machines that run a lot of programs
interacting with each other, and provide a terminal
which looks very much like early UNIX terminals. In fact, terminal is just another program.

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

| UNIX programs            | Actors |
|--------------------------|------------------|
| Command-line options     | [Input object](#get-input) |
| Read stdin               | No direct equivalent, you can [read from a dataset](#dataset) specified in the input.|
| Write to stdout	       | [Push results to dataset](#push-results-to-dataset), set [actor status](#actor-status)|
| Write to stderr	       | No direct equivalent, you can write errors to log, set error status message, or push failed dataset items into an "error" dataset.|
| File system	           | [Key-value store](#key-value-store-access)|
| Process identifier (PID) | Actor run ID |
| Process exit code        | [Actor exit code](#exit-actor) |

### Design principles

- Each actor should do just one thing, and do it well.
- Optimize for the users of the actors, help them understand what the actor does, easily run it, and integrate.
- Keep the system as simple as possible, so that actors can be built and used by the top 90% of developers.

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
directly via HTTP requests (see [Live view](#live-view)),
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

The most complete implementation of actor system is provided by the Apify SDK for Node.js,
via the [apify](https://www.npmjs.com/package/apify) NPM package. The package contains everything
that you need to start building actors locally.
You can install it to your Node.js project by running: 

```bash
$ npm install apify
```

### Python

To build actors in Python, simply install the Apify SDK for Python,
via the [apify](https://pypi.org/project/apify/) PyPi package
into your project:

```bash
$ pip3 install apify
```

### Command-line interface (CLI)

For local development of actors and management of the Apify platform,
it is useful to install Apify CLI.
You just need to install [Node.js](https://nodejs.org/en/download/)
and then the [apify-cli](https://www.npmjs.com/package/apify-cli) NPM package globally as follows:

```bash
$ npm install -g apify-cli
```

To confirm the installation succeeded and to login to the Apify platform
with your username and API token, run the `login` command as follows:

```bash
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

 ```bash
$ apify help <command>
 ```

## Programming interface

The commands described in this section are expected to be called from within a context
of a running actor, both in local environment or on the Apify platform.
By default, the identifier of the current actor run is taken from `ACTOR_RUN_ID`
environment variable, but it can be overridden.
For example, in Node.js you can initialize the `Actor` class using another `actorRunId`,
or in the `apify actor` CLI command you can pass the `--actor-run-id` flag.

### Actor initialization

First, the actor should be initialized. During initialization, it prepares to receive events from Apify platform, determines machine and storage configuration and optionally purges previous state from local storage. It will also create a default instance of the Actor class.

It is not required to perform the initialization explicitly, because the actor will initialize on execution of any actor method, but we strongly recommend it to prevent race conditions.

#### Node.js
 
In Node.js the actor is initialized by calling the `init()` method. It should be paired with an `exit()` method which terminates the actor. Use of `exit()` is not required, but recommended. For more information go to [Exit actor](#exit-actor).

```js
import { Actor } from 'apify';

await Actor.init();

const input = await Actor.getInput();
console.log(input);

await Actor.exit();
```

An alternative way of initializing the actor is with a `main()` function. This is useful in environments where the latest JavaScript
syntax and top level awaits are not supported. The main function is only syntax-sugar for `init()` and `exit()`. It will call `init()` before it executes its callback and `exit()` after the callback resolves. 

```js
import { Actor } from 'apify';

Actor.main(async () => {
  const input = await Actor.getInput();
  // ...
});
```

#### Python

TODO: @fnesveda please add Python examples.

#### UNIX equivalent

```c
int main (int argc, char *argv[]) {
  ...
}
```

### Get input

Get access to the actor input object passed by the user.
It is parsed from a JSON file, which is stored by the system in the actor's default key-value store,
Usually the file is called `INPUT`, but the exact key is defined in the `ACTOR_INPUT_KEY` environment variable.

The input is an object with properties.
If the actor defines the input schema, the input object is guaranteed to conform to it.
For details, see [Input and output](#input-and-output).

#### Node.js

```js
const input = await Actor.getInput();
console.log(input);

// prints: { "option1": "aaa", "option2": 456 }
```

#### Python

```python
input = actor.get_input()
print(input)
```

#### CLI

```bash
# Emits a JSON object, which can be parsed e.g. using the "jq" tool
$ apify actor get-input | jq

> { "option1": "aaa", "option2": 456 }
```

#### UNIX equivalent

```bash
$ command --option1=aaa --option2=bbb
```

```c
int main (int argc, char *argv[]) {}
```

### Key-value store access

Write and read arbitrary files using a storage
called [Key-value store](https://sdk.apify.com/docs/api/key-value-store).
When an actor starts, by default it is associated with a newly-created key-value store,
which only contains one file with input of the actor (see [Get input](#get-input)).

The user can override this behavior and specify another key-value store or input key
when running the actor.

#### Node.js

```js
// Save object to store (stringified to JSON)
await Actor.setValue('my_state', { something: 123 });

// Save binary file to store with content type
await Actor.setValue('screenshot.png', buffer, { contentType: 'image/png' });

// Get record from store (automatically parsed from JSON)
const value = await Actor.getValue('my_state');

// Access another key-value store by its name
const store = await Actor.openKeyValueStore('screenshots-store');
await store.setValue('screenshot.png', buffer, { contentType: 'image/png' });
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

```bash
$ echo "hello world" > file.txt
$ cat file.txt
```

### Push results to dataset

Larger results can be saved to append-only object storage called [Dataset](https://sdk.apify.com/docs/api/dataset).
When an actor starts, by default it is associated with a newly-created empty default dataset.
The actor can create additional datasets or access existing datasets created by other actors,
and use those as needed.

Note that Datasets can optionally be equipped with schema that ensures only certain kinds
of objects are stored in them. See [Dataset schema file](./pages/DATASET_SCHEMA.md) for more details.

#### Node.js

```js
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
# Push data to default dataset, in JSON format
$ echo '{ "someResult": 123 }' | actor push-data --json
$ apify actor push-data --json='{ "someResult": 123 }'
$ apify actor push-data --json=@result.json

# Push data to default dataset, in text format
$ echo "someResult=123" | apify actor push-data
$ apify actor push-data someResult=123

# Push to a specific dataset in the cloud
$ apify actor push-data --dataset=bob/election-data someResult=123

# Push to dataset on local system
$ apify actor push-data --dataset=./my_dataset someResult=123
```

#### UNIX equivalent

```c
printf("Hello world\tColum 2\tColumn 3");
```

### Exit actor

When the main actor process exits (i.e. the Docker container stops running),
the actor run is considered finished and the process exit code is used to determine
whether the actor has succeeded (exit code `0` leads to status `SUCCEEDED`)
or failed (exit code not equal to `0` leads to status `SUCCEEDED`).
In this case, the platforms set a status message to a default value like `Actor exit with exit code 0`,
which is not very descriptive for the users.

An alternative and preferred way to exit an actor is using the `exit` function in SDK, as
shown below. This has two advantages:

- You can provide a custom status message for users to tell them what the actor achieved
  On error, try to explain to users
  what happened and most importantly, how they can fix the error.
  This greatly improves user experience.
- The system emits the `exit` event, which can be listened to and used by various
  components of the actor to perform a cleanup, persist state, etc.
  Note that the caller of exit can specify how long should the system wait for all `exit`
  event handlers to complete before closing the process, using the `timeoutSecs` option.
  For details, see [System Events](#system-events).

#### Node.js

```js
// Actor will finish with 'SUCCEEDED' status
await Actor.exit('Succeeded, crawled 50 pages');

// Exit right away without calling `exit` handlers at all
await Actor.exit('Done right now', { timeoutSecs: 0 });

// Actor will finish with 'FAILED' status 
await Actor.exit('Could not finish the crawl, try increasing memory', { exitCode: 1 });

// ... or nicer way using this syntactic sugar:
await Actor.fail('Could not finish the crawl, try increasing memory');

// Register a handler to be called on exit.
// Note that the handler has `timeoutSecs` to finish its job
Actor.on('exit', ({ statusMessage, exitCode, timeoutSecs }) => {
    // Perform cleanup...
})
```

#### Python

```python
# Actor will finish in 'SUCCEEDED' state
await actor.exit('Generated 14 screenshots')

# Actor will finish in 'FAILED' state
await actor.exit('Could not finish the crawl, try increasing memory', { exitCode: 1 })
# ... or nicer way using this syntactic sugar:
await Actor.fail('Could not finish the crawl, try increasing memory');
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
exit(1);
```


### Environment variables

Actors have access to standard process environment variables. 
The Apify platform uses environment variables prefixed with `ACTOR_` to pass the actors information
about the execution context.

| Environment variable               | Description                                                                                                                                                                                                                |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ACTOR_RUN_ID`                     | ID of the actor run.                                                                                                                                                                                                       |
| `ACTOR_DEFAULT_KEY_VALUE_STORE_ID` | ID of the key-value store where the actor's input and output data are stored.                                                                                                                                    |
| `ACTOR_DEFAULT_DATASET_ID`         | ID of the dataset where you can push the data.                                                                                                                                                                        |
| `ACTOR_DEFAULT_REQUEST_QUEUE_ID`   | ID of the request queue that stores and handles requests that you enqueue.                                                                                                                                            |
| `ACTOR_INPUT_KEY`                  | The key of the record in the default key-value store that holds the actor input. Typically it's `INPUT`, but it might be something else.                                                             |
| `ACTOR_MEMORY_MBYTES`              | Indicates the size of memory allocated for the actor run, in megabytes (1,000,000 bytes). It can be used by actors to optimize their memory usage.                                                                       |
| `ACTOR_STARTED_AT`                 | Date when the actor was started, in ISO 8601 format. For example, `2022-01-02T03:04:05.678`.                                                                                                                                                                                          |
| `ACTOR_TIMEOUT_AT`                 | Date when the actor will time out, in ISO 8601 format.                                                                                                                                                                          |
| `ACTOR_EVENTS_WEBSOCKET_URL`       | Websocket URL where actor may listen for events from Actor platform. See [System events](#system-events) for more details.                                       |
| `ACTOR_WEB_SERVER_PORT`            | TCP port on which the actor can start a HTTP server to receive messages from the outside world. See [Live view web server](#live-view-web-server) section for more details. |
| `ACTOR_WEB_SERVER_URL`             | A unique public URL under which the actor run web server is accessible from the outside world. See [Live view web server](#live-view-web-server) section for more details.  |

**WARNING/TODO**: This is not implemented yet. Currently, the actors use environment variables
prefixed by `APIFY_`. See the full list of environment variables
in [Apify documentation](https://docs.apify.com/actors/development/environment-variables).

<!--
  TODO: Implement these env vars, we need to keep the old ones for backwards compatibility
  Only Apify-specific env vars should have prefix APIFY_, e.g. APIFY_PROXY_PASSWORD, APIFY_TOKEN or APIFY_USER_ID.
  Mention these additional env vars in the text
-->

The actor developer can also define custom environment variables
that are then passed to the actor process both in local development environment or on the Apify platform.
These variables are defined in the [.actor/actor.json](/pages/ACTOR.md) file using the `environmentVariables` directive,
or manually in the user interface in Apify Console.

The environment variables can be set as secure in order to protect sensitive data such as API keys or passwords.
The value of a secure environment variable is encrypted and can only be retrieved by the actors during their run,
but not outside the runs. Furthermore, values of secure environment variables are omitted from the log.

#### Node.js

For convenience, rather than using environment vars directly, we provide a `Configuration` class
that allows reading and updating the actor configuration.

```javascript
const token = Actor.config.get('token');

// use different token
Actor.config.set('token', 's0m3n3wt0k3n')
```

#### CLI

```bash
$ echo "$ACTOR_RUN_ID started at $ACTOR_STARTED_AT"
```


#### UNIX equivalent

```bash
$ echo $ACTOR_RUN_ID
```

### Actor status

Each actor run has a status (the `status` field), which can be one of the following values:

|Status|Type|Description|
|--- |--- |--- |
|`READY`|initial|Started but not allocated to any worker yet|
|`RUNNING`|transitional|Executing on a worker|
|`SUCCEEDED`|terminal|Finished successfully|
|`FAILED`|terminal|Run failed|
|`TIMING-OUT`|transitional|Timing out now|
|`TIMED-OUT`|terminal|Timed out|
|`ABORTING`|transitional|Being aborted by user|
|`ABORTED`|terminal|Aborted by user|

Additionally, the actor run has a status message (the `statusMessage` field),
which contains a text for users informing them what the actor is currently doing,
and thus greatly improve their user experience.

When an actor exits, the status message is either automatically set to some default text
(e.g. "Actor finished with exit code 1"), or to a custom message - see [Exit actor](#exit-actor) for details.

When the actor is running, it should periodically update the status message as follows,
to keep users informed and happy. The function can be called as often as necessary,
the SDK only invokes API if status changed. This is to simplify the usage.

#### Node.js

```js
await Actor.setStatusMessage('Crawled 45 of 100 pages');

// Setting status message to other actor externally is also possible
await Actor.setStatusMessage('Everyone is well', { actorRunId: 123 });
```

#### Python

```python
await actor.set_status_message('Crawled 45 of 100 pages')
```

#### CLI

```bash
$ apify actor set-status-message "Crawled 45 of 100 pages"
$ apify actor set-status-message --run=[RUN_ID] --token=X "Crawled 45 of 100 pages"
```


### System events

Actors are notified by the system about various events such as a migration to another server,
[abort operation](#abort-another-actor) triggered by another actor, or the CPU being overloaded.

Currently, the system sends the following events:

| Event name     | Payload | Description |
| -------------- | ------- | ----------- |
| `cpuInfo`      | `{ isCpuOverloaded: Boolean }` | The event is emitted approximately every second and it indicates whether the actor is using the maximum of available CPU resources. If that’s the case, the actor should not add more workload. For example, this event is used by the AutoscaledPool class. | 
| `migrating`    | N/A | Emitted when the actor running on the Apify platform is going to be migrated to another worker server soon. You can use it to persist the state of the actor and abort the run, to speed up migration. For example, this is used by the RequestList class. |
| `aborting`     | N/A | When a user aborts an actor run on the Apify platform, they can choose to abort gracefully to allow the actor some time before getting killed. This graceful abort emits the `aborting` event which the SDK uses to gracefully stop running crawls and you can use it to do your own cleanup as well.|
| `persistState` | `{ isMigrating: Boolean }` | Emitted in regular intervals (by default 60 seconds) to notify all components of Apify SDK that it is time to persist their state, in order to avoid repeating all work when the actor restarts. This event is automatically emitted together with the migrating event, in which case the `isMigrating` flag is set to `true`. Otherwise the flag is `false`. Note that the `persistState` event is provided merely for user convenience, you can achieve the same effect using `setInterval()` and listening for the `migrating` event. |

In the future, the event mechanism might be extended to custom events and messages enabling communication between
actors.

Under the hood, actors receive the system events by connecting to a web socket address specified
by the `ACTOR_EVENTS_WEBSOCKET_URL` environment variable.
The system sends messages in JSON format in the following structure:

```js
{
    // Event name
    name: String,

    // Time when the event was created, in ISO format
    createdAt: String,
          
    // Optional object with payload      
    data: Object,
}
```

Note that some events (e.g. `persistState`) are not sent by the system via the web socket,
but generated virtually on the Actor SDK level.

#### Node.js

```js
// Add event handler
Actor.on('cpuInfo', (data) => {
    if (data.isCpuOverloaded) console.log('Oh no, we need to slow down!');
});

// Remove all handlers for a specific event
Actor.off('systemInfo');

// Remove a specific event handler
Actor.off('systemInfo', handler);
```

#### Python

TODO: @fnesveda Add Python example, here and elsewhere too


#### UNIX equivalent

```c
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

```bash
# Print memory usage of programs
$ ps -a
```


### Start another actor

Actor can start other actors, if they have a permission.

It can override the default dataset or key-value store,
and e.g. forwarding the data to another named dataset,
that will be consumed by the other actor.

The `call` operation waits for the other actor to finish, the `start` operation
returns immediately.

#### Node.js

```js
// Start actor and return a Run object
const run = await Actor.start(
    'apify/google-search-scraper', // name of the actor to start
    { queries: 'test' }, // input of the actor
    { memory: 2048 }, // run configuration
);

// Start actor and wait for it to finish
const run2 = await Actor.call(
  'apify/google-search-scraper', 
  { queries: 'test' },
  { memory: 2048 },
);
```


#### CLI

```bash
# On stdout, the commands emit actor run object (in text or JSON format),
# we shouldn't wait for finish, for that it should be e.g. "execute"
$ apify actor call apify/google-search-scraper queries='test\ntest2' \
  countryCode='US'
$ apify actor call --json apify/google-search-scraper '{ "queries": }'
$ apify actor call --input=@data.json --json apify/google-search-scraper
$ apify actor call --memory=1024 --build=beta apify/google-search-scraper
$ apify actor call --output-record-key=SCREENSHOT apify/google-search-scraper

# Pass input from stdin
$ cat input.json | apify actor call apify/google-search-scraper --json

# Call local actor during development
$ apify actor call file:../some-dir someInput='xxx'
```

#### Slack

It will also be possible to run actors from Slack app.
The following command starts the actor, and then prints the messages to a Slack channel.

```
/apify start bob/google-search-scraper startUrl=afff
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

```bash
# Run a program in the background
$ command <arg1>, <arg2>, … &
```

```c
// Spawn another process
posix_spawn();
```

### Metamorph 🪄

This is the most magical actor operation, which replaces running actor’s Docker image with another actor,
similar to UNIX `exec` command.
It is used for building new actors on top of existing ones.
You simply define input schema and write README for a specific use case,
and then delegate the work to another actor.

An actor can metamorph only to actors that have compatible output schema as the main actor,
in order to ensure logical and consistent outcomes for users. 
If the output schema of the target actor is not compatible, the system should throw an error.

<!-- TODO: This is not implemented yet -->

Note that the target actor inherits the default storages used by the calling actor.
The target actor input is stored to the default key-value store, often under a key such as `INPUT-2`. 
Internally, the target actor can recursively metamorph into another actor.

#### Node.js

```js
await Actor.metamorph(
    'bob/web-scraper',
    { startUrls: [ "http://example.com" ] },
    { memoryMbytes: 4096 },
);
```

#### CLI

```bash
$ apify actor metamorph bob/web-scraper startUrls=http://example.com
$ apify actor metamorph --input=@input.json --json --memory=4096 \
  bob/web-scraper
```

#### UNIX equivalent

```bash
$ exec /bin/bash
```

### Attach webhook to an actor run

Run another actor or an external HTTP API endpoint after actor run finishes or fails.


#### Node.js

```js
await Actor.addWebhook({
    eventType: ['ACTOR.RUN.SUCCEEDED', 'ACTOR.RUN.FAILED'],
    requestUrl: 'http://api.example.com?something=123',
    payloadTemplate: `{
        "userId": {{userId}},
        "createdAt": {{createdAt}},
        "eventType": {{eventType}},
        "eventData": {{eventData}},
        "resource": {{resource}}
    }`,
});
```

#### CLI

```bash
apify actor add-webhook --actor-run-id=RUN_ID \\
  --event-types=ACTOR.RUN.SUCCEEDED,ACTOR.RUN.FAILED \\
  --request-url=https://api.example.com \\
  --payload-template='{ "test": 123" }'

apify actor add-webhook --event-types=ACTOR.RUN.SUCCEEDED \\
  --request-actor=apify/send-mail \\
  --memory=4096 --build=beta \\
  --payload-template=@template.json

# Or maybe have a simpler API for self-actor?
apify actor add-webhook --event-types=ACTOR.RUN.SUCCEEDED --request-actor=apify/send-mail 
```

#### UNIX equivalent

```bash
# Execute commands sequentially, based on their status
$ command1; command2    # (command separator)
$ command1 && command2  # ("andf" symbol)
$ command1 || command2  # ("orf" symbol)
```


### Abort another actor

Abort itself or another running actor on the Apify platform,
changing its [status](#actor-status) to `ABORTED`.

#### Node.js

```js
await Actor.abort({ statusMessage: 'Job was done,', actorRunId: 'RUN_ID' });
```

#### CLI

```bash
$ apify actor abort --actor-run-id=[RUN_ID] --token=123 
```


#### UNIX equivalent

```bash
# Terminate a program
$ kill <pid>
```

### Live view web server

An actor can launch an HTTP web server that is exposed to the outer world.
This enables actors to provide a custom HTTP API to integrate with other systems,
to provide a web application for human users, to show actor run details, diagnostics, charts,
or to run an arbitrary web app.

On Apify platform, the port on which the actor can launch the public web server,
is specified by the `ACTOR_WEB_SERVER_PORT` environment variable.
The web server is then exposed to the public internet on a URL identified 
by the `ACTOR_WEB_SERVER_URL`, for example `https://hard-to-guess-identifier.runs.apify.net`.

#### Node.js

```js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(process.env.ACTOR_WEB_SERVER_PORT, () => {
  console.log(`Example live view web server running at ${process.env.ACTOR_WEB_SERVER_URL}`)
})
```


### Migration to another server

TODO...


## Actor definition files

The actor system uses several special files that define actor metadata, documentation,
instructions how to build and run it, input and output schema, etc.

**These files MUST be stored in the `.actor` directory placed in actor's top-level directory.
The entire `.actor` directory should be added to the source control.**
The only required files are [Actor file](#actor-file) and [Dockerfile](#dockerfile),
all other files are optional.

The actor definition files are used by the CLI (e.g. by `apify push` and `apify run` commands),
as well as when building actors on the Apify platform.
The motivation to place the files into a separate directory
is to keep the source code repository tidy and to prevent interactions with other source files,
in particular when creating an actor from pre-existing software repositories.


### Actor file

This is the main definition file of the actor in JSON format,
and it always must be present at `.actor/actor.json`.
This file contains references to all other necessary files.

For details, see the [Actor file](./pages/ACTOR.md) page.


### Dockerfile

This file contains instructions for the system how to build the actor's
Docker image and how to run it.
Actors are started by running their Docker image,
both locally using the `apify run` command,
as well as on the Apify platform.

The Dockerfile is referenced from the [Actor file](./pages/ACTOR.md) using the `dockerfile`
directive, and typically stored at `.actor/Dockerfile`.
Note that paths in Dockerfile are ALWAYS specified relative to the Dockerfile's location.
Learn more in the official [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).


### README

The README file contains actor documentation written
in [Markdown](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
format.
It is used to generate actor's public web page on Apify,
and it should contain great explanation what the actor does and how to use it.

The README file is referenced from the [Actor file](./pages/ACTOR.md) using the `readme`
directive, and typically stored at `.actor/README.md`.

Good documentation makes good actors!
[Learn more](https://docs.apify.com/actors/publishing/seo-and-promotion) how to write great SEO-optimized READMEs.


### Schema files

The structure of actor's [input and output](#input-and-output) can be optionally
dictated by the input and output schema files.
These files list properties accepted by actor on input, and properties that the actor produces on output,
respectively.
The input and output schema files are used to render a user interface
to make it easy to run the actor manually,
to generate API documentation, render the view of actor's output,
validate the input,
and to enable connecting actor outputs to input of another actor for rich workflows. 

The input and output schema is defined by two JSON files that are linked 
from the [Actor file](#actor-file):

- [Input schema file](./pages/INPUT_SCHEMA.md)
- [Output schema file](./pages/OUTPUT_SCHEMA.md)

Both input and output schema files can additionally reference schema files 
for specific storages:

- [Dataset schema file](./pages/DATASET_SCHEMA.md)
- [Key-value store schema file](./pages/KEY_VALUE_STORE_SCHEMA.md)
- [Request queue schema file](./pages/REQUEST_QUEUE_SCHEMA.md)

These storage schemas are used to ensure that stored objects or files 
fulfil specific criteria, their fields have certain types, etc.
On Apify platform, the schemas can be applied to the storages directly,
without actors.

Note that all the storage schemas are weak, in a sense that if the schema doesn't define a property,
such property can be added to the storage and have an arbitrary type.
Only properties explicitly mentioned by the schema
are validated. This is an important feature which allows extensibility.
For example, a data deduplication actor might require on input datasets
that have an `uuid: String` field in objects, but it does not care about other fields.


### Backward compatibility

If the `.actor/actor.json` file is missing,
the system falls back to the legacy mode,
and looks for `apify.json`, `Dockerfile`, `README.md` and `INPUT_SCHEMA.json`
files in the actor's top-level directory instead.
This behavior might be deprecated in the future.

## Development

TODO (@jancurn): Write a high-level overview how to build new actors. Provide links 
how to build directly on Apify+screenshots.

### Local development

**Status: Not implemented yet.**

TODO: Explain basic workflow with "apify" - create, run, push etc. Move the full local support for actors
 to ideas (see https://github.com/apify/actor-specs/pull/7/files#r794681016 )

Actors can be developed and run locally. To support running other actors, we need to define mapping
of `username/actor` to local or remote git/https directories with `.actor` sub-directory,
which is then used to launch actors specified e.g. by `Apify.call('bob/some-actor')'`.
TODO: Maybe using environment variable with the mapping?

`apify run` - starts the actor using Dockerfile
referenced from `.actor/actor.json` or Dockerfile in the actor top-level directory
(if the first is not present)


### Deployment to Apify platform

`apify push` - uses info from `.actor/actor.json`
New flags:
- `--force-title` and `--force-description`
- `--target` to specify where to deploy. See `.actor/actor.json` for details.
- 
....

### Repackaging existing software as actors

Just add `.actor` directory to an existing source code repo.
Use `apify actor` command in the Dockerfile's `RUN` instruction
to set up and run the actor.

TODO: Explain more, show example


### Continuous integration and delivery

TODO: Mention CI/CD, e.g. how to integrate with GiHub etc.

## Sharing & Community

TODO: Motivation - why building on Apify is easier than building your own SaaS


### Shared actors

For example:

```
https://apify.com/jancurn/some-scraper
```



## TODOs (@jancurn)

- Add more pictures, e.g. screenshots from Apify Store, Input UI, etc.
- Maybe add comparison with other systems, like Lambda, Modal, Replit, ECS etc. in terms of developer experience 
  - Maybe mention these in specific points,
- Review external links and consider replacing them with local links

