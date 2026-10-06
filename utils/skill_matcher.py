import re
def skill_exists(skill, text):

    pattern = r"\b" + re.escape(skill) + r"\b"

    return bool(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
    )
def find_matching_skills(skills, text):

    found = []
    missing = []

    for skill in skills:

        if skill_exists(skill, text):
            found.append(skill)

        else:
            missing.append(skill)

    return found, missing


def calculate_score(found, total):

    if total == 0:
        return 0

    score = (len(found) / total) * 100

    return round(score)