# House-style rules

Every change the skill makes cites one of these rules by number. A preference the user gives
at the start (section order, page length, sections, target role, look) overrides the matching
rule, and the change table says so.

## Page and layout
1. One page, US Letter. The render fails when the page limit is exceeded.
2. No bullet wraps to a second line. About 120 rendered characters per bullet, fewer when it
   has several bold spans.
3. Minimal white space: every bullet fills 90-99% of its line when the facts allow (never
   pad), and the page runs to the bottom margin.
4. Font: Source Sans Pro, 11pt, chosen for being narrow.
5. Margins about 0.5 in on all sides (0.75 in in the roomy look).
6. Section titles in small caps with a full-width rule under them.

## Header
7. Name centered, large, small caps.
8. One contact line under it: city, phone, email, LinkedIn, GitHub, website, separated by `|`.
   Leave out any item the person doesn't have.
9. URLs shown as text (`linkedin.com/in/...`), since parsers drop link targets.
10. No photo, no summary or objective section, no "references available" line.

## Section order
11. Technical Skills, Experience, Projects, Involvements, Education.

## Each section
12. **Technical Skills:** labeled lines grouped by the person's field (for example Languages,
    Frameworks, Data, Cloud, Tools), label in bold, comma list after. Include the concept words
    postings use (Machine Learning, REST APIs, Agile, OOP), not only tool names. No soft-skill
    claims (team player, fast learner); bullets show those. Listed skills that no bullet backs
    get one question for the whole list: which can they defend in an interview (rule 27).

13. **Experience:** `Bold Title | italic Company, team, City` on the left, dates on the right.
    A promotion is one entry with an arrow (`Developer → Senior Developer`). 1-5 bullets, the
    most for the current role.

14. **Projects:** `Bold Name - context (hackathon, award) | italic tech stack` on the left, date
    on the right. The name links to the live site, repo or write-up when one exists. 2-3 bullets.

15. **Involvements:** `Bold Org | italic Role` on the left, dates on the right. One bullet each.

16. **Education:** school and city, then `Program, Credential | GPA` (GPA only if they list it)
    with dates, then one "Relevant Coursework" bullet.

17. The left side of a heading stays short so it doesn't collide with the date.

## Bullets
18. Start with a strong verb that claims no more than the person did: past tense for finished
    work (Built, Engineered, Delivered), present tense for ongoing duties in a current role
    (Ship, Lead). A role is current when it ends Present or in the future; finished pieces of
    work inside it stay past tense.
19. Bold the technology and the number, not the verb. Numbers are bold and italic (`97.6%`,
    `500+`).
20. Each bullet says what was built or done, with what, and the result or scale when one exists.
21. Company and project names are underlined links when a link exists.

## Dates and parsing
22. One date format everywhere: `Oct 2020 -- Feb 2022`, `Present` for ongoing work. An expected
    future end date is fine. Separate stints at one place are listed with commas
    (`Sep 2025, Sep 2026`).
23. Text extracted from the PDF (`pdftotext`) reads cleanly and in order.
24. A target role or posting only reorders skill lines and projects and picks which concept
    words lead. It adds no new claims.

## Truth
25. Every fact comes from the person's facts file. Nothing goes on the page that isn't there.
26. No invented metrics. Team results stay team results. What the person wrote stays unless
    they change it; anything they say is unsure stays off until they confirm it.
27. Keywords stretch only as far as the person can defend in an interview or a coding test.
28. Anything the person marks private stays off.
