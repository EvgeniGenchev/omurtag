#!/bin/bash

export XDG_CONFIG_HOME=/tmp/omurtag_config
export XDG_DATA_HOME=/tmp/omurtag_data

FASTAPI_URL="github:EvgeniGenchev/fastapi_frontend_omurtag_template"
FASTAPI_BRANCH="docker"
NEOVIM_TMPL="/home/gena/Workspace/Hobby/neovim_plugin_omurtag_template"

PASS=0
FAIL=0

ok()   { echo "  PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

assert_path_exists()     { [ -e "$2" ]  && ok "$1" || fail "$1 (missing: $2)"; }
assert_path_not_exists() { [ ! -e "$2" ] && ok "$1" || fail "$1 (exists: $2)"; }
assert_contains()        { echo "$3" | grep -q "$2" && ok "$1" || fail "$1 (expected '$2' in output)"; }

assert_no_placeholder() {
    local found
    found=$(grep -rl '<\*project\*>' "$2" 2>/dev/null)
    found+=$(find "$2" -name '*<*project*>*' 2>/dev/null)
    [ -z "$found" ] && ok "$1" || fail "$1 (leftover: $found)"
}

setup() {
    rm -rf /tmp/omurtag_config /tmp/omurtag_data /tmp/omurtag_test_*
    mkdir -p /tmp/omurtag_config/omurtag
    cat > /tmp/omurtag_config/omurtag/config.py <<EOF
templates = [
    "$FASTAPI_URL",
]
EOF
}

# --- add: local template with <*project*> in file contents, filename, dirname ---
test_add() {
    echo "--- add ---"
    mkdir -p "/tmp/omurtag_test_tmpl/<*project*>_module"
    echo 'name = "<*project*>"'    > "/tmp/omurtag_test_tmpl/<*project*>.cfg"
    echo 'def main(): pass'        > "/tmp/omurtag_test_tmpl/<*project*>_module/<*project*>.py"

    omurtag add /tmp/omurtag_test_tmpl
    assert_path_exists "add: template in data dir" "$XDG_DATA_HOME/omurtag/omurtag_test_tmpl"
}

# --- list ---
test_list() {
    echo "--- list ---"
    out=$(omurtag list)
    assert_contains "list: local template visible" "omurtag_test_tmpl" "$out"
}

# --- create: verify placeholder replaced in file contents, filenames, dirnames ---
test_create_local() {
    echo "--- create (local template) ---"
    pname="omurtag_test_myapp"

    omurtag create /tmp/$pname -t omurtag_test_tmpl

    assert_path_exists     "create: project dir"                "/tmp/$pname"
    assert_path_exists     "create: .cfg filename replaced"     "/tmp/$pname/$pname.cfg"
    assert_path_not_exists "create: original .cfg gone"         "/tmp/$pname/<*project*>.cfg"
    assert_path_exists     "create: subdir renamed"             "/tmp/$pname/${pname}_module"
    assert_path_not_exists "create: original subdir gone"       "/tmp/$pname/<*project*>_module"
    assert_path_exists     "create: file in renamed subdir"     "/tmp/$pname/${pname}_module/$pname.py"
    assert_no_placeholder  "create: no leftover placeholders"   "/tmp/$pname"
}

# --- remove ---
test_remove() {
    echo "--- remove ---"
    omurtag remove omurtag_test_tmpl
    assert_path_not_exists "remove: template gone" "$XDG_DATA_HOME/omurtag/omurtag_test_tmpl"
    out=$(omurtag list 2>&1)
    if echo "$out" | grep -q "omurtag_test_tmpl"; then
        fail "remove: template still in list"
    else
        ok "remove: template not in list"
    fi
}

# --- pull (default branch) ---
test_pull() {
    echo "--- pull (no branch) ---"
    out=$(omurtag pull "$FASTAPI_URL" 2>&1)
    assert_contains        "pull: cloned successfully"      "Cloned" "$out"
    assert_path_exists     "pull: template in data dir"     "$XDG_DATA_HOME/omurtag/fastapi_frontend"
}

# --- pull with --branch (remove first to skip confirm) ---
test_pull_branch() {
    echo "--- pull --branch $FASTAPI_BRANCH ---"
    omurtag remove fastapi_frontend
    out=$(omurtag pull --branch "$FASTAPI_BRANCH" "$FASTAPI_URL" 2>&1)
    assert_contains    "pull --branch: cloned"          "Cloned" "$out"
    assert_path_exists "pull --branch: template present" "$XDG_DATA_HOME/omurtag/fastapi_frontend"
    # verify checked out branch
    branch=$(git -C "$XDG_DATA_HOME/omurtag/fastapi_frontend" rev-parse --abbrev-ref HEAD 2>/dev/null)
    [ "$branch" = "$FASTAPI_BRANCH" ] && ok "pull --branch: correct branch checked out" \
                                       || fail "pull --branch: expected '$FASTAPI_BRANCH', got '$branch'"
}

# --- create from pulled template (also exercises stack detection + security scan) ---
test_create_fastapi() {
    echo "--- create (fastapi template) ---"
    pname="omurtag_test_fastapi"
    out=$(omurtag create /tmp/$pname -t fastapi_frontend 2>&1)
    assert_path_exists    "create fastapi: project dir"            "/tmp/$pname"
    assert_no_placeholder "create fastapi: no leftover placeholders" "/tmp/$pname"
    assert_contains       "create fastapi: stack detected"         "Detected stacks" "$out"
    assert_contains       "create fastapi: python stack"           "python"           "$out"
}

# --- sync (updates existing template, also tests _update_template path) ---
test_sync() {
    echo "--- sync ---"
    out=$(omurtag sync 2>&1)
    assert_contains    "sync: mentions template"   "fastapi_frontend" "$out"
    assert_path_exists "sync: template present"    "$XDG_DATA_HOME/omurtag/fastapi_frontend"
}

# --- neovim plugin template: dirname and filename placeholders ---
test_neovim() {
    echo "--- neovim plugin template ---"
    omurtag add "$NEOVIM_TMPL"
    pname="omurtag_test_myplugin"
    omurtag create /tmp/$pname -t neovim_plugin_omurtag_template

    assert_path_exists     "neovim: lua/<pname>/init.lua"  "/tmp/$pname/lua/$pname/init.lua"
    assert_path_exists     "neovim: plugin/<pname>.lua"    "/tmp/$pname/plugin/$pname.lua"
    assert_path_exists     "neovim: doc/<pname>.txt"       "/tmp/$pname/doc/$pname.txt"
    assert_path_not_exists "neovim: no <*project*> dir"    "/tmp/$pname/lua/<*project*>"
    assert_no_placeholder  "neovim: no leftover placeholders" "/tmp/$pname"
}

# --- list --verbose: desc and stack shown for templates with omurtag.toml ---
test_list_verbose() {
    echo "--- list --verbose ---"
    omurtag add "$NEOVIM_TMPL"
    out=$(omurtag list --verbose 2>&1)
    assert_contains "list --verbose: neovim desc shown"  "Neovim plugin boilerplate" "$out"
    assert_contains "list --verbose: neovim stack shown" "neovim"                    "$out"
}

# --- security scan: fake python template with requests==2.19.1 (has CVE-2018-18074) ---
test_security_scan() {
    echo "--- security scan (requests==2.19.1) ---"
    omurtag add tests/fake_python_tmpl
    pname="omurtag_test_seccheck"
    out=$(omurtag create /tmp/$pname -t fake_python_tmpl 2>&1)

    assert_path_exists "security: project dir"              "/tmp/$pname"
    assert_path_exists "security: filename placeholder replaced" "/tmp/$pname/$pname.py"
    assert_contains    "security: stack detected"           "Detected stacks" "$out"
    assert_contains    "security: python stack"             "python"           "$out"
    assert_contains    "security: requests scanned"         "requests"         "$out"
    assert_contains    "security: CVE reported"             "CVE-2018-18074"   "$out"
}

# --- run ---

if ! command -v omurtag &>/dev/null; then
    echo "omurtag not found. Install with: pip install -e ."
    exit 1
fi

setup

echo "=== omurtag integration tests ==="
echo ""
test_add
test_list
test_create_local
test_remove
test_pull
test_pull_branch
test_create_fastapi
test_sync
test_neovim
test_list_verbose
test_security_scan
echo ""
echo "=== $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ] && exit 0 || exit 1
