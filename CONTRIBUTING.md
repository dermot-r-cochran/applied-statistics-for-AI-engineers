# Contributing to Applied Statistics for AI Engineers

Contributions are welcome: corrections to the statistics or the prose, fixes to the page, and checks. A correction to a worked number is especially welcome.

## Before you start

- For anything beyond a small fix, you may find it useful to open an issue first describing the problem and the change you have in mind, before you spend time on it.
- Read the prime directive in `README.md`: one `index.html`, data on top and engine below, no dependencies, no build, no network. A change that adds any of these will not be accepted.
- Changes to the case, the course's rules or the lesson format are the author's decision; propose them in an issue.
- Every worked example is synthetic and says so, apart from the two real reference sets the README describes.

## Making a change

- Keep a pull request to one change, and say in its description what it changes and why.
- Run what CI runs before you push:

```bash
node tools/check.js
node tools/check-docs.js
node tools/check-page.js
```

- Every calculator reproduces its worked example: change a number in the prose and the calculator must agree, and the reverse.
- Write as advice, not orders, in the course's existing voice.

## How a pull request is reviewed

The repository has one maintainer, Dermot Cochran, so a pull request may wait a while before anyone looks at it.

- CI must be green. A failing check is the first thing to fix.
- The review may be assisted by an AI tool, which reads the change and reports to the maintainer. It does not approve or merge anything.
- **Every outside pull request is merged by the maintainer, never by an automated process or an AI tool,** however small.
- A pull request may be declined, or asked to change shape, when it moves the project somewhere it is not meant to go. That is not a judgement on the work.

## Licence

Contributions are accepted under this repository's licences: the engine under the MIT License (`LICENSE`), and the course content under CC BY 4.0 (`CONTENT-LICENSE.md`), the same terms everyone else receives them under. No sign-off line and no contributor licence agreement are required. Only contribute work you have the right to license on these terms.

## Security

Please don't describe a security problem in a public issue or pull request. Report it privately instead, through the repository's **Security** tab (*Report a vulnerability*). Only the maintainer sees the report.
