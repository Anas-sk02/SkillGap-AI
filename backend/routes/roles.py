import json
import os
from fastapi import APIRouter, HTTPException
from backend.schemas import RoleDetail, RoleSkillDetail, RolesCatalogueResponse

router = APIRouter()

TAXONOMY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'data', 'processed', 'role_skill_taxonomy.json'
)

_taxonomy_cache = None


def _load_taxonomy():
    global _taxonomy_cache
    if _taxonomy_cache is None:
        with open(TAXONOMY_PATH) as f:
            _taxonomy_cache = json.load(f)
    return _taxonomy_cache


@router.get("/roles", response_model=RolesCatalogueResponse)
def get_all_roles():
    taxonomy = _load_taxonomy()
    roles = [
        RoleDetail(
            role=role_name,
            skills=[RoleSkillDetail(**s) for s in role_data["skills"]]
        )
        for role_name, role_data in taxonomy.items()
    ]
    return RolesCatalogueResponse(roles=roles)


@router.get("/roles/{role_name}", response_model=RoleDetail)
def get_role_detail(role_name: str):
    taxonomy = _load_taxonomy()
    normalized = role_name.replace("-", " ").title()

    for key, val in taxonomy.items():
        if key.lower() == normalized.lower() or key.lower() == role_name.lower():
            return RoleDetail(role=key, skills=[RoleSkillDetail(**s) for s in val["skills"]])

    raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found.")
