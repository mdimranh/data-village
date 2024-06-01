from django.db import models

DISCOUNT_TYPE = (
    ('percentage', 'Percentage'),
    ('fixed_amount', 'Fixed Amount'),
)

CLASS_TYPE = (
    ('OnlineLiveClass', 'Online Live Class'),
    ('PhysicalClass', 'Physical Class'),
)

class Course(models.Model):
    title = models.TextField()
    thumbnail = models.ImageField(upload_to="media/course/thumb")
    class_type = models.CharField(max_length=100, choices=CLASS_TYPE, default="OnlineLiveClass")
    class_start = models.DateField(blank=True, null=True)
    free = models.BooleanField(default=False)
    fee = models.IntegerField()
    discount_amount = models.IntegerField(blank=True, null=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, blank=True, null=True, max_length=20)

    class Meta:
        ordering = ["-id"]

    def start_date(self):
        return self.class_start.strftime("%m/%d/%Y")

    def classType(self):
        if self.class_type == "OnlineLiveClass":
            return "Online Live Class"
        else: return "Physical Class"


    def final_fee(self):
        if self.discount_amount is not None and self.discount_type is not None:
            if self.discount_type == 'percentage':
                return max(self.fee - (self.fee * self.discount_amount / 100), 0)
            else:
                return max(self.fee - self.discount_amount, 0)

    def __str__(self):
        return self.title