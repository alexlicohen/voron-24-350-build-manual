# Licence check — wave 4, subtask 2C (2026-09-24)

Checked against each repo's actual LICENSE file via GitHub, not recalled. A repo's
code licence does not automatically cover its docs/images — checked separately below
where a distinct docs licence or notice could plausibly exist.

| Repo | LICENSE file | Licence | Docs/images covered separately? | Embed (Alex's decision 3) |
|---|---|---|---|---|
| [Klipper3d/klipper](https://github.com/Klipper3d/klipper) | `COPYING` (repo root; single file, no per-directory exception) | GPL-3.0 | No — README points to the same `COPYING` for "documentation"; no notice in `docs/` or `docs/img/` | **Yes** — embed (already the class of licence used for Voron/LDO images; Alex's explicit instruction) |
| [mainsail-crew/docs](https://github.com/mainsail-crew/docs) | `LICENSE` (repo root, default branch `zensical`) | GPL-3.0 | No separate docs/image notice found (README has none) | **Yes** — permissive/GPL with attribution, clears |
| [KlipperScreen/KlipperScreen](https://github.com/KlipperScreen/KlipperScreen) | `LICENSE` (repo root) | AGPL-3.0 | No separate `docs/` notice; `docs/img` sits under the same root LICENSE | **Yes** — AGPL-3.0 permits redistribution with attribution, clears |
| [nevermore3d/Nevermore_Micro](https://github.com/nevermore3d/Nevermore_Micro) | none present (GitHub license API returns null; README has no licence statement) | **None stated** | N/A | **No** — link only, no licence to redistribute under |
| [tanaes/whopping_Voron_mods](https://github.com/tanaes/whopping_Voron_mods) (Clicky-Clack door source) | `LICENSE` (repo root) | GPL-3.0 | No separate notice for `clickyclacky_door/` | **Yes** — clears |
| [raspberrypi/documentation](https://github.com/raspberrypi/documentation) | `LICENSE.md` (repo root) | CC-BY-SA-4.0 | No separate image notice found | **Yes** — share-alike with attribution, clears |

## Notes
- The KB3D wiki (Clicky-Clack install photos, 34 images) and ldomotion.com (LDO's Leviathan/Nevermore
  step guides) are **not** GitHub repos and carry no stated licence anywhere on either site — confirmed
  already in `docs/voron-build-instructions-survey.md` § Licensing conclusion (link only, unchanged by
  this check).
- Per Alex's decision 3: Klipper-docs images embed outright; Mainsail docs, KlipperScreen, the
  Clicky-Clack source repo and raspberrypi/documentation also clear (all GPL-3.0/AGPL-3.0/CC-BY-SA-4.0,
  redistribution with attribution permitted); Nevermore Micro does not clear — link only.

## 2E result — nothing to mirror this pass
`grep -n '!\[.*\](http' docs/manual/1[1-4]-*.md` returns no matches: every image already referenced in
chapters 11–14 is already a local `assets/remote/…` file (mirrored in earlier waves), each with an
existing `SOURCES.txt` entry. The plan (§2 Design: screenshots table) names candidate sources for new
Ch 11–14 images (Klipper `docs/img` figures for 14.7–14.18, Mainsail/KlipperScreen docs screenshots,
Nevermore Micro / Clicky-Clack source images) but gives no concrete file list — repo + purpose only, no
specific filenames or URLs. Per the brief's instruction to pick at most the images the chapters already
link as remote URLs when no concrete list is given, and since that grep is empty, no new files are
mirrored in this pass. Choosing specific figures and running them through this cleared/not-cleared table
is scoped to 2F (content packets) and to 2D's screenshot spike, not to 2C/2E.
