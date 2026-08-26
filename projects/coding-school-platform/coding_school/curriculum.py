from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class ExerciseSpec:
    student_prompt: str
    teacher_notes: str
    starter_code: str
    solution_visibility: str = "teacher-only"


@dataclass(frozen=True)
class AssessmentSpec:
    rubric: tuple[str, ...]
    evidence_types: tuple[str, ...]
    mastery_levels: tuple[str, ...]


@dataclass(frozen=True)
class ProjectSpec:
    prompt: str
    milestones: tuple[str, ...]


@dataclass(frozen=True)
class ProgressSpec:
    unlock_rule: str
    badges: tuple[str, ...]
    parent_summary_template: str


@dataclass(frozen=True)
class CurriculumItem:
    id: str
    track: str
    stage: str
    module: str
    lesson: str
    concept_tags: tuple[str, ...]
    skill_tags: tuple[str, ...]
    prerequisites: tuple[str, ...]
    rubric: tuple[str, ...]
    badges: tuple[str, ...]
    age_band: str = "10-14 JavaScript Core"
    student_facing_goal: str = ""
    teacher_facing_goal: str = ""
    learning_loop: tuple[str, ...] = ()
    exercise: ExerciseSpec | None = None
    assessment: AssessmentSpec | None = None
    project: ProjectSpec | None = None
    progress: ProgressSpec | None = None
    source_files: tuple[str, ...] = ()
    starter_code: str = ""


def _manifest_path() -> Path:
    return Path(__file__).resolve().parents[1] / "curriculum" / "canonical-curriculum-manifest.json"


def _load_manifest() -> dict[str, object]:
    return json.loads(_manifest_path().read_text())


def _item_from_manifest(item: dict[str, object]) -> CurriculumItem:
    exercise = item.get("exercise") or {}
    assessment = item.get("assessment") or {}
    project = item.get("project") or {}
    progress = item.get("progress") or {}
    return CurriculumItem(
        id=str(item["id"]),
        track=str(item["track"]),
        stage=str(item["stage"]),
        module=str(item["module"]),
        lesson=str(item["title"]),
        concept_tags=tuple(item.get("conceptTags", ())),
        skill_tags=tuple(item.get("skillTags", ())),
        prerequisites=tuple(item.get("prerequisites", ())),
        rubric=tuple(assessment.get("rubric") or item.get("rubric", ())),
        badges=tuple(progress.get("badges") or item.get("badges", ())),
        age_band=str(item.get("ageBand", "10-14 JavaScript Core")),
        student_facing_goal=str(item.get("studentFacingGoal", "")),
        teacher_facing_goal=str(item.get("teacherFacingGoal", "")),
        learning_loop=tuple(item.get("learningLoop", ())),
        exercise=ExerciseSpec(
            student_prompt=str(exercise.get("studentPrompt", "")),
            teacher_notes=str(exercise.get("teacherNotes", "")),
            starter_code=str(exercise.get("starterCode", "")),
            solution_visibility=str(exercise.get("solutionVisibility", "teacher-only")),
        ) if exercise else None,
        assessment=AssessmentSpec(
            rubric=tuple(assessment.get("rubric", ())),
            evidence_types=tuple(assessment.get("evidenceTypes", ())),
            mastery_levels=tuple(assessment.get("masteryLevels", ())),
        ) if assessment else None,
        project=ProjectSpec(
            prompt=str(project.get("prompt", "")),
            milestones=tuple(project.get("milestones", ())),
        ) if project else None,
        progress=ProgressSpec(
            unlock_rule=str(progress.get("unlockRule", "")),
            badges=tuple(progress.get("badges", ())),
            parent_summary_template=str(progress.get("parentSummaryTemplate", "")),
        ) if progress else None,
        source_files=tuple(item.get("sourceFiles", ())),
        starter_code=str(exercise.get("starterCode", "")),
    )


def curriculum_catalog() -> tuple[CurriculumItem, ...]:
    manifest = _load_manifest()
    return tuple(_item_from_manifest(item) for item in manifest["lessons"])
