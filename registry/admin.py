from django.contrib import admin
from .models import (
    Member, Sacrament, SacramentParticipant,
    BaptismDetail, ConfirmationDetail, CommunionDetail,
    MarriageDetail, LastRitesDetail, Pledge, PledgePayment
)

admin.site.register(Member)
admin.site.register(Sacrament)
admin.site.register(SacramentParticipant)
admin.site.register(BaptismDetail)
admin.site.register(ConfirmationDetail)
admin.site.register(CommunionDetail)
admin.site.register(MarriageDetail)
admin.site.register(LastRitesDetail)
admin.site.register(Pledge)
admin.site.register(PledgePayment)
