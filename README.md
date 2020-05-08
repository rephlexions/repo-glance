# repo-lens
Is a Python script to get details about a repository without cloning
it. All the information are retrieved using the [GitHub API](http://developer.github.com/v3/repos/).

<img src="https://i.postimg.cc/L85j4KZn/Annotation-2020-05-08-172622.png" 
    height="500" style="display: block;margin-left: auto;margin-right: auto;">

⚠ API requests made by this module aren't using basic authentication or
OAuth. The rate limit allows for up to 60 requests per hour. Unauthenticated requests are associated with the originating IP address, and not the user making requests.


## Information Provided

1. Basic information about the repository.
   - Repository Name
   - Default Branch
   - Repository Size
   - Repository License
   - Repository Description

2. Languages used in the repository.

3. Repository Statistics.
   - Forks
   - Watchers
   - Open Issues
   - Total Stars

4. URL's of the repository.
   - GIT URL
   - SSH URL
   - SVN URL
   - Clone URL

## Installation

To install this script so that it is accessible via Python from anywhere, copy
the script into a directory of your choice, and then add that directory to your
`PYTHONPATH`

## Usage

```
python -m repo-lens
```

## License

MIT ©
