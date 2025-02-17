
# Differences between the CROSS codebase submitted to NIST and the one in liboqs

The coding conventions required by [liboqs][liboqs_conventions] and [PQClean][pqclean_conventions] differ in some aspects from the [NIST call][nist_conventions]. Below is a list of changes made to CROSS to make it library-ready, starting from the [NIST submission package][cross_resources].

## Directory Structure

The Reference Implementation of CROSS is placed in the `clean` directory, and the Optimized Implementation in the `avx2` directory. Source and header files live in the same directory instead of being separated into `include` and `lib`.

## Parameter Sets

A parameter set is an instance of the algorithm defined by all its possible parameters. CROSS has two variants (RSDP and RSDPG), three security levels (128, 192, and 256 bits), and three optimization targets (balanced, fast, small). In total, there are 18 possible parameter sets (2×3×3). Each parameter set contains two implementations: `clean` and `avx2`. The script `generate.py` creates the 18 directories and substitutes the appropriate parameters using a placeholder mechanism.

## Namespacing

PQClean requires all exported symbols to be prefixed with a string corresponding to the parameter set and implementation. For example, the function `crypto_sign` becomes `PQCLEAN_CROSSRSDP128BALANCED_CLEAN_crypto_sign`. We handle this namespacing with a new file: `namespace.h`. The only exception is `api.h`, which PQClean requires not to include any external files. Here, `generate.py` will namespace symbols explicitly.

## Parameter File

The file `set.h` is added to distinguish parameter sets. It uses `#define` statements to specify the problem type, security category, and optimization target. For example:
```
#define RSDP 1
#define CATEGORY_1 1
#define BALANCED 1
```
These definitions were handled externally in the NIST submission package, such as in `Additional_Implementations/Benchmarking/CMakeLists.txt`.

## Dead Code Removal

CROSS' source code makes heavy use of `#ifdef` and similar preprocessor macros, for example, to assign different values to constants in `parameters.h` based on the security level. This behavior is prohibited in PQClean. Therefore, when generating parameter sets, `generate.py` removes lines of code corresponding to dead branches of an `#if`. This is achieved using the `unifdef` utility.

## Detached Signatures

Two additional functions, `crypto_sign_signature` and `crypto_sign_verify`, are declared in `api.h` and defined in `sign.c`. They compute signing and verification using detached signatures (where the signature is returned separately from the message instead of being appended to it).

## Deterministic CSPRNG for Testing

The definition of `randombytes` is removed from `csprng_hash.h`. This function is called during key generation and signing to obtain salts and seeds. The libraries define an identical function, common to all algorithms, to ensure reproducibility of results like KAT.

## No Variable-Length Arrays

A few functions in CROSS use VLAs, but since the array size is always known at compile time, we place a `#define` before the function to specify the array size instead of using a normal variable definition.

:warning: Functions `csprng_initialize_x3` and `csprng_randombytes_x3` allocate memory dynamically for an array that is never actually used. This is the fourth input/output to 4-way Keccak when only the first three are needed. Here, we replace the VLA with a `malloc` call (`OQS_MEM_malloc` in liboqs).

## AVX2 Flags

In the NIST codebase, a series of preprocessor macros in `architecture_detect.h` check at compile time whether the AVX2-optimized implementation of CROSS is being compiled on a platform that actually supports AVX2 intrinsics. In liboqs, we skip these checks and assume the platform is compatible.

## SHAKE

A portable version of SHAKE is included in CROSS for hashing and pseudorandom number generation. We replace it with the one in `liboqs/src/common/sha3`. One relevant difference is that liboqs' implementation uses dynamic memory allocation, so we need to add calls to `xof_shake_release` to free memory after each use of SHAKE.

## Makefiles

A `Makefile` and a `Makefile.Microsoft_nmake` are added to specify the source files and compilation flags for CROSS.

## Metadata

Each parameter set requires its own `META.yml` file to specify metadata about CROSS, such as authors, available implementations, and KAT.

## Astyle

TODO

## Other

TODO


<!-- sources -->

[nist_conventions]: https://csrc.nist.gov/Projects/pqc-dig-sig/standardization/call-for-proposals
[liboqs_conventions]: https://github.com/open-quantum-safe/liboqs/wiki/Coding-conventions
[pqclean_conventions]: https://github.com/PQClean/PQClean/blob/master/CONTRIBUTING.md
[cross_resources]: https://www.cross-crypto.com/nist-submission.html
[repo_PQClean]: https://github.com/PQClean/PQClean/
[repo_liboqs]: https://github.com/open-quantum-safe/liboqs
[repo_oqs-provider]: https://github.com/open-quantum-safe/oqs-provider
[repo_oqs-demos]: https://github.com/open-quantum-safe/oqs-demos
