---
name: onec-element-ide
description: Work in cloud 1C:Element IDE workspaces through the in-app browser, keep edits visible in the IDE and its connected Git repository, and run the publish/update/test loop. Use when the user gives a 1C:Element IDE URL or IDE id, asks to continue development inside cloud Element IDE, wants app code changes to survive Git sync, or needs to avoid the mismatch where a deployed assembly changed but IDE source/Git did not.
---

# 1C:Element IDE Workflow

## Core Rule

Treat the IDE workspace as the source of truth when the user cares about future Git sync. A cloud assembly update alone is not enough: it can make the application run new code while the IDE/Git still contains old code. Do not call the task done until the relevant IDE source files are changed, saved, committed, and synchronized in the IDE Git panel, or until you clearly report that this step is blocked.

## Intake

When the user provides an IDE URL or id:

1. Normalize it to an IDE URL. Use `scripts/ide_url.py` if helpful.
2. Open the IDE in the in-app browser and reuse the user's authenticated session. If the IDE redirects to `ide-auth` or shows a login screen, ask the user to log in and then continue from the same tab.
3. Ask the user for the console/control-panel key and secret if they were not already provided in the current task. Use them only for the active session and never write them into committed files.
4. Identify the project, active app, and branch from the status bar. Note signals such as `workspace (Git) - main*`, `Основная ветка (main*)`, and `есть неопубликованные изменения`.
5. Keep track of any separate deployed application id or app URL if the user also wants live testing.

Use the Browser Use plugin/in-app browser for IDE work. Do not use only console API assemblies when the user expects IDE-visible source changes.

## Required Finish Loop

After every code change, before calling the task complete:

1. Verify that the changes are visible in the IDE source, not only in a local export or deployed assembly.
2. Commit and synchronize/push the change through IDE Git.
3. Publish or update the application.
4. Test the changed behavior and fix regressions found during testing.

## Edit In IDE Source

Prefer editing files directly in the IDE editor:

1. Use the project navigator or quick file search to open each target `.xbsl`/`.yaml` file.
2. If you prepared code locally from an exported assembly, paste the whole updated file into the IDE only after confirming the target tab is the correct file.
3. Save after each file.
4. Verify inside the IDE using editor search:
   - search for newly added helper names or changed fields;
   - search for removed hardcoded strings and confirm `Результаты отсутствуют`;
   - check line breadcrumbs/tabs to ensure the search is in the intended file.
5. For broad changes, open the IDE Git diff or changed-file list before committing.

Avoid the trap of editing only `.tmp` exports, generated ZIPs, or local scratch copies. Those are useful for preparing patches and smoke tests, but they do not protect the IDE Git source from later overwrite.

## Git Discipline In IDE

Before committing:

1. Open the source control panel in the IDE.
2. Confirm the changed-file count and filenames match the task. For example, a focused server/model fix should show only files such as `Prompt` and `ИнтеграцияСС`, not unrelated metadata churn.
3. If unrelated user changes appear, do not include them blindly. Ask or use manual selection if the IDE offers it.
4. Commit with a concise Russian message describing the production change.
5. Use the IDE action that commits and synchronizes/pushes, such as `Зафиксировать и отправить`, or commit then run `Синхронизировать изменения`.
6. Wait for a success signal such as `Синхронизация успешно завершена`, `Изменения 0`, or a clean branch status.

If the IDE says `Репозиторий не найден`, API branch endpoints are unavailable, or the Git panel does not expose commit controls, report the blocker and leave a Git-applicable patch as a fallback. Do not imply the change is safely in Git.

## Publish And Test Loop

After the IDE/Git source is protected:

1. Publish/rebuild/update the app through the IDE command (`1C: Опубликовать проект`, `1C: Пересобрать проект`) or through documented console API commands.
2. If using console API assemblies, verify the final application source version/status after update.
3. Smoke-test the exact changed behavior through the live app HTTP endpoints or UI.
4. Distinguish 1C wrapper failures from backend failures:
   - missing key, serialization, auth, and balance errors are likely 1C-side;
   - backend 4xx/5xx responses after the wrapper mapping is correct may be service-side;
   - timeouts should be reported with endpoint, payload shape, and whether direct backend calls behave differently.

When a user asks "why don't I see the change in IDE?", immediately check whether prior work changed an exported assembly instead of the IDE workspace. Move or replay the patch into the IDE source and commit/sync it.

## Console API Use

Use console API for app metadata, export/import, assembly upload, update, and status checks. Prefer official 1C:Element console API documentation when endpoint details matter. Keep credentials out of committed files; pass them as environment variables or session-only values.

Common observations:

- IDE API URLs under `/ide/api/v1/<id>/` often require browser `ide-auth` cookies. Bearer tokens from the console API may not authorize direct IDE file access.
- Console project branch endpoints may be unavailable for some Element projects. This does not mean the IDE Git panel is unusable; use the authenticated IDE UI.
- A deployed app can be on a newer assembly while IDE Git remains old. Always verify both surfaces when Git preservation matters.

## Useful References

Read `references/ide-git-checklist.md` when the task involves committing/syncing Element IDE source or diagnosing IDE-vs-deploy mismatch.
