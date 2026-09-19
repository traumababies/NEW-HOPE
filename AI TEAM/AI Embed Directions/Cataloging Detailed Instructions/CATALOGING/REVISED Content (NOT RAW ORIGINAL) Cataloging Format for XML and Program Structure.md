**THESE DIRECTIONS ARE FOR THE REVISED FINAL INSTAGRAM AND TIKTOK CONTENT, NOT FOR ORIGINAL RAW CONTENT (PLEASE LOOK AT FILE: FOR HOW TO CATALOG ORIGINAL RAW CONTENT WE DID NOT MODIFY)**

Legally Called DERIVATIVE WORK when altered/combined existing content

Where to find 15 Dublin Core for Cataloging:

ISO 8601 with IPTC Subject Code filename: 
2026-09-10_W37_COS_EXFOLIANT_08_ig-tt.wp4

Format: 
YYYY(year)-MM(month)-DD(day)_W##(week00)_IPTC-SUBJECT-CODES_THEME_SEQUENCE_HOST.FILE_EXTENSION

**Where to find all 15 Element Catalog Record**:

1. dc:title = In file name (available after MUSE) a: "YYYY_W##_THEME_FILE-EXTENSION_SEQUENCE_for-HOST"

2. dc:creator = "Evolue Media Team" is default

3. dc:subject = In file name (available after Muse): IPTC-SUBJECT-CODES

4. dc:description = Captions and Hashtags for Instagram/TikTok once they are Approved (COPYWRITER - available after final approval)

5. dc:publisher = "Evolue Skincare Inc" by default

6. dc:contributor = "Original Creator via url of platform and image/video" ex: Jane Doe via www.pixels.com/photo/12345 (Available by CONTENT SCOUTS after Studio Cut)

7. dc:date = In file name: "yyyy-mm-dd" - always use creation date after final approval (MEDIA EDITOR)

8. dc:type = In file name: .FILE-EXTENSION - use "MovingImage" for video (mp4) and "StillImage" for image (jpeg, png, webp), and for documents, codes, html, anything in a language use "Text" (docx, pdf, html, json, md), "Sound" for audio files, "Dataset" for spreadsheets and databases, "Software" for computer programs, applications, or executable scripts (distinct from the raw text files containing code), and "InteractiveResource" for web applications, VR environments, or games requiring user input (Available by CONTENT SCOUTS after Studio Cut)

9. dc:format = in file name: .FILE-EXTENSION - use image/jpeg or image/png or image/webp. For videos, video/mp4. For text, text/docx, text/html, text/md, text/json, text/pdf (Available at the same time as dc:type, after Studio Cut)

10. dc:identifier = Full file name - "YYYY-MM-DD_W##_IPTC-SUBJECT-CODES_THEME_SEQUENCE_HOST.FILE_EXTENSION" (Available after Final Approval)

11. dc:source = "URL of platform" ex: www.pixels.com (Available after Studio Cut)

12. dc:language = "eng" by default - Use ISO 639-3 Standards

13. dc:relations = In file name: "YYYY_ITPC-SUBJECT-CODE" ex: 2026_COS

14. dc:coverage = "Global" by default

15. dc:rights = "© 2026 Evolue Skincare Inc. All rights reserved for new creative additions. Pre-existing image elements are utilized under the standard content license provided by dc:resource." is default (Available by CONTENT SCOUT after Studio Cut)

ex: © 2026 Evolue Skincare Inc. All rights reserved for new creative additions. Pre-existing image elements are utilized under the standard content license provided by www.pexels.com

16. dcterms:hasVersion (Original) and dcterms:isVersionof (Derivative) are "Version" with dc:identifier=url of original work creating UUIDs that links both Original and Derivative works. UUIDs are created using uuidv7() which uses time and random numbers.


XML:

<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">

&#x20; [dc:identifier](dc:identifier)2026-09-12\_W37\_BEA\_EXFOLIANT\_3100\_ig.mp4</dc:identifier>

&#x20; [dc:title](dc:title)Exfoliant Product Focus – Week 37 Instagram Post</dc:title>

&#x20; [dc:creator](dc:creator)Your Brand Media Team</dc:creator>

&#x20; [dc:publisher](dc:publisher)Your Brand</dc:publisher>

&#x20; [dc:contributor](dc:contributor)Jane Doe via Pexels</dc:contributor>

&#x20; [dc:source](dc:source)https://www.pixels.com/photo/12345</dc:source>



&#x20; <!-- Controlled Subjects: IPTC Code + Theme -->

&#x20; <dc:subject scheme="IPTC">BEA</dc:subject>

&#x20; [dc:subject](dc:subject)EXFOLIANT</dc:subject>

&#x20; [dc:subject](dc:subject)Skincare</dc:subject>



&#x20; [dc:description](dc:description)15-second texture breakdown showing exfoliant application over ambient music.</dc:description>

&#x20; [dc:type](dc:type)MovingImage</dc:type>

&#x20; [dc:format](dc:format)video/mp4</dc:format>

&#x20; [dc:date](dc:date)2026-09-12</dc:date>

&#x20; [dc:language](dc:language)en</dc:language>

&#x20;

&#x20; <!-- Origin and Relationships -->

&#x20; [dc:source](dc:source)https://www.pexels.com/photo/123456/</dc:source>

&#x20; [dc:relation](dc:relation)IsPartOf: 2026\_Q3\_Exfoliant\_Campaign</dc:relation>

&#x20;

&#x20; <!-- Scope \\\& Rights -->

&#x20; [dc:coverage](dc:coverage)2026-Q3</dc:coverage>

&#x20; [dc:coverage](dc:coverage)Global</dc:coverage>

&#x20; [dc:rights](dc:rights)Copyright 2026 Evolue Skincare Inc. Contains stock media used under Pexels License.</dc:rights>

</metadata>





STRUCTURE:

\[ User / App Interface inside REVIEWS PAGE ]  ──► (Writes SQL Data) ──► \[ Azure SQL Database Tables ]

&#x20;                                                            │

&#x20;                                                            ▼ (Only if requested by external software)

&#x20;                                                    \[ Dynamic XML Export ]
