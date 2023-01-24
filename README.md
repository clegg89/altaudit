# Altaudit

A group of packages aimed at gathering and storing information for alts in World of Warcraft

Currently undergoing a large refactoring aimed at breaking the code into more reusable pieces. There are a few different plans for this:

1. Separate the model and server (formerly the `altaudit` directory) into separate packages. This allows the re-use of just the model layer by future packages.
2. Change the server component to instead store all information in the database (rather than output to CSV). This should function as a python library, where dependencies such as the database, blizzard tokens, etc. are passed in on construction. The object created can then run "update" to update all characters in the database by querying blizzard's API
3. Scripts to run the API on a regular basis (not packaged), along with Dockerfiles containing the scripts.
4. Eventually we may create a more friendly frontend than the google sheets bullshit. I'm thinking we could use some sort of python web framework. This is where separating the "model" aspect comes in handy.

I also plan to create a local repository on my home network using something like [devpi](https://devpi.net).
