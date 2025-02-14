
#define __variant__ 1
#define CATEGORY___nist-level__ 1
#define __target__ 1

#if defined(SPEED)
#define NO_TREES 1
#else
#undef NO_TREES
#endif

/* liboqs-edit: when compiling avx2 just assume that Intel Instrinsics are available */
#define IMPLEMENTATION___implementation__
#if defined(IMPLEMENTATION_avx2)
#define HIGH_COMPATIBILITY_X86_64
#define HIGH_PERFORMANCE_X86_64
#endif

/* PQClean-edit: avoid VLA */
#define CSPRNG_INPUT_LENGTH (SALT_LENGTH_BYTES+SEED_LENGTH_BYTES)

/* PQClean-edit: skip asserts so that verify() always returns a value */
#define SKIP_ASSERT

/* Undefine unused macros to facilitate dead code removal using unifdef */
#undef SHA_3_LIBKECCAK
/* Variant */
#if defined(RSDP)
#undef RSDPG
#else
#undef RSDP
#endif
/* Category */
#ifndef CATEGORY_1
#undef CATEGORY_1
#endif
#ifndef CATEGORY_3
#undef CATEGORY_3
#endif
#ifndef CATEGORY_5
#undef CATEGORY_5
#endif
/* Target */
#ifndef BALANCED
#undef BALANCED
#endif
#ifndef SPEED
#undef SPEED
#endif
#ifndef SIG_SIZE
#undef SIG_SIZE
#endif
