# OpenJEV support

This fork of [jinwonkim93/vllm-verifier](https://github.com/jinwonkim93/vllm-verifier)
adds **optional** support for [OpenJEV](https://openjev.sh) alongside the existing
TypeSafe integration. OpenJEV is a free community gateway to the same Jev model
built by [TypeSafe](https://typesafe.ai). TypeSafe remains the default; anyone
with a TypeSafe key sees zero behaviour change.

## What was added

- `src/vllm_verifier/service.py` — `openjev` accepted as a model alias in
  `check_model`, next to `jev-latest`.
- `src/vllm_verifier/decision/service.py` — `openjev` accepted as a model alias
  in `DirectDecisionService.evaluate`.
- `src/vllm_verifier/engine/core.py` — `openjev` accepted in the native engine
  model guard.
- `src/vllm_verifier/app.py` — `openjev` listed in the `/v1/models` response.
- `examples/openjev.py` — new example calling the OpenJEV public API
  (`https://api.openjev.sh/v1/systemone`, model `openjev`, key `OPENJEV_API_KEY`)
  with the existing TypeSafe SDK pointed at OpenJEV.
- `.env.example` — documents the optional `OPENJEV_API_KEY` and `JEV_PROVIDER`
  environment variables.
- `README.md` — short OpenJEV note after the intro and a note on the `openjev`
  alias next to the `jev-latest` documentation.

No TypeSafe code, default or documentation was renamed, removed or re-defaulted.

## Provider selection rule

1. An explicit base URL / `JEV_PROVIDER=openjev` wins.
2. Otherwise, if a TypeSafe key is set → TypeSafe, exactly as before (default
   unchanged).
3. Otherwise, if only `OPENJEV_API_KEY` is set → OpenJEV.

The same System One request/response contract applies to both:

| | TypeSafe direct | OpenJEV |
|---|---|---|
| Endpoint | `https://api.typesafe.ai/v1/systemone` | `https://api.openjev.sh/v1/systemone` |
| Model | `jev-latest` | `openjev` |
| Key | TypeSafe API key | `OPENJEV_API_KEY` |
| Overload | 529 | 503 (also 429) |

The verifier's retryable-status handling (`429`, `503`, `529` in
`src/vllm_verifier/backend.py`) already covers the OpenJEV overload statuses.

## Configuration

Set `OPENJEV_API_KEY` (from https://openjev.sh/dashboard) to use OpenJEV as a
client, or `JEV_PROVIDER=openjev` to prefer it explicitly. See `.env.example`.

## How it was verified

- A live `POST https://api.openjev.sh/v1/systemone` request with model `openjev`,
  state `ping`, and one noul question returned HTTP 200.
- `grep` confirmed no hardcoded `api.typesafe.ai` default was introduced; the
  only `typesafe.ai` references are pre-existing documentation links in
  `docs/sources.md` and `docs/benchmarks/`, which are unchanged.
- No repository code was executed during this port (read/edit only).

## Upstream

Original project: https://github.com/jinwonkim93/vllm-verifier by @jinwonkim93
(Apache-2.0).
