# Security and privacy notes

This initial development build is not production-ready. The current caller-supplied `owner_id` is not an authentication mechanism and can be spoofed. Do not deploy with real personal or business analytics until authenticated sessions, server-side ownership checks, CSRF/session protections as appropriate, secret rotation, HTTPS, strict CORS, rate limiting, deletion workflows, consent management and retention policies are implemented and tested.

The event schema intentionally avoids collecting form contents, passwords, names, email addresses or full IP addresses. Page paths can themselves contain sensitive query parameters; a production tracker must strip query strings and fragments before sending. Obtain appropriate consent and comply with applicable law and site policies.
