# Platform Matrix

| Platform | Target content | Preferred route | Current state |
|---|---|---|---|
| YouTube | Shorts and videos | Existing Google OAuth; later Postiz bridge | Existing automation |
| TikTok | Vertical video | Postiz + TikTok Content Posting API | Needs developer app/OAuth |
| Instagram | Reels/posts | Postiz + Meta official API | Needs professional account/app/OAuth |
| Facebook | Reels/Page posts | Postiz + Meta official API | Needs Page/app/OAuth |
| Threads | Text/media distribution | Postiz + Threads API | Needs Meta scopes/OAuth |
| LinkedIn | Business/career content | Postiz + LinkedIn 3-legged OAuth | **v2.23.0 production-blocked:** source gate found `202601` plus stale `202306`; update all calls above official `202508` sunset floor, then run staged 2 MiB ranged-upload probe |
| X | Short text/media | Postiz + official X API | 1 MiB range fixture passes; live staged probe and paid write access remain required |
| Reddit | Community-specific posts | Postiz + Reddit OAuth | Needs app/account/rules policy |
| Pinterest | Evergreen visual posts | Postiz + Pinterest OAuth | MP4-after-cover fixture passes; live staged register/upload/create probe and developer app/OAuth remain required |
| Bluesky | Text/media | Postiz + AT Protocol | Needs account app credential/OAuth |

Update this file only from live identity, scope, and harmless capability probes.

Release-specific evidence and unresolved compatibility checks are recorded in [`RELEASE_WATCH.md`](RELEASE_WATCH.md).
