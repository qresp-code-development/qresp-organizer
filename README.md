# Qresp organizer
Qresp | Organizer is a software to configure the parent folder containing a collection of folders where each paper content is organized and stored.
It can also be used to upload content to Zenodo

## Documentation

**Qresp organizer** is available at [Qresp Organizer](http://qresp.org/QrespOrganizerDownload.html)


## Development 
The **Qresp Organizer** development is hosted on [GitHub](https://github.com/qresp-code-development/qresp-organizer), and licensed under the open-source GPLv3 license. See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and [AUTHORS.md](AUTHORS.md) for more information.

## Installation

You need python > 3 to install qresp organizer

```bash
$ git clone https://github.com/qresp-code-development/qresp-organizer.git
$ cd qresp-organizer
$ python setup.py install --user
```

## Usage

Qresp organizer aids in 

a) Uploading your paper content to [Zenodo](https://www.zenodo.org/). To upload your paper,
* Login to [Zenodo](https://www.zenodo.org/login/?next=%2F) or [Zenodo sandbox](https://sandbox.zenodo.org/login/?next=%2F).
* Generate new token at [applications page](https://www.zenodo.org/account/settings/applications/). Create a personal token with all permissions checked and copy the token id. Use [sandbox applications page](https://www.ssandbox.zenodo.org/account/settings/applications/) alternatively.
* Run
```bash
$ qresp_config zenodo upload <folder_name> <token> 
```
* For sandbox,
```bash
$ qresp_config zenodo upload <folder_name> <token> --sandbox 
```
* Follow the prompts to upload content to zenodo.

Or

b) Creating a folder/paper collection in a centralized server to host datasets for many users
```bash
$ qresp_config collection <paper_collection> [<path>]
```
* Follow the prompts to create a qresp.ini file which will be accessed by curator to view user priveleges. 

Or

c) Create a project skeleton for qresp within a paper collection
```bash
$ cd <paper_collection> 
$ qresp_config paper <paper_name> [<path>] 
``` 
* This will enable git as a service for the user to version control their data.





