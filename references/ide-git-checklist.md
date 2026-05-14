# Control Panel Upload And IDE/Git Checklist

Use this checklist when a 1C:Element change is edited locally through a downloaded source/export and must then become visible in the cloud IDE and protected in Git.

## Before Editing

- Confirm the control-panel key and secret are available for the active session.
- Download the current source/export from the control panel before editing.
- Record the active application, source/package version, branch/Git state if exposed, and published app URL if live testing is needed.
- If code was already changed only in local scratch files or a deployed assembly, keep that change as a patch source but upload/replay it into the control-panel source.

## Local Editing

- Open each target file from the downloaded local source tree.
- Confirm the path before replacing content.
- Save every edited file locally.
- Search the local tree for:
  - the new helper/function names;
  - removed hardcoded strings;
  - key request fields such as `model`, `user_id`, `dataset_id`, or endpoint URL builders.
- If a removed hardcode still appears as a deliberate fallback, distinguish fallback from direct service call.
- Upload the corrected files/package back through the control panel.
- Verify in IDE/source view that the uploaded content is visible in the cloud project.

## Source Control

- Open the IDE/control-panel source-control view when available.
- Confirm the changed-file count and names.
- If unrelated files appear, use manual change selection or ask before committing.
- Commit with a short production-oriented Russian message.
- Push/synchronize and wait for a positive signal:
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

- **Local files changed, IDE did not:** the edited export was not uploaded or the upload targeted the wrong project/source version. Upload/replay the patch into the control-panel source and verify IDE visibility.
- **Assembly changed, source did not:** an assembly was uploaded without updating the source tracked by IDE/Git. Replay the patch into the control-panel source and commit/sync if available.
- **Console token does not access IDE API:** use browser `ide-auth` session through the in-app browser.
- **IDE Git panel says repository not found:** report blocker; preserve a patch file; do not claim Git is protected.
- **Smoke test times out after wrapper mapping is correct:** test direct backend if possible and report likely backend/service issue.
