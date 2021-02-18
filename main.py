import click
import requests
import json
from decouple import config

__author__ = "Krisztián Gyula Tóth"

REGISTRY_URL = config('REGISTRY_URL')


@click.group()
def main():
    """
    Simple CLI for querying remote Docker registry by Krisztián Gyula Tóth
    """
    pass


@main.command()
@click.option('-d', '--digest', help="Image digest")
@click.argument('repository')
def find_tags(digest, repository):
    """
    List tags that point at a specific digest.
    We need to list all tags in the repository, and download all referenced manifests to figure out which ones have that digest too.
    """

    fetch_all_tags_url_format = '/v2/{}/tags/list'
    response = requests.get(
        REGISTRY_URL + fetch_all_tags_url_format.format(repository))

    data = response.json()
    all_tags = data['tags']

    digest_by_tag = {}
    fetch_mainfest_url_format = '/v2/{}/manifests/{}'
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

    for tag in all_tags:
        response = requests.get(
            REGISTRY_URL + fetch_mainfest_url_format.format(repository, tag), headers=headers)
        data = response.json()
        digest_by_tag[tag] = data.get('config', {}).get('digest')


    matchingTags = list({ key for (key,value) in digest_by_tag.items() if value == digest})

    result = {
        'digest': digest,
        'repository': repository,
        'tags': matchingTags
    }

    click.echo(json.dumps(result, sort_keys = True, indent = 2))


if __name__ == "__main__":
    main()
