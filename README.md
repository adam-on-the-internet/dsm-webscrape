# DSM Webscrape

This application checks the City of Des Moines website for certain updates,
such as News, Calendar Events, and Council Meetings.
This allows the public to be quickly informed when the City publishes 
or modifies information.

This is written in Python and runs automatically on a timer with GitHub Actions. 
An Express REST API is used to access related data.
An Angular app is available to display the updates submitted to the REST API.

Note: This application is an operational work in progress.
Not all elements may work as they should, but the application itself is able to run stably.

## Helpful Links

- [GitHub Repository](https://github.com/adam-on-the-internet/dsm-webscrape)
- [Check the updates](https://www.dsmpeoplestownhall.com/#/dsm-updates)
- [trigger the action](https://github.com/adam-on-the-internet/dsm-webscrape/actions/workflows/scrape.yml)
