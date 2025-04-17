from django.contrib import admin
from .models import Course, Enrollment


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'attendee_qty', 'spaces_left', 'start_date', 'location')

    def spaces_left(self, obj):
        return obj.spaces_left

admin.site.register(Course, CourseAdmin)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'course',
        'spots_booked',
        'is_paid',
        'confirmed',
        'status',
        'order',
    )
    list_editable = ('confirmed',)
    list_filter = ('confirmed', 'status', 'course')
    search_fields = ('user__username', 'course__title') 

    actions = ['mark_as_paid', 'mark_as_confirmed']

    def mark_as_paid(self, request, queryset):
        for enrollment in queryset:
            enrollment.is_paid = True
            enrollment.send_course_email()
            enrollment.save()
        self.message_user(request, "Selected enrollments have been marked as paid and emails sent.")

    mark_as_paid.short_description = "Mark selected as paid and send confirmation email"

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(confirmed=True)
        self.message_user(request, f"{updated} enrollment(s) marked as confirmed.")

    mark_as_confirmed.short_description = "Mark selected as confirmed"


admin.site.register(Enrollment, EnrollmentAdmin)
