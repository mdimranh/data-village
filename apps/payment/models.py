from django.db import models


class Payment(models.Model):
    tran_id = models.CharField(max_length=255)
    val_id = models.CharField(max_length=255)
    amount = models.FloatField()
    store_amount = models.FloatField()
    card_type = models.CharField(max_length=100)
    card_no = models.CharField(max_length=255)
    bank_tran_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    tran_date = models.DateTimeField(auto_now_add=True)