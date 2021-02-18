# docker-registry-api-utils
Simple CLI Python app that can help you to get more out form your private remote Docker registry's APIs.

## Usage
Run command: `python main.py [OPTIONS] COMMAND [ARGS]...`

## Commands
- `find-tags <repository> -d <digest>` | List all tags that point at a specific digest.

## Example

```
$ python main.py find-tags alpine -d sha256:e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25

{
  "digest": "sha256:e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25",
  "tags": [
    "3.13.1",
    "unstable"
  ],
  "repository": "alpine"
}
```

### Docker Registry V2 API call samples
Find repositories

```
GET /v2/_catalog
Host: localhost:5000
{
    "repositories": [
        "alpine",
        "hello-world"
    ]
}
```
List tags
```
GET /v2/{{repository}}/tags/list
Host: localhost:5000
{
    "name": "alpine",
    "tags": [
        "3.13.1",
        "3.13.2",
        "latest",
        "stable",
        "unstable"
    ]
}
```
Pulling an image manifest (See the image digest at config -> digest)
```
GET /v2/alpine/manifests/unstable HTTP/1.1
Host: localhost:5000
Accept: application/vnd.docker.distribution.manifest.v2+json
{
    "schemaVersion": 2,
    "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
    "config": {
        "mediaType": "application/vnd.docker.container.image.v1+json",
        "size": 1471,
        "digest": "sha256:e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25"
    },
    "layers": [
        {
            "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
            "size": 2811321,
            "digest": "sha256:4c0d98bf9879488e0407f897d9dd4bf758555a78e39675e72b5124ccf12c2580"
        }
    ]
}
```
