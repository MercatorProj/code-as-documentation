# Site delivery (VitePress)

## Default policy

Inspect for an existing docs site and package manager first; reuse the current
toolchain. Propose VitePress only when no site exists and the user wants a browsable
site. Local preview and offline static delivery by default; no CI/CD, Git hooks,
remote hosting, or auto-publish. Never overwrite existing build config, upgrade a
batch of dependencies, or delete an existing site without explicit authorization.

## Procedure

1. Identify Node.js, package manager, project structure; read `package.json`,
   lockfiles, existing `.vitepress/config.*`, and Git state.
2. Confirm docs source directory, site entry, nav, and sidebar information
   architecture. Every menu item must point at a real page.
3. If initializing, change as little as possible: required dependencies, config,
   home page, Markdown source dir; keep existing scripts and lockfile policy.
4. Check paths and rendering for images, attachments, relative links, and Mermaid
   against what is actually installed; never assume features that are not there.
5. Run the repository's real install/preview/build commands. If they cannot run,
   say so; example commands are not project facts.
6. After a successful build, verify output directory, relative asset paths, and
   `base`. For offline delivery, document the static directory, how to serve it, and
   known limits.
7. Report build commands, results, artifact paths, and unverified items. No
   auto-publish, ever.

## Configuration notes

- Configure `srcDir`, `outDir`, `base`, `title`, `description`, and Markdown plugins
  consistently.
- Every `nav`/`sidebar` target must exist; update navigation in the same change that
  moves pages.
- Prefer in-repo relative links that follow VitePress path rules.
- Add the generated directory to `.gitignore` only after checking the existing
  ignore policy.
- Do not bake secrets, internal credentials, personal data, or non-public runbooks
  into static output.
- Exclude scratch and working directories (drafts, meeting notes, personal notes)
  from navigation and from offline packages; they are not published material.

## Offline packaging

Before packaging: identify the real output directory; confirm audience and exclude
internal-only pages; check local links and asset presence; search for remote runtime
dependencies (fonts, images, embeds, APIs) and disclose them; include a README with
contents, build timestamp/version, serving instructions, and limitations; archive
only the intended output (not secrets, `node_modules`, or unrelated repo files);
verify the archive extracts and test serving it over local HTTP.

Do not assume `file://` opening works: SPA routing, module loading, and asset paths
may require HTTP serving or a VitePress `base` configuration and rebuild. For truly
air-gapped use, verify fonts, images, scripts, search indexes, and embeds are local.

## Publishing boundary

No online deployment, account connection, DNS, CDN, CI/CD, or upload is included by
default. Authorization for local packaging is not authorization for remote
publication.
