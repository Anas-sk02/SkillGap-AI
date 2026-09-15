from fastapi import APIRouter, HTTPException
from backend.schemas import StudentProfile, RoadmapResponse, RoadmapStageSkill
from backend.services import prediction_service, recommendation_service, roadmap_service
from ml.preprocessing import ROLES

router = APIRouter()


@router.post("/roadmap", response_model=RoadmapResponse)
def get_roadmap(profile: StudentProfile):
    if profile.target_role not in ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role. Choose from: {sorted(ROLES)}")

    result = prediction_service.predict(profile.model_dump())
    ranked = recommendation_service.get_ranked_missing_skills(result["missing_skills"], profile.target_role)
    roadmap = roadmap_service.get_roadmap(ranked)

    serialized_roadmap = {
        stage: [RoadmapStageSkill(**s) for s in skills]
        for stage, skills in roadmap.items()
    }

    return RoadmapResponse(target_role=profile.target_role, roadmap=serialized_roadmap)
