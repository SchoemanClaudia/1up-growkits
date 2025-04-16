from django.contrib import admin
from .models import Course, Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_paid', 'confirmed', 'status',)
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        for enrollment in queryset:
            enrollment.is_paid = True
            enrollment.send_course_email()
            enrollment.save()
        self.message_user(request, "Selected enrollments have been marked as paid and emails sent")
    mark_as_paid.short_description = "Mark selected as paid and send confirmation email"

admin.site.register(Course)
admin.site.register(Enrollment, EnrollmentAdmin)