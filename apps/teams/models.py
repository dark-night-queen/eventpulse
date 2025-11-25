# Standard Library imports
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# App imports
from apps.common.models import AbstractBaseModel
from apps.teams.constants import Roles


class Team(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class TeamMember(AbstractBaseModel):
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.MEMBER)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    profile_metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("team", "user")


class TeamPermissionDoc(AbstractBaseModel):
    title = models.CharField(max_length=200, blank=True)
    json_text = models.JSONField(default=dict, blank=True)
    version = models.PositiveIntegerField(db_index=True)
    previous_version = models.ForeignKey(
        "TeamPermissionDoc",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_versions",
    )

    created_by = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_permission_docs",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="permission_docs",
    )
    last_updated_by = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_permission_docs",
    )

    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        unique_together = ("team", "version")
        ordering = ["-version", "-created_at"]

    def clean(self):
        if self.previous_version and self.previous_version.team_id != self.team_id:
            raise ValidationError("Previous version must belong to the same team.")
