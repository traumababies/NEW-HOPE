# OPERATING-CONTEXT — the shared world-state for the évolué AI media team

Purpose: the **ONE page every assistant is seeded with at each boundary** (new week,
new brief, or whenever laws change) so the team works from the same map. AIs don't
"meet"; they read this and stay aligned. Owner updates it at the start of each week
(~5 minutes), and one-line outcomes are folded back at week's end.

## How to use it
1. At the start of the week, fill the "current week" section below.
2. Every assistant's prompt/context references this file (or its distilled subset
   per role - nobody needs all of it).
3. When the week closes: approved outcomes → History + `training_knowledge`;
   rejected reasons → `taste.md` (one tagged line per rejection).
4. Bump the version at the bottom whenever a law/contract changes so no assistant
   serves a stale format.

## Current week
| field | value |
|---|---|
| Version | 1 |
| Week (W##) + dates | |
| Theme | |
| 9 subjects (IPTC) | ART / CHM / CIN / CUL / FIN / HLT / HUM / LIF / PRD (one line each: what *this week's* angle is) |
| Brand voice (one line) | |
| Tone notes | |
| Posts / positions | 1-9, with Mon/Wed/Fri mapping (1-3 Mon, 4-6 Wed, 7-9 Fri) |
| In flight | Cataloger queue: _ · Media Editor queue: _ · Scout candidates (ephemera): _ · Scheduler: _ |
| Last week's rejects (distilled why) | 3-5 bullet lines, written as data (tag per `taste.md`) |
| Approval thresholds | e.g., no gore; no modern faces in vintage frames; rights statement required; pale-cool palette |
| Platform rules | IG feed 1080×1350 · TT 1080×1920 · 5 hashtags/platform · 3 posts Mon/Wed/Fri |

## Who reads what
| Role | Reads from | Writes to |
|---|---|---|
| Creative Director | theme calendar, brand voice, last 2-4 weeks of decisions | the weekly Creative Brief (this file's Week/Theme) |
| Current Events (compound) | the Brief | 2-3 current claims w/ primary-source URLs + confidence |
| Fact Checker (compound-mini) | Current Events output | verified claims + confidence ranking |
| Muse | approved Library (9 subjects) + approval history | per-subject: 1 library pick, 1 gap, 1 caption |
| Content Scouts | the Brief's search terms + subject codes | 9 candidates/subject into **ephemera**, provenance intact |
| Studio (owner) | candidate grid | choices + one tagged "why" per call (→ taste.md) |
| Cataloger | Library filename law + Dublin Core contract | ISO-8601 record + library_review_queue staging |
| Media Editor | chosen originals + brief + platform formats + rejection grammar | previews → approval → FB/IG/TT derivatives |
| Scheduler | approvals + calendar | Mon/Wed/Fri publish queue (deterministic) |

## Team law (the 6 rules)
1. One Brief - every stage reads the same artifact.
2. One map - this file is re-seeded at every boundary.
3. Contracts over conversation - output N+1 is input N; schemas versioned.
4. The queue is the meeting.
5. Shared memory = every approved/rejected decision with its why.
6. The calendar is the heartbeat - every role knows its turn in the week.