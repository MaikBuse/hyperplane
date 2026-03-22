# Changelog

## [1.3.0](https://github.com/MaikBuse/hyperplane/compare/v1.2.3...v1.3.0) (2026-03-22)


### Features

* add dev login endpoint and justfile for local development ([fab5cc7](https://github.com/MaikBuse/hyperplane/commit/fab5cc7625ffdb8242ab96996c1c17def614bcf6))
* add GitHub Actions workflow to build and push container images ([ac5f388](https://github.com/MaikBuse/hyperplane/commit/ac5f3881265a29ebea72fd471df98802fef08e7f))
* add Helm chart for Kubernetes deployment ([c2cbdcd](https://github.com/MaikBuse/hyperplane/commit/c2cbdcd805d9c28331f100d0074f58233fed5cd7))
* **auth:** add Zitadel OIDC authentication provider ([70fd208](https://github.com/MaikBuse/hyperplane/commit/70fd208ab53ce37f5c0a096064d28dbffd47e443))
* **auth:** replace all auth methods with Zitadel OIDC ([119ce78](https://github.com/MaikBuse/hyperplane/commit/119ce783b832d5544d056f78214ab3ef7fd8e6bf))
* **auth:** restore email/password and magic link authentication ([787fc3d](https://github.com/MaikBuse/hyperplane/commit/787fc3dfed9966c42d3c1833231bdad1d1784c70))
* **auth:** simplify frontend auth to single Zitadel OIDC redirect ([afc4d1f](https://github.com/MaikBuse/hyperplane/commit/afc4d1f87e157ec04b0a367d428c7c0f44e74d79))


### Bug Fixes

* apply lint and format auto-fixes across codebase ([ed5f3f5](https://github.com/MaikBuse/hyperplane/commit/ed5f3f51e07f56b1bd3bafafcf5b03e2ad85a998))
* **ci:** resolve CI failures in format, build, and tests ([a6e89ad](https://github.com/MaikBuse/hyperplane/commit/a6e89ad8f66358810200aefd743b55535ff421b5))
* delete orphaned admin auth config pages and fix propel formatting ([831fc5c](https://github.com/MaikBuse/hyperplane/commit/831fc5c9680a6e64c171f1bc7e3a46894c4e24f5))
* rename container images from plane-* to hyperplane-* ([4c3c9e5](https://github.com/MaikBuse/hyperplane/commit/4c3c9e59d3a339231877b588a887ce2bc2baeb37))
* resolve formatting and type errors across codebase ([c5ddb1c](https://github.com/MaikBuse/hyperplane/commit/c5ddb1c4c8102247cf0b179661944a966065986a))
* resolve remaining type-check errors in space and web apps ([7e7a620](https://github.com/MaikBuse/hyperplane/commit/7e7a620b617b5783594be6e037a2cc1b1816713d))
* resolve type errors for setPassword and github_app_name ([7a85fb2](https://github.com/MaikBuse/hyperplane/commit/7a85fb21749ea3a18e6957130e586d5c23d775b8))
* **tests:** fix unit test failures in copy_s3_objects and url utils ([972e8f8](https://github.com/MaikBuse/hyperplane/commit/972e8f8839b117719b26fd92d9eec93ff3ec41ab))
