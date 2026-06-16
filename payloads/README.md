# checkm8 payloads

Binary exploit stages from upstream [ipwndfu](https://github.com/axi0mX/ipwndfu) will live here after licensing review.

## Planned layout

```
payloads/
├── a5/
├── a6/
├── ...
└── README.md   (this file)
```

## Phase 2 status

Phase 2 adds **routing and module stubs** only. Payload blobs are not vendored in this repository yet.

Options for phase 2.1:

1. Git submodule pointing at axi0mX/ipwndfu payload paths
2. Git LFS for per-SoC `.bin` files
3. Generate from upstream assembly during build (document provenance)

Do not commit Apple-signed or copyrighted firmware images here.
