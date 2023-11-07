# vectorizer-ai

Python SDK for [vectorizer.ai](https://vectorizer.ai/).

## What is it?

Convert JPEG and PNG bitmaps to SVG vectors.

## Install

```bash
$ pip install vectorizer-ai
```

## Usage

### Basic

```python
from vectorizer_ai import VectorizerAI

client = VectorizerAI(
    api_id="VECTORIZER-AI-API-ID",
    api_secret="VECTORIZER-AI-API-SECRET",
    mode="production"
)
svg = client.vectorize("/path/to/input.png")

svg.save("/path/to/output.svg")
```

You can also use:

```python
client.vectorize(image_base64="base64encodedimage==")

# or

client.vectorize(image_url="https://imageurl.com/test.png")
```

### Advanced

```python
client.vectorize(
    image_path="/path/to/image",
    input_max_pixels=100,
    processing_max_colors=256
    ...
)
```

Reference: [https://vectorizer.ai/api](https://vectorizer.ai/api#:~:text=Options%20Documentation.-,Parameters,-The%20input%20image)

All parameters described in the API spec above replace period (`.`) with underscore (`_`). For example, if the parameter is `input.max_pixels`, the SDK will use `input_max_pixels`.

## Contributing

Feel free to open a PR for any changes!

## Testing

```bash
$ python -m unittest discover -s tests -p 'test_*.py'
```

Made with ❤️ by [@mitchbregs](https://twitter.com/mitchbregs)
