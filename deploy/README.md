# Teddy hosting boundary

The website should be deployed as a separate static module. It is not Teddy's chat surface and receives no access to companion memory, model credentials, attestation keys, work orders, or loopback APIs.

Recommended custody:

```text
/var/lib/qwos/sites/quietwire/
├── releases/<release-id>/
├── current -> releases/<release-id>/public
└── provenance/
```

Serve only the `current` symlink read-only. Activate a new release atomically after build checks, manifest verification, and explicit approval.

Begin on `teddy.quietwire.ai`. Preserve the existing Google Sites deployment until the new origin, TLS, DNS, email records, monitoring, backup, and rollback path have been verified.
