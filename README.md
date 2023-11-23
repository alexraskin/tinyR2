# tinyR2

<a href="https://gyazo.com/1479e9898faff896c797eafad237a39b"><img src="https://i.gyazo.com/1479e9898faff896c797eafad237a39b.png" alt="Image from Gyazo" width="250"/></a>

TinyR2 is a multi threaded script that compresses images using the [TinyPNG](https://tinypng.com/) API and then uploads them to [CloudflareR2](https://developers.cloudflare.com/r2/)

## Usage

Create a `.env` file with the following variables:

```bash
TINYFY_TOKEN=
PREFIX=
BUCKET_NAME=
R2_ENDPOINT_URL=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
```

Add the images you want to compress to the `images` folder and then run:

This will install the dependencies and run the script.

```bash
./run.sh
```

If you want to change the amount of threads, update the `config.py` file with the desired amount.

## Contributing

This is a personal project, but feel free to fork it and make it your own.

## License

[MIT](https://choosealicense.com/licenses/mit/)
