# CROSS-lib-oqs
This repository hosts a patched version of the [CROSS][repo_cross] signature scheme to comply with the coding conventions of the Open Quantum Safe project. The project's main library, [liboqs][repo_liboqs], uses this repo as an "upstream" source, meaning it pulls the CROSS implementation directly from here.

Liboqs requires that each parameter set be in its own subdirectory. CROSS has 18 parameter sets: two problems (RSDP and RSDPG), three security levels (128, 192, and 256 bits), and three optimization targets (fast, balanced, small). The script [`generate.py`][script_generate] creates these 18 directories from a single codebase, it also handles namespacing and code formatting.


[&#8594; Differences with the NIST submission package][docs_diff]
\
[&#8594; Keep CROSS up to date in liboqs][docs_liboqs]

<!-- sources -->

[repo_liboqs]: https://github.com/open-quantum-safe/liboqs
[repo_cross]: https://github.com/CROSS-signature/CROSS-implementation
[script_generate]: https://github.com/CROSS-signature/CROSS-lib-oqs/blob/main/generate/generate.py
[docs_diff]: https://github.com/CROSS-signature/CROSS-lib-oqs/blob/main/docs/DIFF.md
[docs_liboqs]: https://github.com/CROSS-signature/CROSS-lib-oqs/blob/main/docs/LIBOQS.md