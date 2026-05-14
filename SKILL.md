---
name: onec-element-ide
description: Work with 1C:Element cloud projects by downloading source files locally through the control-panel/API flow, editing them in the local workspace, uploading the corrected files back to the control panel, and then verifying the result in the IDE, Git state, published app, and tests. Use when the user gives a 1C:Element IDE URL or id, control-panel credentials, asks to change Element app code, wants changes to survive Git sync, or needs to avoid the mismatch where local/uploaded changes are not visible in IDE/Git.
---

# 1C:Element Cloud Source Workflow

## Core Rule

Treat the downloadable source in the control panel as the editable working copy and keep the IDE/Git view as the verification surface. The normal loop is: download files locally, edit in the local workspace, upload/update through the control panel, then confirm that IDE/Git and the published app see the same change. A cloud assembly update alone is not enough if it does not land in the source that the IDE/Git will later pull from.

## Intake

When the user provides an IDE URL or id:

1. Normalize it to an IDE URL. Use `scripts/ide_url.py` if helpful.
2. Ask the user for the console/control-panel key and secret if they were not already provided in the current task. Use them only for the active session and never write them into committed files.
3. Use the control-panel/API flow to identify the project, application, source package/files, branch/source version, and published application URL if live testing is needed.
4. Download the relevant source files or export package into a local working directory before editing.
5. Open the IDE in the in-app browser only when needed to verify that uploaded changes, source-control state, or published status are visible there. If the IDE redirects to `ide-auth` or shows a login screen, ask the user to log in and then continue from the same tab.

Use the Browser Use plugin/in-app browser for IDE checks. Do not make the IDE editor the primary edit surface unless the control-panel download/upload path is blocked or the user explicitly asks for direct IDE editing.

## Required Finish Loop

After every code change, before calling the task complete:

1. Upload the corrected local files/package through the control panel.
2. Verify that the uploaded changes are visible from the IDE/source view, not only in the local workspace or deployed assembly.
3. Commit and synchronize/push through the connected Git flow if the control panel/IDE exposes Git state for the project.
4. Publish or update the application.
5. Test the changed behavior and fix regressions found during testing.

## Local Edit And Upload

Prefer editing downloaded source files locally:

1. Download the project source/export package from the control panel into a local task directory.
2. Locate each target `.xbsl`/`.yaml` file with `rg`/local search and make the edits locally.
3. Search the local tree for newly added helper names, changed fields, and removed hardcoded strings before upload.
4. Rebuild/repack the source package only with the intended file changes.
5. Upload the changed files/package back through the control-panel/API flow.
6. After upload, verify in the IDE or control-panel source view that the same file content is now visible there.

Avoid the trap of editing local exports without uploading them back to the control panel. Local files are only a staging area; the task is not finished until the control panel accepts the upload and the cloud source reflects the change.

## Git Discipline In IDE

When the project exposes Git state through the IDE or control panel:

1. Open the source control panel in the IDE.
2. Confirm the changed-file count and filenames match the task. For example, a focused server/model fix should show only files such as `Prompt` and `ИнтеграцияСС`, not unrelated metadata churn.
3. If unrelated user changes appear, do not include them blindly. Ask or use manual selection if the IDE offers it.
4. Commit with a concise Russian message describing the production change.
5. Use the IDE action that commits and synchronizes/pushes, such as `Зафиксировать и отправить`, or commit then run `Синхронизировать изменения`.
6. Wait for a success signal such as `Синхронизация успешно завершена`, `Изменения 0`, or a clean branch status.

If the IDE says `Репозиторий не найден`, API branch endpoints are unavailable, or the Git panel does not expose commit controls, report the blocker and leave a Git-applicable patch/source upload record as a fallback. Do not imply the change is safely in Git.

## Publish And Test Loop

After the uploaded source is visible in the cloud project:

1. Publish/rebuild/update the app through the IDE command (`1C: Опубликовать проект`, `1C: Пересобрать проект`) or through documented console API commands.
2. If using console API assemblies, verify the final application source version/status after update.
3. Smoke-test the exact changed behavior through the live app HTTP endpoints or UI.
4. Distinguish 1C wrapper failures from backend failures:
   - missing key, serialization, auth, and balance errors are likely 1C-side;
   - backend 4xx/5xx responses after the wrapper mapping is correct may be service-side;
   - timeouts should be reported with endpoint, payload shape, and whether direct backend calls behave differently.

When a user asks "why don't I see the change in IDE?", immediately check whether prior work changed only local files, a temporary export, or a deployed assembly. Upload/replay the patch into the control-panel source and then verify IDE/Git visibility.

## Console API Use

Use console/control-panel API for app metadata, source download/export, source upload/import, assembly upload, update, and status checks. Prefer official 1C:Element console API documentation when endpoint details matter. Keep credentials out of committed files; pass them as environment variables or session-only values.

Common observations:

- IDE API URLs under `/ide/api/v1/<id>/` often require browser `ide-auth` cookies. Bearer tokens from the console API may not authorize direct IDE file access.
- Console project branch endpoints may be unavailable for some Element projects. This does not mean the IDE Git panel is unusable; use the authenticated IDE UI.
- A deployed app can be on a newer assembly while IDE Git remains old. Always verify both surfaces when Git preservation matters.

## Useful References

Read `references/ide-git-checklist.md` when the task involves committing/syncing Element IDE source or diagnosing IDE-vs-deploy mismatch.
