from django.db import models

DISCOUNT_TYPE = (
    ('percentage', 'Percentage'),
    ('fixed_amount', 'Fixed Amount'),
)

class Course(models.Model):
    title = models.TextField()
    thumbnail = models.ImageField(upload_to="media/course/thumb")
    free = models.BooleanField(default=False)
    fee = models.IntegerField()
    discount_amount = models.IntegerField(blank=True, null=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, blank=True, null=True, max_length=20)

    def final_fee(self):
        if self.discount_amount is not None and self.discount_type is not None:
            if self.discount_type == 'percentage':
                return max(self.fee - (self.fee * self.discount_amount / 100), 0)
            else:
                return max(self.fee - self.discount_amount, 0)

    def __str__(self):
        return self.title