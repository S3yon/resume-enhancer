# Expected audit rows for messy-resume.txt

Each line names a rule break the change table must have a row for, with that rule number.
The dry run uses house-style defaults, answers "unknown" to every gap question, and approves
every row.

rule 10: the Objective section is removed
rule 10: "References available upon request." is removed
rule 11: sections reordered to Skills, Experience, Projects, Involvements, Education
rule 22: dates normalized to `Mon YYYY -- Mon YYYY` (2023-05 to May 2023, May '24 to May 2024)
rule 22: "Summer 2022" gets a Gap row asking for the months, not a guessed month
rule 18: "Responsible for", "Helped with" and "Was responsible for" openers become strong verbs
rule 18: present-tense bullets in the finished Example Logistics job move to past tense
rule 2: the long REST API bullet is cut down to one line
rule 20: "Improved app performance significantly" gets a Gap row asking how much
rule 12: the skills paragraph becomes labeled lines, without "fast learner" or "team player"
rule 9: the LinkedIn URL is shown as `linkedin.com/in/jordanlee`
rule 15: the Coding Club entry keeps one bullet (a Cut row)
rule 1: Cut rows, weakest lines first, bring it to one page

## Must not
- add a GitHub link or any contact item the fixture doesn't have
- add a number, team size or result the fixture doesn't state
- give "Summer 2022" a month
