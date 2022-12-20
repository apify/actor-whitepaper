# Request Queue Schema File

TODO: This will be added later

But in general I think that it might be useful for 2 things:
- ensuring what kind of URLs might be enqueued (certain domains or subdomains, ...)
- ensure that for example each requets has `userData.label`, i.e. schema of `userData` the same way as we enforce it for the Datasets

- Consider renaming `RequestQueue` to just `Queue` and make it more generic, and then it makes sense to have request schema
