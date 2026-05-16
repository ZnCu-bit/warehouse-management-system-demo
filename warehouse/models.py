from django.db import models

class Goods(models.Model):
    gid = models.CharField(max_length=20, verbose_name="商品编号", primary_key=True)
    name = models.CharField(max_length=50, verbose_name="商品名称")
    stock = models.IntegerField(default=0, verbose_name="库存数量")
    price = models.FloatField(default=0, verbose_name="商品单价")

    def __str__(self):
        return self.name
