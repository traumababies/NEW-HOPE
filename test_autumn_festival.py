"""
FULL END-TO-END TEST: Autumn Festival
"""
import json
from evolue.config import get_settings
get_settings.cache_clear()

import evolue.ai.providers as prov
prov._PROVIDERS.clear()

from evolue.domain.calendar import Week
from evolue.application.services.workflow import (
    step1_save_theme, step2_compose_brief, step2b_current_events,
    step3b_validate_brief, step3c_creative_grade, step3d_production_grade,
    step5_muse_search, step6_extract_scout_requests,
    step9_studio_commit, step16_scheduler, close_loop,
)

WEEK = Week(year=2026, week_number=42, theme="Autumn Festival")
CONTEXT = """Theme: Autumn Festival. Palette: Orange and Brown.
Ideas: Full Moon, Mooncakes.
Post 1 (CUL): Balsam crushed petals wrapped around nails with leaves/strings on asian girl fingers.
Post 2 (LIF): Persimmons hanging by string on ceiling.
Brand voice: Warm, restrained, editorial. Platform: IG and TT, 9:16."""

print("=" * 60)
print("AUTUMN FESTIVAL — FULL PIPELINE TEST")
print("=" * 60)

# Step 1
print("\n--- STEP 1: Save Theme ---")
print(f"Theme: {step1_save_theme(WEEK)}")

# Step 2
print("\n--- STEP 2: Creative Director ---")
r2 = step2_compose_brief(WEEK, context=CONTEXT)
b = r2["result"]
print(f"Provider: {r2['provider_used']}")
print(f"Theme: {b.get('weekly_theme','?')}")
print(f"Posts: {len(b.get('post_briefs',[]))}")
for p in b.get("post_briefs",[])[:3]:
    print(f"  Post {p.get('position')}: {p.get('subject_code','')} - {p.get('working_title','')[:50]}")

# Step 2b
print("\n--- STEP 2b: Current Events ---")
r2b = step2b_current_events(b, context=CONTEXT)
print(f"Provider: {r2b['provider_used']}")
print(f"Claims: {len(r2b['result'].get('claims',[]))}")


# Step 5
print("\n--- STEP 5: Muse ---")
rm = step5_muse_search(b, [], context=CONTEXT)
m = rm["result"]
print(f"Provider: {rm['provider_used']}")
gaps = [p for p in m.get("positions",[]) if p.get("gap")]
picks = [p for p in m.get("positions",[]) if p.get("selected_candidate_id")]
print(f"Positions: {len(m.get('positions',[]))}, Library picks: {len(picks)}, Gaps: {len(gaps)}")
for p in m.get("positions",[])[:3]:
    g = p.get("gap")
    if g: print(f"  Pos {p['position']}: GAP - search: {g.get('search_terms',[])}")

# Step 6
print("\n--- STEP 6: Scout Requests ---")
srs = step6_extract_scout_requests(m)
print(f"Requests: {len(srs)}")

# Step 7/8 - Scout infra check
print("\n--- STEP 7/8: Content Scouts ---")
from evolue.infrastructure.scouts import SUBJECT_CODES
from evolue.config import settings
print(f"Subjects: {SUBJECT_CODES}")
print(f"Platforms: Pixabay({settings.scout_pixabay_per_page}), Pexels({settings.scout_pexels_per_page}), Unsplash({settings.scout_unsplash_per_page}), Coverr({settings.scout_coverr_page_size})")
print(f"Quarantine: Ephemera container ({settings.container_ephemera})")

# Step 9
print("\n--- STEP 9: Studio COMMIT ---")
sel = [f"{c}_01" for c in SUBJECT_CODES]
com = step9_studio_commit("2026_W42_Autumn-Festival", sel)
print(f"Committed: {len(com['committed'])}, Destroyed: {com['destroyed']}")
for c in com["committed"][:2]:
    print(f"  {c['tile']}: orig={c['original'][:50]}...")
    print(f"    deriv={c['derivative'][:50]}...")
    print(f"    hasVersion={c['original_meta']['dcterms:hasVersion']}")
    print(f"    isVersionof={c['derivative_meta']['dcterms:isVersionof']}")

# Step 16
print("\n--- STEP 16: Scheduler ---")
for t in [1,4,7]:
    s = step16_scheduler(platform="instagram", tile=t)
    print(f"  IG tile {t}: {s['day']} {s['window']} {s['timezone']}")
for t in [9,6,3]:
    s = step16_scheduler(platform="tiktok", tile=t)
    print(f"  TT tile {t}: {s['day']} {s['window']} {s['timezone']}")

# Closed Loop
print("\n--- CLOSED-LOOP TEST ---")
loop = close_loop("2026_W42_CUL_01_dcterms:isVersionof_v1-0_abc123", "bunbuns/2026_W42_CUL_01.jpg")
print(f"State: {loop['state']}")
print(f"Storage: {loop['storage']}")
print(f"Previous deleted: {loop['previous_deleted']}")

print("\n" + "=" * 60)
print("FULL PIPELINE TEST COMPLETE")
print("=" * 60)
# Step 3b
print("\n--- STEP 3b: Validator ---")
rv = step3b_validate_brief(b, context=CONTEXT)
print(f"Provider: {rv['provider_used']}")
print(f"Verdict: {rv['result'].get('verdict','?')}, Score: {rv['result'].get('structural_score','?')}")

# Step 3c
print("\n--- STEP 3c: Creative Grader ---")
rcg = step3c_creative_grade(b, context=CONTEXT)
print(f"Provider: {rcg['provider_used']}")
print(f"Score: {rcg['result'].get('total_score','?')}/100, Verdict: {rcg['result'].get('verdict','?')}")

# Step 3d
print("\n--- STEP 3d: Production Grader ---")
rpg = step3d_production_grade(b, context=CONTEXT)
print(f"Provider: {rpg['provider_used']}")
print(f"Score: {rpg['result'].get('total_score','?')}/75, Verdict: {rpg['result'].get('verdict','?')}")