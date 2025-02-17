# Keep CROSS up to date in liboqs

When the codebase of CROSS changes we need to port the modifications to liboqs, this is a step-by-step guide on how to do it.

- Clone this repository
    ```
    git clone https://github.com/CROSS-signature/CROSS-lib-oqs
    ```

- Apply the changes to the files in the `clean` and `avx2` directories

- If necessary, edit also the metadata in file `META.yml`

- Install the `unifdef` utility, used to remove dead code. On a Debian-based system it's as simple as:

    ```
    sudo apt install unifdef
    ```

- Generate code for the 18 variants:
    ```
    cd generate
    python3 generate.py
    ```

- Commit everything and push to GitHub

- Copy the commit SHA
    ```
    git log -1 --format=%H
    ```

- All the changes are now part of the "upstream" repository, it's time to deal with liboqs. Move to a fresh directory to follow the next steps

- Fork liboqs and create a new branch, change the branch name to something significant (e.g. `CROSS-fix-endianness-issue`):
    ```
    cd liboqs
    git checkout -b CROSS-fix
    ```

- Create a virtual environment for Python and activate it:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r ./scripts/copy_from_upstream/requirements.txt
    echo "*" > .venv/.gitignore
    ```

- Replace the commit SHA in the configuration file
\
`scripts/copy_from_upstream/copy_from_upstream.yml`
\
with the one copied before:
    ```
    name: upcross
    ...
    git_branch: master
    git_commit: a880bb3561f68d0012bf82eff0eb557bf9ae3df3 # <- replace this
    ```

- Import the "upstream" code:
    ```
    export LIBOQS_DIR=$(pwd)
    cd ./scripts/copy_from_upstream
    rm -rf repos
    # rm -rf ../../src/sig/cross
    python3 copy_from_upstream.py copy
    ```

- Build and test liboqs:
    ```
    cd $LIBOQS_DIR
    rm -rf build; mkdir build && cd build; cmake -GNinja ..; ninja; cd ..
    ./build/tests/speed_sig -f
    ```

- Some files in liboqs might also need attention when modifying CROSS:
    - Documentation file, stores metadata about CROSS
    \
    `liboqs/docs/algorithms/sig/cross.yml`
    - Valgrind suppression file, ensures any suspect non-constant-time behaviour in CROSS is documented
    \
    `liboqs/tests/constant_time/sig/passes/cross`
    - Signature test, CROSS variants that use a large amount of stack are prevented from running in threads
    \
    `liboqs/tests/test_sig.c`
    - Zephyr configuration file, CROSS variants that use a large amount of stack are disabled in Zephyr
    \
    `liboqs/zephyr/CMakeLists.txt`
    - Lists of code owners and contributors
    \
    `liboqs/.github/CODEOWNERS`
    \
    `liboqs/CONTRIBUTING.md`

- Commit everything and push to GitHub. Make sure to sign every commit to liboqs with your name, by adding a line like this to the commit message:
    ```
    Signed-off-by: Alice alice@example.com
    ```

- Go to your liboqs branch on `github.com` and you will be pompted to open a Pull Request to liboqs

<br/><br/>
<br/><br/>

```
KNOWN BUG:

The script copy_from_upstream.py in liboqs will not update files if they don't already exist, a solution is to add this to the "generator" function:

if not os.path.exists(os.path.join(os.environ['LIBOQS_DIR'], destination_file_path)):
    open(os.path.join(os.environ['LIBOQS_DIR'], destination_file_path), 'a').close()

```
