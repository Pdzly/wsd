from functools import lru_cache

from apps.common.models.base import BaseModel
from apps.common.utils import camel_to_snake, track_events
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

VOTE_CLASS_ATTRIBUTE = "vote_class"


@lru_cache(maxsize=None)
def create_vote_class(klass, name):
    class Vote(BaseModel):
        REPR = "<{self.__class__.__name__}: {self.post} by {self.user}>"

        class VoteType(models.IntegerChoices):
            UPVOTE = 1, _("Upvote")
            DOWNVOTE = -1, _("Downvote")

        user = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE,
            related_name=f"{camel_to_snake(klass.__name__)}_votes",
            verbose_name=_("User"),
            help_text=_("The voter."),
        )
        post = models.ForeignKey(
            klass,
            on_delete=models.CASCADE,
            related_name=name,
            verbose_name=_("Post"),
            help_text=_("The post this vote is for."),
        )
        body = models.IntegerField(
            choices=VoteType.choices,
            verbose_name=_("Body"),
            help_text=_("The actual vote. -1 or +1"),
        )

        def type(self):
            return self.get_body_display()

        class Meta:
            abstract = True
            app_label = klass._meta.app_label  # NOQA

    klass_name = f"{klass.__name__}Vote"
    bases = (Vote,)

    class Meta:
        app_label = klass._meta.app_label  # NOQA
        verbose_name = _(f"{klass.__name__} Vote")
        verbose_name_plural = _(f"{klass._meta.verbose_name.title()} Votes")  # NOQA
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name=f"unique_{camel_to_snake(klass_name)}",
            ),
        ]

    klass_dict = {"__module__": klass.__module__, "Meta": Meta}
    vote_class = track_events(app_label=klass._meta.app_label)(type(klass_name, bases, klass_dict))  # NOQA
    return vote_class


class VoteMaker:
    def contribute_to_class(self, cls, name):  # NOQA
        setattr(cls, VOTE_CLASS_ATTRIBUTE, create_vote_class(cls, name))


def votes():
    vote_maker = VoteMaker()
    return vote_maker
