# IDE Git Checklist

Use this checklist when a 1C:Element change must be visible in the cloud IDE and protected in Git.

## Before Editing

- Confirm the browser is on the IDE workspace, not only the published app.
- If the IDE URL redirects to login, wait for the user to authenticate in the same in-app browser.
- Read the status bar:
  - active application name;
  - branch name;
  - Git source-control status;
  - unsaved/unpublished markers.
- If code was already changed through exported assemblies, keep that export as a patch source but replay it into IDE files.

## Editing

- Open each target file from the navigator or quick search.
- Confirm the tab path/breadcrumb before replacing content.
- Save every edited file.
- In each edited file, search for:
  - the new helper/function names;
  - removed hardcoded strings;
  - key request fields such as `model`, `user_id`, `dataset_id`, or endpoint URL builders.
- If a removed hardcode still appears as a deliberate fallback, distinguish fallback from direct service call.

## Source Control

- Open the IDE source-control panel.
- Confirm the changed-file count and names.
- If unrelated files appear, use manual change selection or ask before committing.
- Commit with a short production-oriented Russian message.
- Push/synchronize from the IDE and wait for a positive signal:
  - `Синхронизация успешно завершена`;
  - `Изменения 0`;
  - clean branch badge without `*`.

## After Commit

- Publish/rebuild/update the application.
- Verify the application status is running/healthy.
- Smoke-test the changed endpoints or UI paths.
- In the final answer, separate:
  - IDE/Git source status;
  - published application status;
  - test results and any backend-side residual issue.

## Failure Modes

- **Assembly changed, IDE did not:** source was edited in an export or uploaded as an assembly only. Replay the patch into IDE source and commit.
- **Console token does not access IDE API:** use browser `ide-auth` session through the in-app browser.
- **IDE Git panel says repository not found:** report blocker; preserve a patch file; do not claim Git is protected.
- **Smoke test times out after wrapper mapping is correct:** test direct backend if possible and report likely backend/service issue.
