# Notes

## Validation behavior

`RV` validates:

- support type/content
- probability values and tolerance
- support/probability compatibility
- tail flags
- `is_pmf` flag type

When validation fails during construction, errors are aggregated into one `ValueError`.

## Setter behavior

Property setters log validation errors and keep prior valid values.

## Platform behavior

On Windows, plots attempt to maximize the figure window before layout tightening.

## Existing generated docs

This repository also contains pre-generated HTML docs under `help/`.
Those are separate from the MkDocs site configured by `mkdocs.yml`.
