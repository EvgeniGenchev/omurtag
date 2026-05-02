/* global React */

// Docs content as data so search + scroll-spy can introspect it.
window.DOCS_CONTENT = [
  {
    id: "introduction",
    group: "Getting started",
    title: "Introduction",
    body: (toolName) => ({
      lead: `${toolName} is a small, focused command-line tool. It does one thing well and stays out of your way.`,
      paragraphs: [
        `This page is the long-form introduction. Use the sidebar to jump between sections; links highlight as you scroll, and you can press / to search.`,
        `Everything on this site is meant to be skimmable. If you've used a Unix tool before, the conventions should feel familiar.`,
      ],
    }),
  },
  {
    id: "tldr",
    group: "Getting started",
    title: "TL;DR",
    body: (toolName) => ({
      paragraphs: [
        `One command to install, one command to run.`,
      ],
      code: { lang: "bash", text: `# install\ncurl -fsSL https://evgeni-genchev.com/omurtag/install.sh | sh\n\n# run\n${toolName} --help` },
      list: [
        `Configuration is optional. Sensible defaults out of the box.`,
      ],
    }),
  },
  {
    id: "creating-templates",
    group: "Templates",
    title: "Creating templates",
    body: (toolName) => ({
      paragraphs: [
        `Any folder can be a template. Use \`${toolName} add <folder>\` to register a local one. To host it so others can pull it, name the repo with a \`_omurtag_template\` suffix. That's what ${toolName} checks when validating a pull URL. For local templates added with \`add\`, naming doesn't matter.`,
        `Placeholders use the \`<*name*>\` syntax. On \`${toolName} create\`, every placeholder is replaced in **file contents**, **filenames**, and **directory names**. \`<*project*>\` is always set to the project name. Any other placeholders you define are prompted for interactively at create time.`,
        `A **security audit** runs automatically on every \`create\`. ${toolName} detects the stack from marker files (\`pyproject.toml\`, \`package.json\`, \`Cargo.toml\`, etc.) and checks each direct dependency for known CVEs via [deps.dev](https://deps.dev). Opt in to transitive scanning with \`transitive_deps = True\` in config.`,
        `An optional \`omurtag.toml\` at the template root provides metadata shown in \`${toolName} list\`. It is never copied into created projects. Fields: \`name\`, \`description\`, \`stack\`, \`author\`.`,
        `A community-maintained list of available templates is kept up to date at [/templates.json](/omurtag/templates.json).`,
      ],
      code: { lang: "bash", text: `# folder structure example\nmy_service_omurtag_template/\n  <*project*>/\n    main.py\n  <*project*>_tests/\n    test_main.py\n  pyproject.toml       # triggers python security scan\n  omurtag.toml         # optional metadata\n\n# omurtag.toml\n[template]\nname        = "my-service"\ndescription = "Minimal Python service"\nstack       = ["python"]\nauthor      = "you"` },
    }),
  },
  {
    id: "usage",
    group: "Reference",
    title: "Usage",
    body: (toolName) => ({
      paragraphs: [
        `${toolName} is a tool that helps you create projects from templates.`,
      ],
      code: { lang: "bash", text: `${toolName} {add,remove,create,list,pull,sync,search}\n\n  add      Add a local folder as a template\n  remove   Remove a template by name\n  create   Generate a project from a template\n  list     List templates with stack info\n  pull     Pull a template from a git repo\n  sync     Download/update all templates from config\n  search   Browse and pull from the community template list` },
    }),
  },
  {
    id: "configuration",
    group: "Reference",
    title: "Configuration",
    body: (toolName) => ({
      paragraphs: [
        `Configuration lives in ${"$"}XDG_CONFIG_HOME/${toolName}/${"`"}config.py${"`"} or ${"~"}/.${toolName}/${"`"}config.py${"`"}.`,
        `The ${"`"}templates${"`"} list is used by ${"`"}${toolName} sync${"`"} to download and update all your templates in one command. Supports GitHub, GitLab, Codeberg, or any git host.`,
      ],
      code: { lang: "bash", text: `# config.py\ntemplates = [\n    "github:EvgeniGenchev/fastapi_frontend_omurtag_template",\n    "gitlab:user/my_project_omurtag_template",\n    "codeberg.org:user/tool_omurtag_template",\n    "https://codeberg.org/user/repo_omurtag_template.git",\n]\n\n# optional\ntransitive_deps = False  # scan transitive deps on create (slower)\nshow_desc  = True        # show description in list\nshow_stack = True        # show stack in list` },
    }),
  },
  {
    id: "examples",
    group: "Reference",
    title: "Examples",
    body: (toolName) => ({
      paragraphs: [
        `Common workflows.`,
      ],
      code: { lang: "bash", text: `# browse community templates and pull interactively\n${toolName} search\n\n# pull a template from GitHub\n${toolName} pull github:EvgeniGenchev/fastapi_frontend_omurtag_template\n\n# pull a specific branch\n${toolName} pull github:user/repo_omurtag_template --branch dev\n\n# list available templates\n${toolName} list\n${toolName} list --verbose\n\n# create a project (interactive if no args)\n${toolName} create\n${toolName} create ~/projects/myapp --type fastapi_frontend\n\n# add a local folder as a template\n${toolName} add ~/my_template_folder\n\n# remove a template\n${toolName} remove fastapi_frontend\n\n# sync all templates from config\n${toolName} sync` },
    }),
  },
  {
    id: "faq",
    group: "Reference",
    title: "FAQ",
    body: (toolName) => ({
      paragraphs: [
        `**How does the security audit work?** On every \`create\`, ${toolName} detects marker files in the new project (\`pyproject.toml\`, \`package.json\`, \`Cargo.toml\`, etc.) to identify the stack, then reads direct dependencies and queries [deps.dev](https://deps.dev) for known advisories. Each vulnerable package is printed with its CVE ID and CVSS score. Transitive dependency scanning is opt-in via \`transitive_deps = True\` in config.`,
        `**Is \`omurtag.toml\` required?** No. It's optional metadata for the template. Without it, the template still works, it just shows no description or stack in \`${toolName} list\`. Add one if you want to publish a template for others.`,
      ],
    }),
  },
];
