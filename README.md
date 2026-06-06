# Signal-WA-Bridge-Builder

This repository contains a placeholder Matrix bot built on mautrix AppService.

## Supported Matrix message commands

Send these as Matrix text messages (with or without a `!` prefix):

- `help`
- `create_bridged_pair`
- `bridge`
- `debug_info`

Each command currently replies with:

`Placeholder: '<command>' command is not implemented yet.`

## Docker usage

Set required environment variables:

- `MATRIX_HOMESERVER_URL`
- `MATRIX_HOMESERVER_DOMAIN`
- `MATRIX_AS_TOKEN`
- `MATRIX_HS_TOKEN`
- `MATRIX_BOT_LOCALPART`
- `MATRIX_APP_SERVICE_ID`

Then run:

```bash
docker compose up --build
```
